from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
import numpy as np

from vibra.utils.interface_functions import get_main_window

from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.call_double_confirmation_input import CallDoubleConfirmationInput

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class SpecificImpedanceInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/ui_files/model/acoustic/specific_impedance_input.ui'), self)

        icon_path = str(Path('data/icons/logo_vibra.png'))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set specific impedance")

        self.main_window = get_main_window()
        self.main_window.set_input_widget(self)
        self.project = self.main_window.project
        self.properties = self.project.model.properties

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_info()
        self.exec()


    def _reset_variables(self):
        self.typed_ids = []
        self.remove_specific_impedance = False
        self.specific_impedance = None
        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.project_path = self.project.file.project_path
        self.acoustic_bc_filename = self.project.file.acoustic_model_setup_filename
        self.acoustic_bc_info_path = os.path.join(self.project_path, self.acoustic_bc_filename)
        self.acoustic_folder_path = self.project.file.acoustic_imported_data_folder_path
        self.specific_impedance_tables_folder_path = os.path.join(self.acoustic_folder_path, "specific_impedance_files") 


    def _define_qt_variables(self):
        # QCheckBox objects
        self.checkBox_averaged_constant_values = self.findChild(QCheckBox, 'checkBox_averaged_constant_values')
        self.checkBox_averaged_table_values = self.findChild(QCheckBox, 'checkBox_averaged_table_values')
        # QLineEdit objects
        self.lineEdit_selection_id = self.findChild(QLineEdit, 'lineEdit_selection_id')
        self.lineEdit_real_value = self.findChild(QLineEdit, 'lineEdit_real_value')
        self.lineEdit_imag_value = self.findChild(QLineEdit, 'lineEdit_imag_value')
        self.lineEdit_load_table_path = self.findChild(QLineEdit, 'lineEdit_table_path')
        # QPushButton objects
        self.pushButton_load_table = self.findChild(QPushButton, 'pushButton_load_table')
        self.pushButton_constant_value_confirm = self.findChild(QPushButton, 'pushButton_constant_value_confirm')
        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_reset = self.findChild(QPushButton, 'pushButton_reset')
        # QRadioButton objects
        self.radioButton_nodal_attribution_constant = self.findChild(QRadioButton, 'radioButton_nodal_attribution_constant')
        self.radioButton_element_integration_constant = self.findChild(QRadioButton, 'radioButton_element_integration_constant')
        self.radioButton_element_integration_table = self.findChild(QRadioButton, 'radioButton_element_integration_table')
        self.radioButton_nodal_attribution_table = self.findChild(QRadioButton, 'radioButton_nodal_attribution_table')
        # QSpinBox object
        self.spinBox_skiprows = self.findChild(QSpinBox, 'spinBox')
        # QTabWidget objects
        self.tabWidget_specific_impedance = self.findChild(QTabWidget, "tabWidget_specific_impedance")
        self.tab_constant_values = self.tabWidget_specific_impedance.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_specific_impedance.findChild(QWidget, "tab_table_values")
        self.tab_remove = self.tabWidget_specific_impedance.findChild(QWidget, "tab_remove")
        self.current_tab =  self.tabWidget_specific_impedance.currentIndex()
        # QTreeWidget objects
        self.treeWidget_specific_impedance = self.findChild(QTreeWidget, 'treeWidget_specific_impedance')
        self.treeWidget_specific_impedance.setColumnWidth(1, 20)
        self.treeWidget_specific_impedance.setColumnWidth(2, 80)


    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.remove_bc_from_selection)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_load_table.clicked.connect(self.load_specific_impedance_table)
        self.pushButton_reset.clicked.connect(self.check_reset)
        #
        self.radioButton_nodal_attribution_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_element_integration_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_nodal_attribution_table.clicked.connect(self.update_controls_for_table_of_values)
        self.radioButton_element_integration_table.clicked.connect(self.update_controls_for_table_of_values)
        #
        self.tabWidget_specific_impedance.currentChanged.connect(self.tabEvent_specific_impedance)
        self.treeWidget_specific_impedance.itemClicked.connect(self.on_click_item)
        self.treeWidget_specific_impedance.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        geometry_widget = self.main_window.viewer_tabs.geometry_widget
        geometry_widget.selection_changed.connect(self.geometry_selection_callback)


    def tabEvent_specific_impedance(self):
        self.current_tab =  self.tabWidget_specific_impedance.currentIndex()
        if self.current_tab == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)


    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))


    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.remove_bc_from_selection()


    def load_info(self):
        self.treeWidget_specific_impedance.clear()
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                real_values = np.array(data["real_values"])
                imag_values = np.array(data["imag_values"])
                complex_values = real_values + 1j*imag_values
                new = QTreeWidgetItem([str(surface_id), str(self.text_label(complex_values))])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_specific_impedance.addTopLevelItem(new)
        self.update_tabs_visibility()


    def geometry_selection_callback(self, points, lines, faces):
        
        if faces:
            text = ", ".join([str(i) for i in faces])
            self.lineEdit_selection_id.setText(text)
        
        elif not any([points, lines, faces]):
            self.lineEdit_selection_id.setText("")


    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        title = "Invalid entry to the specific impedance"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of specific impedance."
                PrintMessageInput([title, message, window_title_1])
                self.lineEdit_real_value.setFocus()
                self.stop = True
                return
        else:
            real_F = 0

        if lineEdit_imag.text() != "":
            try:
                imag_F = float(lineEdit_imag.text())
            except Exception:
                message = "Wrong input for imaginary part of specific impedance."
                PrintMessageInput([title, message, window_title_1])
                self.lineEdit_imag_value.setFocus()
                self.stop = True
                return
        else:
            imag_F = 0
        
        if real_F == 0 and imag_F == 0:
            return None
        else:
            return real_F + 1j*imag_F


    def check_constant_values(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        for _id in self.typed_ids:
            self.properties._remove_surface_property("acoustic_pressure", _id)
            self.properties._remove_surface_property("mass_flow_rate", _id)
            self.properties._remove_surface_property("volume_velocity", _id)
            self.properties._remove_surface_property("particle_velocity", _id)
            self.properties._remove_surface_property("compressor_excitation", _id)

        specific_impedance = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)
 
        if self.stop:
            return

        if specific_impedance is not None:

            self.specific_impedance = specific_impedance
            real_values = [np.real(specific_impedance)]
            imag_values = [np.imag(specific_impedance)]

            nodal_attribution = self.radioButton_nodal_attribution_constant.isChecked()
            key_avg =self.checkBox_averaged_constant_values.isChecked()
            
            data = {"real_values" : real_values,
                    "imag_values" : imag_values,
                    "nodal_attribution" : nodal_attribution,
                    "averaged" : key_avg}

            for _id in self.typed_ids:
                self.project.set_specific_impedance(data, _id)

            self.properties.export_model_properties()

            print(f"[Set specific impedance] - defined at surface(s) {self.typed_ids}")
            #TODO: remove existing tables and update the render            
            self.close()

        else:    
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance\n" 
            message += "before confirming the input!"
            PrintMessageInput([title, message, window_title_1])
            self.lineEdit_real_value.setFocus()

      
    def load_table(self, lineEdit, direct_load=False):
        title = "Error reached while loading 'specific impedance' table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the specific impedance'
                self.path_imported_table, _ = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Files (*.csv; *.dat; *.txt)')

            if self.path_imported_table == "":
                return None, None

            imported_filename = os.path.basename(self.path_imported_table)
            lineEdit.setText(self.path_imported_table)
            
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")

            if imported_file.shape[1] < 3:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have three columns in the form: frequencies, real and imaginary values."
                PrintMessageInput([title, message, window_title_1])
                return None, None
        
            imported_values = imported_file[:,1]

            if imported_file.shape[1] >= 3:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]
                self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
                
                #TODO: ensure that the table frequency setup governing the model setup 
                # if self.project.change_project_frequency_setup(imported_filename, list(self.frequencies)):
                #     self.lineEdit_reset(self.lineEdit_load_table_path)
                #     return None, None
                # else:
                #     self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)

            return imported_values, imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            lineEdit.setFocus()
            return None, None


    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()


    def save_table_file(self, entity_id, values, filename):
        try:

            self.project.create_folders_acoustic("specific_impedance_files")
        
            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"Vibra - imported table for specific impedance @ surface {entity_id} \n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[m³/s], imaginary[m³/s], absolute[m³/s]"
            basename = f"specific_impedance_surface_{entity_id}.dat"
            
            new_path_table = os.path.join(self.specific_impedance_tables_folder_path, basename)
            np.savetxt(new_path_table, data, delimiter=",", header=header)
            return values, basename

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            return None, None

    def load_specific_impedance_table(self):
        self.imported_values, self.filename_specific_impedance = self.load_table(self.lineEdit_load_table_path)

    def check_table_values(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        for _id in self.typed_ids:
            self.properties._remove_surface_property("acoustic_pressure", _id)
            self.properties._remove_surface_property("mass_flow_rate", _id)
            self.properties._remove_surface_property("volume_velocity", _id)
            self.properties._remove_surface_property("particle_velocity", _id)
            self.properties._remove_surface_property("compressor_excitation", _id)

        list_table_names = self.get_list_table_names_from_selected_surfaces(self.typed_ids)
        if self.lineEdit_load_table_path != "":
            for _id in self.typed_ids:
                if self.filename_specific_impedance is None:
                    self.imported_values, self.filename_specific_impedance = self.load_table(  self.lineEdit_load_table_path, 
                                                                                            direct_load=True  )
                if self.imported_values is None:
                    return
                else:
                    self.specific_impedance, self.basename_specific_impedance = self.save_table_file( _id, 
                                                                                                self.imported_values, 
                                                                                                self.filename_specific_impedance )
                    if self.basename_specific_impedance in list_table_names:
                        list_table_names.remove(self.basename_specific_impedance)

                    real_values = list(np.real(self.specific_impedance))
                    imag_values = list(np.imag(self.specific_impedance))

                    nodal_attribution = self.radioButton_nodal_attribution_table.isChecked()
                    key_avg = self.checkBox_averaged_constant_values.isChecked()

                    data = {"real_values" : real_values,
                            "imag_values" : imag_values,
                            "nodal_attribution" : nodal_attribution,
                            "averaged" : key_avg,
                            "table_name" : self.basename_specific_impedance}

                    self.project.set_specific_impedance(data, _id)
                
            self.properties.export_model_properties()

            self.process_table_file_removal(list_table_names)
            print(f"[Set specific impedance] - defined at surface(s) {self.typed_ids}")   
            self.close()
        else:    
            title = "Additional inputs required"
            message = "You must inform at least one specific impedance\n" 
            message += "table path before confirming the input!"
            PrintMessageInput([title, message, window_title_1])
            self.lineEdit_load_table_path.setFocus()

    def get_list_table_names_from_selected_surfaces(self, list_ids):
        list_table_names = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                if surface_id in list_ids:
                    if "table_name" in data.keys():
                        list_table_names.append(data["table_name"])
        return list_table_names

    def text_label(self, value):
        if value.shape[0] == 1:
            value_label = str(value)
        else:
            value_label = "Table"
        return "{}".format(value_label)

    def remove_bc_from_selection(self):
        if self.lineEdit_selection_id.text() != "":
            surface_properties = self.properties.surface_properties.copy()
            picked_id = int(self.lineEdit_selection_id.text())
            for key in surface_properties.keys():
                property, surface_id = key
                if property == "specific_impedance" and picked_id == surface_id:
                    #TODO: remove imported specific impedance tables
                    list_table_names = self.get_list_table_names_from_selected_surfaces([picked_id])
                    self.process_table_file_removal(list_table_names)
                    self.properties._remove_surface_property("specific_impedance", picked_id)
                    self.load_info()
                    self.lineEdit_selection_id.setText("")
                    return

    def process_table_file_removal(self, list_table_names):
        if list_table_names != []:
            for table_name in list_table_names:
                self.project.remove_acoustic_table_files_from_folder(table_name, "specific_impedance_files")    

    def check_reset(self):
        surface_ids = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                surface_ids.append(surface_id)

        if len(surface_ids) > 0:
            title = f"Resetting of all applied specific impedances"
            message = "Do you really want to remove the specific impedance applied to the following surface(s)?\n\n"
            message += f"{surface_ids}"
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "Close buttons to abort the current operation."
            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            _list_table_names = []
            if read._continue:
                for key, data in self.properties.surface_properties.items():
                    property, surface_id = key
                    if property == "specific_impedance":
                        if "table_name" in data.keys():
                            table_name = data[table_name]
                        else:
                            table_name = None
                        if table_name is not None:
                            if table_name not in _list_table_names:
                                _list_table_names.append(table_name)

                self.properties._reset_property("specific_impedance")
                self.properties.export_model_properties()

                #TODO: remove imported tables
                self.process_table_file_removal(_list_table_names)

                title = "specific impedance resetting process complete"
                message = "All specific impedance applied to the acoustic " 
                message += "model have been removed from the model."
                PrintMessageInput([title, message, window_title_2])

                self.close()


    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_load_table_path.setText("")


    def update_controls_for_constant_value(self):
        _bool = self.radioButton_element_integration_constant.isChecked()
        self.checkBox_averaged_constant_values.setChecked(not _bool)
        self.checkBox_averaged_constant_values.setDisabled(_bool)


    def update_controls_for_table_of_values(self):
        _bool = self.radioButton_element_integration_table.isChecked()
        self.checkBox_averaged_table_values.setChecked(not _bool)
        self.checkBox_averaged_table_values.setDisabled(_bool)


    def update(self):
        # This method should be called to update qt widgets whenever some entity has been clicked 
        return


    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        if self.current_tab != 2:
            self.lineEdit_selection_id.setText(text[:-2])


    def update_tabs_visibility(self):
        surface_ids = []
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "specific_impedance":
                surface_ids.append(surface_id)

        if len(surface_ids) == 0:
            self.tabWidget_specific_impedance.setCurrentWidget(self.tab_constant_values)
            self.tab_remove.setDisabled(True)
        else:
            self.tab_remove.setDisabled(False)

    
    def check_input_surface_id(self, lineEdit, single_ID=False):

        try:

            title = "Invalid entry to the Surface ID"
            message = ""
            tokens = lineEdit.strip().split(',')
            self.surface_ids = self.project.model.mesh.nodes_from_surfaces.keys()

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.surface_ids)
            list_ids = list(map(int, tokens))

            if len(list_ids) == 0:
                    message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."
            
            elif len(list_ids) >= 1: 
                if single_ID and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in self.surface_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. " 
                                message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. " 
                        message += f"The input value(s) must be integer(s) number(s) N such that 1 <= N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
            return True, [] 

        if single_ID:
            return False, list_ids[0]
        else:
            return False, list_ids


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_specific_impedance.currentIndex()==0:
                self.check_constant_values()
            if self.tabWidget_specific_impedance.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_specific_impedance.currentIndex()==2:
                self.remove_bc_from_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return