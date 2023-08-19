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

class MassFlowRateInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/ui_files/model/acoustic/mass_flow_rate_input.ui'), self)

        icon_path = str(Path('data/icons/logo_vibra.png'))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set mass flow rate acoustic excitation")

        self.main_window = get_main_window()
        self.project = self.main_window.project
        self.properties = self.project.model.properties

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.load_info()
        self.exec()


    def _reset_variables(self):
        self.typed_ids = []
        self.remove_mass_flow_rate = False
        self.mass_flow_rate = None
        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.project_path = self.project.file.project_path
        self.acoustic_bc_filename = self.project.file.acoustic_model_setup_filename
        self.acoustic_bc_info_path = os.path.join(self.project_path, self.acoustic_bc_filename)
        self.acoustic_folder_path = self.project.file.acoustic_imported_data_folder_path
        self.mass_flow_rate_tables_folder_path = os.path.join(self.acoustic_folder_path, "mass_flow_rate_files") 


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
        self.tabWidget_mass_flow_rate = self.findChild(QTabWidget, "tabWidget_mass_flow_rate")
        self.tab_constant_values = self.tabWidget_mass_flow_rate.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_mass_flow_rate.findChild(QWidget, "tab_table_values")
        self.tab_remove = self.tabWidget_mass_flow_rate.findChild(QWidget, "tab_remove")
        self.current_tab =  self.tabWidget_mass_flow_rate.currentIndex()
        # QTreeWidget objects
        self.treeWidget_mass_flow_rate = self.findChild(QTreeWidget, 'treeWidget_mass_flow_rate')
        self.treeWidget_mass_flow_rate.setColumnWidth(1, 20)
        self.treeWidget_mass_flow_rate.setColumnWidth(2, 80)


    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.remove_bc_from_selection)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_load_table.clicked.connect(self.load_mass_flow_rate_table)
        self.pushButton_reset.clicked.connect(self.check_reset)
        #
        self.radioButton_nodal_attribution_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_element_integration_constant.clicked.connect(self.update_controls_for_constant_value)
        self.radioButton_nodal_attribution_table.clicked.connect(self.update_controls_for_table_of_values)
        self.radioButton_element_integration_table.clicked.connect(self.update_controls_for_table_of_values)
        #
        self.tabWidget_mass_flow_rate.currentChanged.connect(self.tabEvent_mass_flow_rate)
        self.treeWidget_mass_flow_rate.itemClicked.connect(self.on_click_item)
        self.treeWidget_mass_flow_rate.itemDoubleClicked.connect(self.on_doubleclick_item)


    def tabEvent_mass_flow_rate(self):
        self.current_tab =  self.tabWidget_mass_flow_rate.currentIndex()
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
        self.treeWidget_mass_flow_rate.clear()
        for _id, data in self.properties.surfaces_with_mass_flow_rate.items():
            value = data["values"]
            new = QTreeWidgetItem([str(_id), str(self.text_label(value))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_mass_flow_rate.addTopLevelItem(new)
        self.update_tabs_visibility()


    def check_complex_entries(self, lineEdit_real, lineEdit_imag):

        self.stop = False
        title = "Invalid entry to the volume velocity"
        if lineEdit_real.text() != "":
            try:
                real_F = float(lineEdit_real.text())
            except Exception:
                message = "Wrong input for real part of volume velocity."
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
                message = "Wrong input for imaginary part of volume velocity."
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
        
        #TODO: remove the conflicting acoustic excitations and boundary conditions
        # self.project.remove_acoustic_pressure_table_files(self.typed_ids)
        # self.project.remove_compressor_excitation_table_files(self.typed_ids)
        # self.project.reset_compressor_info_by_node(self.typed_ids)

        mass_flow_rate = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)
 
        if self.stop:
            return

        if mass_flow_rate is not None:

            self.mass_flow_rate = mass_flow_rate

            key_avg = int(self.checkBox_averaged_constant_values.isChecked())
            data = {"entity_type" : "surface",
                    "entity_ids" : self.typed_ids,
                    "values" : mass_flow_rate,
                    "averaged" : key_avg}

            self.project.set_mass_flow_rate(data)
            print(f"[Set Mass Flow Rate] - defined at surface(s) {self.typed_ids}")
            #TODO: remove existing tables and update the render            
            self.close()

        else:    
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity\n" 
            message += "before confirming the input!"
            PrintMessageInput([title, message, window_title_1])
            self.lineEdit_real_value.setFocus()

      
    def load_table(self, lineEdit, direct_load=False):
        title = "Error reached while loading 'volume velocity' table"
        try:
            if direct_load:
                self.path_imported_table = lineEdit.text()
            else:
                window_label = 'Choose a table to import the volume velocity'
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

            self.project.create_folders_acoustic("mass_flow_rate_files")
        
            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"Vibra - imported table for volume velocity @ surface {entity_id} \n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[m³/s], imaginary[m³/s], absolute[m³/s]"
            basename = f"mass_flow_rate_surface_{entity_id}.dat"
            
            new_path_table = os.path.join(self.mass_flow_rate_tables_folder_path, basename)
            np.savetxt(new_path_table, data, delimiter=",", header=header)
            return values, basename

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            return None, None


    def load_mass_flow_rate_table(self):
        self.imported_values, self.filename_mass_flow_rate = self.load_table(self.lineEdit_load_table_path)


    def check_table_values(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        # self.project.remove_acoustic_pressure_table_files(self.typed_ids)
        # self.project.reset_compressor_info_by_node(self.typed_ids)

        list_table_names = self.get_list_table_names_from_selected_surfaces(self.typed_ids)
        if self.lineEdit_load_table_path != "":
            for _id in self.typed_ids:
                if self.filename_mass_flow_rate is None:
                    self.imported_values, self.filename_mass_flow_rate = self.load_table(  self.lineEdit_load_table_path, 
                                                                                            direct_load=True  )
                if self.imported_values is None:
                    return
                else:
                    self.mass_flow_rate, self.basename_mass_flow_rate = self.save_table_file( _id, 
                                                                                                self.imported_values, 
                                                                                                self.filename_mass_flow_rate )
                    if self.basename_mass_flow_rate in list_table_names:
                        list_table_names.remove(self.basename_mass_flow_rate)

                    key_avg = int(self.checkBox_averaged_constant_values.isChecked())
                    data = {"entity_type" : "surface",
                            "entity_ids" : self.typed_ids,
                            "values" : self.mass_flow_rate,
                            "averaged" : key_avg,
                            "table_name" : self.basename_mass_flow_rate}

            self.project.set_mass_flow_rate(data)

            self.process_table_file_removal(list_table_names)
            print(f"[Set Volume Velocity] - defined at surface(s) {self.typed_ids}")   
            self.close()
        else:    
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity\n" 
            message += "table path before confirming the input!"
            PrintMessageInput([title, message, window_title_1])
            self.lineEdit_load_table_path.setFocus()


    def get_list_table_names_from_selected_surfaces(self, list_ids):
        list_table_names = []
        for surface_id, data in self.properties.surfaces_with_mass_flow_rate.items():
            if surface_id in list_ids:
                if "table_name" in data.keys():
                    list_table_names.append(data["table_name"])

        return list_table_names


    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text


    def remove_bc_from_selection(self):
        if self.lineEdit_selection_id.text() != "":
            picked_id = int(self.lineEdit_selection_id.text())       
            if picked_id in self.properties.surfaces_with_mass_flow_rate.keys():
                section_key = f"surface - {picked_id}"           
                key_strings = ["volume velocity", "averaged", "table name"]
                message = f"The volume velocity attributed to the {picked_id} surface has been removed."
                self.project.file.remove_bc_from_file(section_key, self.acoustic_bc_info_path, key_strings, message)
                #TODO: remove imported volume velocity tables
                list_table_names = self.get_list_table_names_from_selected_surfaces([picked_id])
                self.process_table_file_removal(list_table_names)
                self.properties.remove_mass_flow_rate(picked_id)
                self.load_info()
                self.lineEdit_selection_id.setText("")
                # self.close()


    def process_table_file_removal(self, list_table_names):
        if list_table_names != []:
            for table_name in list_table_names:
                self.project.remove_acoustic_table_files_from_folder(table_name, "mass_flow_rate_files")    


    def check_reset(self):
        if len(self.properties.surfaces_with_mass_flow_rate) > 0:
 
            title = f"Resetting of all applied volume velocities"
            message = "Do you really want to remove the volume velocity applied to the following surface(s)?\n\n"
            entity_ids = list(self.properties.surfaces_with_mass_flow_rate.keys())
            message += f"{entity_ids}"
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "Close buttons to abort the current operation."
            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

            if read._doNotRun:
                return

            _list_table_names = []
            sections = []
            if read._continue:
                surfaces_ids = self.properties.surfaces_with_mass_flow_rate.keys()
                for _id in surfaces_ids:
                    key_strings = ["volume velocity", "averaged", "table name"]
                    sections.append(f"surface - {_id}")
                    data = self.properties.surfaces_with_mass_flow_rate[_id]
                    if "table_name" in data.keys():
                        table_name = data[table_name]
                    else:
                        table_name = None
                    if table_name is not None:
                        if table_name not in _list_table_names:
                            _list_table_names.append(table_name)
                self.project.file.remove_bc_from_file(sections, self.acoustic_bc_info_path, key_strings, None)
                self.properties.reset_mass_flow_rate()

                #TODO: remove imported tables
                self.process_table_file_removal(_list_table_names)

                title = "Volume velocity resetting process complete"
                message = "All volume velocity applied to the acoustic " 
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
        if len(self.properties.surfaces_with_mass_flow_rate) == 0:
            self.tabWidget_mass_flow_rate.setCurrentWidget(self.tab_constant_values)
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
            if self.tabWidget_mass_flow_rate.currentIndex()==0:
                self.check_constant_values()
            if self.tabWidget_mass_flow_rate.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_mass_flow_rate.currentIndex()==2:
                self.remove_bc_from_selection()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return