from datetime import datetime

from molde.interactor_styles.box_selection_style import BoxSelectionInteractorStyle
from molde.render_widgets.common_render_widget import CommonRenderWidget

from vibra.engine.model import Model
from vibra.interface.general.entity_visibility_handler import EntityVisibilityHandler
from vibra.interface.general.selection_handler import SelectionHandler
from vibra.interface.user_preferences import UserPreferences
from vibra.utils.interface_utils import SectionPlane, VisualizationFilter


class VibraRenderWidget(CommonRenderWidget):
    model: Model | None
    section_plane: SectionPlane | None
    user_preferences: UserPreferences
    visualization_filter: VisualizationFilter
    selection_handler: SelectionHandler | None
    entity_visibility_handler: EntityVisibilityHandler | None

    def __init__(self):
        super().__init__()
        self.set_interactor_style(BoxSelectionInteractorStyle())

        self.model = None
        self.section_plane = None
        self.user_preferences = UserPreferences()
        self.visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.selection_handler = None
        self.entity_visibility_handler = None

        self._last_click_time = None
        self._last_click_position = (0, 0)
        self._is_double_click = False
        self._must_update = False

    def render(self):
        # render is a better name for this action
        # I will update it later inside Molde
        self.update()

    def set_model(self, model: Model | None):
        self.model = model

    def set_section_plane(self, section_plane: SectionPlane | None):
        self.section_plane = section_plane

    def set_visualization_filter(self, visualization_filter: VisualizationFilter | None):
        if visualization_filter is None:
            visualization_filter = VisualizationFilter(faces=True, symbols=True)
        self.visualization_filter = visualization_filter

    def set_selection_handler(self, selection_handler: SelectionHandler | None):
        self.selection_handler = selection_handler

    def set_entity_visibility_handler(self, entity_visibility_handler: EntityVisibilityHandler | None):
        self.entity_visibility_handler = entity_visibility_handler

    def set_user_preferences(self, user_preferences: UserPreferences | None):
        if user_preferences is None:
            user_preferences = UserPreferences()
        self.user_preferences = user_preferences

    def click_start_callback(self, x0: int, y0: int):
        click_position = (x0, y0)
        click_time = datetime.now()
        self._is_double_click = False

        if self._last_click_time is not None:
            time_since_last_click = (click_time - self._last_click_time).total_seconds()

            x1, y1 = self._last_click_position
            moved_x = abs(x0 - x1) > self.user_preferences.click_dist_tolerance
            moved_y = abs(y0 - y1) > self.user_preferences.click_dist_tolerance
            mouse_moved = moved_x or moved_y

            self._is_double_click = (time_since_last_click < self.user_preferences.click_time_tolerance) and not mouse_moved

        self._last_click_time = click_time
        self._last_click_position = click_position

    def mouse_moved(self, x1: int, y1: int) -> bool:
        x0, y0 = self._last_click_position
        moved_x = abs(x0 - x1) > self.user_preferences.click_dist_tolerance
        moved_y = abs(y0 - y1) > self.user_preferences.click_dist_tolerance
        return moved_x or moved_y

    def showEvent(self, event):
        super().showEvent(event)
        if self._must_update:
            self.update_plot()
