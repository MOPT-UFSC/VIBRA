import logging
from enum import IntEnum

# from time import perf_counter
import numpy as np
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QCloseEvent

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.interface import error_title
from vibra.interface.data_handler.export_model_results import ExportModelResults
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.utils import clear_style_sheet
from vibra.interface.loading_window import LoadingWindow
from vibra.interface.numeric_checks.double_validator import StrictDoubleValidator
from vibra.interface.numeric_checks.unit_utilities import convert_length_unit, units_abreviations
from vibra.interface.plots.general.frequency_response_plotter import FrequencyResponsePlotter
from vibra.interface.ui_generated.plots.acoustic.transmission_loss_inputs_ui import TransmissionLossInputs_UI


class DataType(IntEnum):
    TRANSMISSION_LOSS = 0
    NOISE_REDUCTION = 1


class TLCalculation(IntEnum):
    NODAL_AREAS = 0
    SURFACE_INTEGRATION = 1


class CutoffFrequency(IntEnum):
    DISABLED = 0
    USER_DEFINED = 1
    AUTOMATIC = 2


class TransmissionLossInputs(TransmissionLossInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.show_geometry_render_widget()

        self._initialize()
        self._config_widgets()
        self._configure_validator()
        self._create_connections()
        self.check_and_load_transmission_loss_data()

    @property
    def model(self):
        return app().project.model

    @property
    def mesh(self):
        return app().project.model.mesh

    @property
    def properties(self):
        return app().project.model.properties

    @property
    def acoustic_post(self):
        return app().project.get_acoustic_postprocessing()

    def _initialize(self):
        self.unit_label = "dB"
        self.exporter = None
        self.plotter = None
        self.input_surface_id = None
        self.output_surface_id = None

    def _config_widgets(self):
        self.current_lineEdit = self.lineEdit_output_surface_id
        self.lineEdit_input_surface_id.setFocus()
        #
        unit = units_abreviations.get(self.mesh.length_unit)
        self.label_unit_combo_box.setText(f"[{unit}]")

    def _configure_validator(self):
        self.lineEdit_cutoff_frequency.setValidator(StrictDoubleValidator(0, 1e8, 6))

    def showEvent(self, event):
        super().showEvent(event)
        app().main_window.show_geometry_render_widget()

    def _create_connections(self):
        #
        self.comboBox_processing_selector.currentIndexChanged.connect(self.processing_selector_callback)
        self.comboBox_cutoff_frequency.currentIndexChanged.connect(self.compute_pipe_cutoff_frequency_callback)
        self.comboBox_cutoff_frequency_options.currentIndexChanged.connect(self.cutoff_frequency_options_callback)
        #
        self.pushButton_export_data.clicked.connect(self.export_data_callback)
        self.pushButton_flip_selection.clicked.connect(self.invert_selection)
        self.pushButton_help.clicked.connect(self.help_callback)
        self.pushButton_plot_data.clicked.connect(self.plot_data_callback)
        #
        app().main_window.selection.selection_changed.connect(self.geometry_selection_callback)
        #
        self.clickable(self.lineEdit_input_surface_id).connect(self.lineEdit_input_clicked)
        self.clickable(self.lineEdit_output_surface_id).connect(self.lineEdit_output_clicked)
        #
        self.lineEdit_output_clicked()
        self.update_cutoff_related_widgets_visibility()
        self.geometry_selection_callback()

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
        line_edits = [self.lineEdit_input_surface_id, self.lineEdit_output_surface_id]
        clear_style_sheet([line_edit for line_edit in line_edits if line_edit is not self.current_lineEdit])
        self.current_lineEdit.setStyleSheet("""border-color: rgb(32, 207, 255); border-width: 2px;""")

    def alternate_selected_line_edit(self):
        if self.current_lineEdit == self.lineEdit_input_surface_id:
            self.lineEdit_output_clicked()
            self.lineEdit_output_surface_id.setFocus()
        else:
            self.lineEdit_input_clicked()
            self.lineEdit_input_surface_id.setFocus()
    
    def geometry_selection_callback(self):

        if not app().main_window.action_results_workspace.isChecked():
            return

        faces = app().main_window.selection.geometry_surfaces
        if len(faces) != 1:
            return

        _faces = [str(i) for i in faces]
        self.current_lineEdit.setText(_faces[0])

    def check_and_load_transmission_loss_data(self):

        if self.comboBox_processing_selector.currentIndex() != DataType.TRANSMISSION_LOSS:
            return

        input_surface_candidate = list()
        output_surface_candidate = list()

        for (property, surf_id) in self.properties.surface_properties.keys():
            if property == "incident_plane_wave":
                if surf_id not in input_surface_candidate:
                    input_surface_candidate.append(surf_id)

            elif property == "specific_impedance":
                surface_velocity = self.properties._get_property("surface_velocity", surface=surf_id)
                if surface_velocity is None:
                    if surf_id not in output_surface_candidate:
                        output_surface_candidate.append(surf_id)

                elif surf_id not in input_surface_candidate:
                    input_surface_candidate.append(surf_id)

        if len(input_surface_candidate) == 1:
            if isinstance(self.input_surface_id, int) and self.input_surface_id != input_surface_candidate[0]:
                return True

            self.lineEdit_input_surface_id.setText(str(input_surface_candidate[0]))

        if len(output_surface_candidate) == 1:
            if isinstance(self.output_surface_id, int) and self.output_surface_id != output_surface_candidate[0]:
                return True

            self.lineEdit_output_surface_id.setText(str(output_surface_candidate[0]))

        if input_surface_candidate and output_surface_candidate:
            return False

        if input_surface_candidate:
            self.lineEdit_output_surface_id.setFocus()

        elif output_surface_candidate:
            self.lineEdit_input_surface_id.setFocus()

        return True

    def show_transmission_loss_calculating_requirements_message(self):
        title = "Invalid inputs detected"
        message = "The transmission loss calculation requires only one active excitation source "
        message += "at the input surface, commonly in the form of a incident plane wave with and a "
        message += "specific impedance at the output surface. Analogous results are obtained whether "
        message += "a surface velocity, combined with specific impedances in both input and output "
        message += "surfaces, is adopted. Any mismatch in these requirements will make the transmission "
        message += "loss calculation unfeasible."
        PrintMessageInput([error_title, title, message], height=300)

    def invert_selection(self):
        temp_text_input = self.lineEdit_input_surface_id.text()
        temp_text_output = self.lineEdit_output_surface_id.text()
        self.lineEdit_input_surface_id.setText(temp_text_output)
        self.lineEdit_output_surface_id.setText(temp_text_input)

    def processing_selector_callback(self):
        transmission_loss = self.comboBox_processing_selector.currentIndex() == DataType.TRANSMISSION_LOSS
        self.label_integration_method.setEnabled(transmission_loss)
        self.comboBox_integration_method.setEnabled(transmission_loss)

    def help_callback(self):
        window_title = "Help"
        if self.comboBox_processing_selector.currentIndex() == DataType.TRANSMISSION_LOSS:
            title = "Required data to process the Transmission Loss"
            message = "Dear user, to determine the Transmission Loss (TL) of a filter or duct it is necessary to select the "
            message += "input surface ID where the indicent wave is applied (usually by a normal surface velocity or incident "
            message += "plane wave source) and the output surface ID with an anechoic termination. An anechoic termination "
            message += " also should be applied at the input surface ID to avoid wave reflections caused by the source itself.\n"
            message += "\nInput surface ID: incident plane wave or surface velocity + anechoic impedance"
            message += "\nOutput surface ID: outlet of filter or duct with an anechoic impedance\n"
            height = 340
            width = 620

        else:
            title = "Required data to process the Noise Reduction"
            message = "Dear user, to determine the Noise Reduction (NR) it is necessary to select the input "
            message += "surface ID at inlet of the duct or filter and the surface ID at the end termination. "
            message += "By definition, the NR represents the sound pressure level differece between the "
            message += "input and output of a duct or filter and it does not require a anechoic termination."
            height = 300
            width = 480

        PrintMessageInput([window_title, title, message], height=height, width=width)

    def plot_data_callback(self):

        self.mesh.nodal_normals_data.clear()

        if self.check_inputs():
            return

        if self.join_model_data():
            return

        self.plotter = FrequencyResponsePlotter(close_dialogs=True)
        self.plotter.imported_real_data(decibel_data=True)

        f_cut = None
        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            f_cut = float(self.lineEdit_cutoff_frequency.text()) 

        self.plotter.set_cutoff_frequency(f_cut)
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
        self.input_surface_id, error_data = self.model.check_selected_ids(
            input_surface_id,
            "surfaces",
            domain="acoustic",
            single_id=True,
            )

        if error_data is not None:
            self.lineEdit_input_surface_id.setFocus()
            self.lineEdit_input_clicked()
            PrintMessageInput(error_data)
            return True

        output_surface_id = self.lineEdit_output_surface_id.text()
        self.output_surface_id, error_data = self.model.check_selected_ids(
            output_surface_id,
            "surfaces",
            domain="acoustic",
            single_id=True,
            )

        if error_data is not None:
            self.lineEdit_output_surface_id.setFocus()
            self.lineEdit_output_clicked()
            PrintMessageInput(error_data)
            return True

        if self.comboBox_processing_selector.currentIndex() == DataType.TRANSMISSION_LOSS:
            if self.check_and_load_transmission_loss_data():
                self.show_transmission_loss_calculating_requirements_message()
                return True

        if self.input_surface_id == self.output_surface_id:
            title = "Invalid surfaces selected"
            message = "The same surface has been selected in both input and output "
            message += "selection fields. You must selecting different sufaces to "
            message += "proceed with the transmission loss or noise reduction calculation."
            PrintMessageInput([error_title, title, message])
            return True

        if self.comboBox_cutoff_frequency_options.currentIndex() != CutoffFrequency.DISABLED:
            line_edit = self.lineEdit_cutoff_frequency
            if line_edit.text() == "":
                line_edit.setFocus()
                return True

    def update_cutoff_related_widgets_visibility(self):
        index = self.comboBox_cutoff_frequency_options.currentIndex()
        user_defined = index == CutoffFrequency.USER_DEFINED
        self.lineEdit_cutoff_frequency.setEnabled(user_defined)

        automatic = index == CutoffFrequency.AUTOMATIC
        self.comboBox_cutoff_frequency.setVisible(automatic)
        self.label_fc_combo_box.setVisible(automatic)
        self.label_unit_combo_box.setVisible(automatic)

    def cutoff_frequency_options_callback(self):
        index = self.comboBox_cutoff_frequency_options.currentIndex()
        self.update_cutoff_related_widgets_visibility()

        if index == CutoffFrequency.DISABLED:
            self.lineEdit_cutoff_frequency.clear()

        elif index == CutoffFrequency.AUTOMATIC:
            self.map_cylindrical_surfaces_to_fluids()
            self.compute_pipe_cutoff_frequency_callback()

    def map_cylindrical_surfaces_to_fluids(self):

        self.map_curvatures_to_fluid = {}
        self.comboBox_cutoff_frequency.clear()
        self.comboBox_cutoff_frequency.blockSignals(True)

        for surface_id, diameter in self.mesh.cylindrical_surfaces_data.items():

            d_in = convert_length_unit(diameter, "meter", self.mesh.length_unit)
            dr_in = round(d_in, 4)

            fluid = self.properties._get_property("fluid", surface=surface_id)
            if isinstance(fluid, Fluid):
                if (dr_in, fluid) not in self.map_curvatures_to_fluid.values():
                    self.map_curvatures_to_fluid[dr_in] = (dr_in, fluid)

            elif isinstance(fluid, list) and len(fluid) == 2:
                for _fluid in fluid:
                    if not isinstance(_fluid, Fluid):
                        continue

                    if (dr_in, _fluid) not in self.map_curvatures_to_fluid.values():
                        self.map_curvatures_to_fluid[dr_in] = (dr_in, _fluid)

        for (_d_in, fluid) in self.map_curvatures_to_fluid.values():
            self.comboBox_cutoff_frequency.addItem(str(_d_in))

        max_din = max(self.map_curvatures_to_fluid.keys())
        self.comboBox_cutoff_frequency.setCurrentText(str(max_din))
        self.comboBox_cutoff_frequency.blockSignals(False)

    def compute_pipe_cutoff_frequency_callback(self):
        if self.comboBox_cutoff_frequency.currentText() == "":
            return
        
        if not self.map_curvatures_to_fluid:
            return
        
        key = float(self.comboBox_cutoff_frequency.currentText())
        data = self.map_curvatures_to_fluid.get(key)
        if data is None:
            return

        d_in, fluid = data
        if not isinstance(fluid, Fluid):
            return

        if d_in == 0:
            return

        # speed of sound in m/s
        Co = fluid.speed_of_sound

        # cut-off frequency of a circular pipe
        d_in = convert_length_unit(d_in, self.mesh.length_unit, "meter")
        f_cut = round(1.8412 * Co / (np.pi * d_in), 4)

        self.lineEdit_cutoff_frequency.setText(str(f_cut))

    def join_model_data(self):

        self.model_results = {}

        if self.comboBox_processing_selector.currentIndex() == DataType.TRANSMISSION_LOSS:

            plot_type = "Transmission loss"

            def transmission_loss_callback():

                input_surface_id = int(self.lineEdit_input_surface_id.text())
                output_surface_id = int(self.lineEdit_output_surface_id.text())

                surface_ids = [
                    input_surface_id, 
                    output_surface_id,
                    ]

                surface_integration = self.comboBox_integration_method.currentIndex() == TLCalculation.SURFACE_INTEGRATION

                if not surface_integration:

                    logging.info("Processing the transmission loss... [10/100]")
                    self.mesh.process_face_elements_connected_to_nodes(surface_ids)

                    logging.info("Processing the transmission loss... [20/100]")
                    self.mesh.compute_nodal_areas()

                # t0 = perf_counter()

                x_data, y_data = self.acoustic_post.compute_transmission_loss(
                    input_surface_id,
                    output_surface_id,
                    surface_integration = surface_integration,
                    )

                # dt = perf_counter() - t0
                # print(f"Time to process TL: {dt}s")

                return x_data, y_data

            x_data, y_data = LoadingWindow(transmission_loss_callback).run()

        elif self.comboBox_processing_selector.currentIndex() == DataType.NOISE_REDUCTION:

            plot_type = "Noise reduction"
    
            x_data, y_data = self.acoustic_post.compute_noise_reduction(
                self.input_surface_id, 
                self.output_surface_id,
                )

        if y_data is None:
            title = "Invalid input surface id"
            message = "An invalid surface id has been selected at Input ID field. "
            message += "Check if the Input ID has a surface velocity excitation to proceed."
            PrintMessageInput([error_title, title, message])
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