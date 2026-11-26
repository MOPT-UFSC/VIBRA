from collections import defaultdict
from collections.abc import Sequence

from molde.colors import Color, color_names
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from vibra.engine.model import Model
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.viewer_3d.actors.geometry_actor import GeometryActor, GeometryTextures
from vibra.interface.viewer_3d.actors.symbols_actor_acoustic import SymbolsActorAcoustic
from vibra.interface.viewer_3d.actors.symbols_actor_structural import SymbolsActorStructural
from vibra.interface.viewer_3d.render_widgets.vibra_render_widget import VibraRenderWidget
from vibra.utils.interface_utils import GeometryColorMode, SectionPlane
from vibra.utils.time_utils import function_timer


class NewGeometryRenderWidget(VibraRenderWidget):
    def __init__(self):
        super().__init__()

        self.create_actors()

        self.left_clicked.connect(self.click_start_callback)
        self.left_released.connect(self.click_end_callback)

    def create_actors(self):
        self.create_axes()
        self.create_scale_bar()

        self.acoustic_symbols_actor = SymbolsActorAcoustic(self.model, self.renderer.GetActiveCamera())
        self.add_actors(self.acoustic_symbols_actor)

        self.structural_symbols_actor = SymbolsActorStructural(self.model, self.renderer.GetActiveCamera())
        self.add_actors(self.structural_symbols_actor)

        self.geometry_actor = GeometryActor(self.model)
        self.add_actors(self.geometry_actor)

    def set_model(self, model: Model | None):
        super().set_model(model)
        self.acoustic_symbols_actor.model = model
        self.structural_symbols_actor.model = model
        self.geometry_actor.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        super().set_section_plane(section_plane)
        self.geometry_actor.section_plane = section_plane

    @function_timer
    def update_plot(self, reset_camera: bool = False):
        if self.isVisible() or reset_camera:
            self._must_update = False
        else:
            self._must_update = True
            return

        self.geometry_actor.update()
        self.acoustic_symbols_actor.build()
        self.structural_symbols_actor.build()

        self.update_visualization()

        if reset_camera:
            self.renderer.ResetCamera()

        self.render()

    @function_timer
    def update_visualization(self):
        self.renderer.SetBackground(self.user_preferences.renderer_background_color_1.to_rgb_f())
        self.renderer.SetBackground2(self.user_preferences.renderer_background_color_2.to_rgb_f())

        self.acoustic_symbols_actor.SetVisibility(self.visualization_filter.symbols)
        self.structural_symbols_actor.SetVisibility(self.visualization_filter.symbols)

        self._update_points_appearance()
        self._update_lines_appearance()
        self._update_surfaces_appearance()

        self.geometry_actor.update_caches()
        self.render()

    def _update_points_appearance(self):
        self.geometry_actor.set_points_visibility(visible=self.visualization_filter.points)
        if not self.visualization_filter.points:
            return

        self.geometry_actor.set_point_size(self.user_preferences.points_size)
        self.geometry_actor.set_point_color(self.user_preferences.nodes_points_color)
        if self.selection_handler is not None:
            self.geometry_actor.paint_points(
                self.user_preferences.selection_nodes_points_color,
                self.selection_handler.geometry_points,
            )

    def _update_lines_appearance(self):
        self.geometry_actor.set_lines_visibility(visible=self.visualization_filter.lines)
        if not self.visualization_filter.lines:
            return

        self.geometry_actor.set_line_thickness(self.user_preferences.lines_thickness)
        self.geometry_actor.set_line_color(self.user_preferences.lines_color)
        if self.selection_handler is not None:
            self.geometry_actor.paint_lines(
                self.user_preferences.selection_lines_color,
                self.selection_handler.geometry_lines,
            )

    def _update_surfaces_appearance(self):
        self.geometry_actor.set_surfaces_visibility(visible=self.visualization_filter.faces)
        if not self.visualization_filter.faces:
            return

        if self.visualization_filter.color_mode == GeometryColorMode.EMPTY:
            self.geometry_actor.set_surface_color(self.user_preferences.faces_color)
        else:
            self._paint_surfaces_with_composition()

        if self.selection_handler is not None:
            self.geometry_actor.paint_volumes(
                self.user_preferences.selection_volumes_color,
                self.selection_handler.geometry_volumes,
            )
            self.geometry_actor.paint_surfaces(
                self.user_preferences.selection_faces_color,
                self.selection_handler.geometry_surfaces,
            )

        if self.entity_visibility_handler is not None:
            self.geometry_actor.hide_surfaces()
            self.geometry_actor.show_surfaces(list(self.entity_visibility_handler.get_visible_surfaces()))

    def _paint_surfaces_with_composition(self):
        if self.model is None:
            return

        mesh = self.model.mesh
        if mesh is None:
            return

        properties = self.model.properties
        surfaces_with_perforated_plates = self._surfaces_with_perforated_plate()
        color_to_surfaces = defaultdict(list)
        texture_to_surfaces = defaultdict(list)

        for surface in mesh.all_surface_ids():
            volumes = mesh.volumes_from_surface.get(surface, ())
            volume = self._first_visible_volume(volumes)

            fluid = properties._get_property("fluid", surface=surface, volume=volume)
            material = properties._get_property("material", surface=surface, volume=volume)
            porous = properties._get_property("porous_material_model", surface=surface, volume=volume)

            if surface in surfaces_with_perforated_plates:
                color = color_names.WHITE
                texture = GeometryTextures.HOLES_TEXTURE

            elif porous is not None:
                color = color_names.YELLOW_6
                texture = GeometryTextures.SPONGE_TEXTURE

            elif material is not None:
                color = Color(*material.color)
                texture = GeometryTextures.METAL_TEXTURE

            elif fluid is not None:
                color = Color(*fluid.color)
                texture = GeometryTextures.FLAT_TEXTURE

            else:
                color = color_names.WHITE
                texture = GeometryTextures.CHESS_TEXTURE

            color_to_surfaces[color].append(surface)
            texture_to_surfaces[texture].append(surface)

        for color, surfaces in color_to_surfaces.items():
            self.geometry_actor.paint_surfaces(color, surfaces)

        for texture, surfaces in texture_to_surfaces.items():
            self.geometry_actor.set_surfaces_texture(texture, surfaces)

    def click_end_callback(self, x1: int, y1: int):
        # TODO: move this method to the tools

        if self.selection_handler is None:
            return

        mouse_moved = self.mouse_moved(x1, y1)
        if mouse_moved:
            selection = self.area_pick(self._last_click_position[0], self._last_click_position[1], x1, y1)
        else:
            selection = self.pick(x1, y1)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = modifiers & Qt.KeyboardModifier.ControlModifier
        shift_pressed = modifiers & Qt.KeyboardModifier.ShiftModifier
        alt_pressed = modifiers & Qt.KeyboardModifier.AltModifier

        select_volume = any([self._is_double_click, shift_pressed, self.selection_handler.volume_selection_mode])
        if select_volume:
            selection.geometry_surfaces.clear()
        else:
            selection.geometry_volumes.clear()

        self.selection_handler.update_from(
            selection,
            join=ctrl_pressed,
            remove=alt_pressed,
        )

    def pick(self, x: int, y: int) -> SelectionHandler:
        return self.geometry_actor.pick(x, y, self.renderer)

    def area_pick(self, x0: int, y0: int, x1: int, y1: int) -> SelectionHandler:
        return self.geometry_actor.area_pick(x0, y0, x1, y1, self.renderer)

    def _first_visible_volume(self, volumes: Sequence[int]) -> int | None:
        if self.entity_visibility_handler is None:
            return None

        for volume in volumes:
            if volume not in self.entity_visibility_handler._volumes_to_hide:
                return volume

    def _surfaces_with_perforated_plate(self):
        # Find both surfaces of a perforated plate
        assert self.model is not None
        assert self.model.mesh is not None

        mesh = self.model.mesh
        properties = self.model.properties

        surfaces_with_perforated_plates = set()
        for surface in mesh.all_surface_ids():
            perforated = properties._get_property("perforated_plate_model", surface=surface)
            decoupling = properties._get_property("degrees_of_freedom_decoupling", surface=surface)
            if (perforated is not None) and (decoupling is not None):
                complementary_surface = decoupling.get("new_surface_id")
                surfaces_with_perforated_plates.add(surface)
                surfaces_with_perforated_plates.add(complementary_surface)

        return surfaces_with_perforated_plates
