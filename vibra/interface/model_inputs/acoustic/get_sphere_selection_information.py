from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.ui_generated.model.acoustic.others.get_sphere_selection_information_ui import GetSphereSelectionInformation_UI


class GetSphereSelectionInformation(GetSphereSelectionInformation_UI):
    def __init__(self, selection_id, selection_radius, averaged, filter_type, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self.selection_id = selection_id
        self.selection_radius = selection_radius
        self.averaged = averaged
        self.filter_type = filter_type

        self._config_window()
        self._config_widgets()
        self.get_selection_info()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _config_widgets(self):
        self.lineEdit_number_of_elements.setDisabled(True)
        self.lineEdit_number_of_nodes.setDisabled(True)
        self.lineEdit_selection_radius.setDisabled(True)
        self.lineEdit_selection_radius.setText(str(round(self.selection_radius, 6)))

    def get_selection_info(self):
        LoadingWindow(self.mesh.get_elements_and_nodes_from_sphere).run(
            self.selection_id,
            self.selection_radius,
            averaged=self.averaged,
            filter_type=self.filter_type,
        )

        list_elements = self.mesh.selected_elements
        list_nodes = self.mesh.nodes_inside_sphere

        list_center_coords = self.mesh.get_average_nodal_coordinates(  self.selection_id,
                                                                        averaged=self.averaged  )

        if len(list_center_coords) == 0:
            self.lineEdit_coordinate_x.setText("")
            self.lineEdit_coordinate_y.setText("")
            self.lineEdit_coordinate_z.setText("")

        elif len(list_center_coords) == 1:
            _round_center_coords = [round(value, 4) for value in list_center_coords[0]]
            self.lineEdit_coordinate_x.setText(str(_round_center_coords[0]))
            self.lineEdit_coordinate_y.setText(str(_round_center_coords[1]))
            self.lineEdit_coordinate_z.setText(str(_round_center_coords[2]))

        else:
            self.lineEdit_coordinate_x.setText("Multiple centers")
            self.lineEdit_coordinate_y.setText("Multiple centers")
            self.lineEdit_coordinate_z.setText("Multiple centers")

        self.lineEdit_number_of_elements.setText(str(len(list_elements)))
        self.lineEdit_number_of_nodes.setText(str(len(list_nodes)))

        if not app().main_window.action_mesh_workspace.isChecked():
            app().main_window.action_mesh_workspace_callback()

        self.highlight_mesh_elements(list_elements)

    def highlight_mesh_elements(self, solid_elements: list[int]):
        app().main_window.selection.set_mesh_selection(solids = solid_elements)