from PySide6.QtCore import Qt, QEvent, QObject, Signal
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.ui_generated.plots.acoustic.transmission_loss_inputs_ui import TransmissionLossInputs_UI
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.loading_window import LoadingWindow
from vibra.engine.postprocessing import get_noise_reduction, get_transmission_loss

import logging

window_title_1 = "Error"
window_title_2 = "Warning"


class TransmissionLossInputs(TransmissionLossInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self.project = app().project
        self.model = app().project.model
        self.mesh = app().project.model.mesh
        self.properties = app().project.model.properties

        self._initialize()
        self._create_connections()

        self._config_widgets()
        self._load_analysis_setup()

        if self.load_input_surface_id():
            return

        self.geometry_selection_callback()
    
    def showEvent(self, event):
        super().showEvent(event)
        app().main_window.show_geometry_render_widget()

    def _load_analysis_setup(self):
        self.analysis_method = ""
        analysis_setup = self.project.analysis_setup
        if "analysis_id" in analysis_setup.keys():
            if analysis_setup["analysis_id"] == AnalysisID.ACOUSTIC_HARMONIC:
                self.analysis_method = "Direct method"

    def _initialize(self):
        self.exporter = None
        self.plotter = None
        self.unit_label = "dB"

    def _create_connections(self):
        #
        self.comboBox_processing_selector.currentIndexChanged.connect(self.processing_selector_callback)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_flip_selection.clicked.connect(self.invert_selection)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_surface_id).connect(self.lineEdit_input_clicked)
        self.clickable(self.lineEdit_output_surface_id).connect(self.lineEdit_output_clicked)
        #
        self.lineEdit_output_clicked()

    def _config_widgets(self):
        self.current_lineEdit = self.lineEdit_output_surface_id
        self.lineEdit_input_surface_id.setFocus()

    def clickable(self, widget):
        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_input_clicked(self):
        self.current_lineEdit = self.lineEdit_input_surface_id
        self.highlight_selected_line_edit()

    def lineEdit_output_clicked(self):
        self.current_lineEdit = self.lineEdit_output_surface_id
        self.highlight_selected_line_edit()

    def highlight_selected_line_edit(self):

        if self.current_lineEdit == self.lineEdit_input_surface_id:
            self.lineEdit_output_surface_id.setStyleSheet("")
        else:
            self.lineEdit_input_surface_id.setStyleSheet("")

        self.current_lineEdit.setStyleSheet("""border-color: rgb(200, 0, 0); border-width: 2px;""")

    def alternate_selected_line_edit(self):
        if self.current_lineEdit == self.lineEdit_input_surface_id:
            self.lineEdit_output_clicked()
            self.lineEdit_output_surface_id.setFocus()
        else:
            self.lineEdit_input_clicked()
            self.lineEdit_input_surface_id.setFocus()
    
    def geometry_selection_callback(self):

        faces = app().main_window.selected_geometry_surfaces

        if faces:

            if len(faces) > 1:
                return

            else:
                _faces = [str(i) for i in faces]
                self.current_lineEdit.setText(_faces[0])

        else:
            return

    def load_input_surface_id(self):

        input_surface_candidate = list()
        output_surface_candidate = list()

        for (property, surf_id) in self.properties.surface_properties.keys():
            if property in ["surface_velocity", "incident_plane_wave"]:
                if id not in input_surface_candidate:
                    input_surface_candidate.append(surf_id)

            if property in ["specific_impedance"]:
                if surf_id in input_surface_candidate:
                    continue
                if id not in output_surface_candidate:
                    output_surface_candidate.append(surf_id)

        if len(input_surface_candidate) == 1:
            self.lineEdit_input_surface_id.setText(str(input_surface_candidate[0]))
    
        if len(output_surface_candidate) == 1:
            self.lineEdit_output_surface_id.setText(str(output_surface_candidate[0]))

        if input_surface_candidate:
            self.lineEdit_output_surface_id.setFocus()
        elif output_surface_candidate:
            self.lineEdit_input_surface_id.setFocus()

        if input_surface_candidate and output_surface_candidate:
            return False

        self.close()
        title = "Invalid inputs detected"
        message = "The transmission loss calculation requires only one active excitation source "
        message += "at the input surface, commonly in the form of a incident plane wave with and a "
        message += "specific impedance at the output surface. Analogous results are obtained whether "
        message += "a surface velocity, combined with specific impedances in both input and output "
        message += "surfaces, is adopted. Any mismatch in these requirements will make the transmission "
        message += "loss calculation unfeasible."
        PrintMessageInput([window_title_1, title, message])
        return True

    def invert_selection(self):
        temp_text_input = self.lineEdit_input_surface_id.text()
        temp_text_output = self.lineEdit_output_surface_id.text()
        self.lineEdit_input_surface_id.setText(temp_text_output)
        self.lineEdit_output_surface_id.setText(temp_text_input)

    def processing_selector_callback(self):
        index = self.comboBox_processing_selector.currentIndex()
        self.label_integration_method.setDisabled(bool(index))
        self.comboBox_integration_method.setDisabled(bool(index))

    def plot_data_callback(self):

        self.mesh.nodal_normals_data.clear()

        if self.check_inputs():
            return

        if self.join_model_data():
            return

        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter.imported_real_data()
        self.plotter._set_model_results_data_to_plot(self.model_results)
        app().main_window.update_symbols()

    def export_data_callback(self):

        if self.check_inputs():
            return

        if self.join_model_data():
            return

        self.exporter = ExportModelResults()
        self.exporter._set_data_to_export(self.model_results)

    def check_inputs(self):

        input_surface_id = self.lineEdit_input_surface_id.text()
        self.input_surface_id, error_data = self.mesh.check_selected_ids(   
                                                                         input_surface_id, 
                                                                         selection = "surfaces", 
                                                                         single_id = True
                                                                         )

        if error_data is not None:
            self.lineEdit_input_surface_id.setFocus()
            PrintMessageInput(error_data)
            return True

        output_surface_id = self.lineEdit_output_surface_id.text()
        self.output_surface_id, error_data = self.mesh.check_selected_ids(   
                                                                          output_surface_id, 
                                                                          selection = "surfaces", 
                                                                          single_id = True
                                                                          )

        if error_data is not None:
            self.lineEdit_output_surface_id.setFocus()
            PrintMessageInput(error_data)
            return True

        if self.input_surface_id == self.output_surface_id:
            title = "Invalid surfaces selected"
            message = "The same surface has been selected in both input and output "
            message += "selection fields. You must selecting different sufaces to "
            message += "proceed with the transmission loss or noise reduction calculation."
            PrintMessageInput([window_title_1, title, message])
            return True

    def join_model_data(self):

        self.model_results = dict()
        solver = self.project.acoustic_harmonic_solver

        if self.comboBox_processing_selector.currentIndex() == 0:

            plot_type = "Transmission loss"

            def transmission_loss_callback():

                surface_ids = [self.input_surface_id, self.output_surface_id]
                integration_method = self.comboBox_integration_method.currentIndex()

                if not integration_method:

                    logging.info("Processing the transmission loss... [10/100]")
                    self.mesh._process_face_elements_connected_to_nodes(surface_ids)

                    logging.info("Processing the transmission loss... [20/100]")
                    self.mesh.compute_nodal_areas()

                x_data, y_data = get_transmission_loss(
                    solver,
                    self.input_surface_id,
                    self.output_surface_id,
                    surface_integration = bool(integration_method),
                    )

                return x_data, y_data

            x_data, y_data = LoadingWindow(transmission_loss_callback).run()

        else:

            plot_type = "Noise reduction"
    
            x_data, y_data = get_noise_reduction(
                solver,
                self.input_surface_id, 
                self.output_surface_id,
                )

        if y_data is None:
            title = "Invalid input surface id"
            message = "An invalid surface id has been selected at Input ID field. "
            message += "Check if the Input ID has a surface velocity excitation to proceed."
            PrintMessageInput([window_title_1, title, message])
            return True

        self.title = f"{plot_type}"
        legend_label = f"{plot_type} between surfaces [{self.input_surface_id}] and [{self.output_surface_id}]"

        key = ("surface", (self.input_surface_id, self.output_surface_id))

        self.model_results[key] = { 
                                    "x_data" : x_data,
                                    "y_data" : y_data,
                                    "x_label" : "Frequency [Hz]",
                                    "y_label" : plot_type,
                                    "title" : self.title,
                                    "data_type" : plot_type.lower(),
                                    "legend" : legend_label,
                                    "unit" : self.unit_label,
                                    "color" : [0,0,1],
                                    "linestyle" : "-"  
                                    }

    def plot_nodal_normals(self, normals_data: dict):
        app().main_window.update_symbols()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.plot_data_callback()
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_Up:
            self.alternate_selected_line_edit()

    def closeEvent(self, a0: QCloseEvent | None) -> None:

        if self.exporter is not None:
            self.exporter.close()

        if self.plotter is not None:
            self.plotter.close()

        # self.keep_window_open = False
        return super().closeEvent(a0)