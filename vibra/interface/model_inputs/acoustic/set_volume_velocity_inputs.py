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

class VolumeVelocityInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/ui_files/model/acoustic/volume_velocity_input.ui'), self)

        icon_path = str(Path('data/icons/logo_vibra.png'))
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Set volume velocity boundary condition")

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
        self.remove_volume_velocity = False
        self.volume_velocity = None
        self.list_Nones = [None, None, None, None, None, None]
        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.project_path = self.project.file.project_path
        self.acoustic_bc_filename = self.project.file.acoustic_model_setup_filename
        self.acoustic_bc_info_path = os.path.join(self.project_path, self.acoustic_bc_filename)


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
        # QSpinBox object
        self.spinBox_skiprows = self.findChild(QSpinBox, 'spinBox')
        # QTabWidget objects
        self.tabWidget_volume_velocity = self.findChild(QTabWidget, "tabWidget_volume_velocity")
        self.tab_constant_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_constant_values")
        self.tab_table_values = self.tabWidget_volume_velocity.findChild(QWidget, "tab_table_values")
        self.tab_remove = self.tabWidget_volume_velocity.findChild(QWidget, "tab_remove")
        self.current_tab =  self.tabWidget_volume_velocity.currentIndex()
        # QTreeWidget objects
        self.treeWidget_volume_velocity = self.findChild(QTreeWidget, 'treeWidget_volume_velocity')
        self.treeWidget_volume_velocity.setColumnWidth(1, 20)
        self.treeWidget_volume_velocity.setColumnWidth(2, 80)


    def _create_connections(self):
        #
        self.pushButton_constant_value_confirm.clicked.connect(self.check_constant_values)
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)
        self.pushButton_table_values_confirm.clicked.connect(self.check_table_values)
        self.pushButton_load_table.clicked.connect(self.load_volume_velocity_table)
        self.pushButton_reset.clicked.connect(self.check_reset)
        #
        self.tabWidget_volume_velocity.currentChanged.connect(self.tabEvent_volume_velocity)
        self.treeWidget_volume_velocity.itemClicked.connect(self.on_click_item)
        self.treeWidget_volume_velocity.itemDoubleClicked.connect(self.on_doubleclick_item)


    def tabEvent_volume_velocity(self):
        self.current_tab =  self.tabWidget_volume_velocity.currentIndex()
        if self.current_tab == 2:
            self.lineEdit_selection_id.setText("")
            self.lineEdit_selection_id.setDisabled(True)
        else:
            self.lineEdit_selection_id.setDisabled(False)


    def load_info(self):
        self.treeWidget_volume_velocity.clear()
        for _id, [value, _] in self.properties.surfaces_with_volume_velocity.items():
            new = QTreeWidgetItem([str(_id), str(self.text_label(value))])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_volume_velocity.addTopLevelItem(new)
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

        volume_velocity = self.check_complex_entries(self.lineEdit_real_value, self.lineEdit_imag_value)
 
        if self.stop:
            return

        if volume_velocity is not None:

            self.volume_velocity = volume_velocity

            key_avg = int(self.checkBox_averaged_constant_values.isChecked())
            data = {"entity_type" : "surface",
                    "entity_ids" : self.typed_ids,
                    "values" : volume_velocity,
                    "averaged" : key_avg}

            self.project.set_volume_velocity(data)
            print(f"[Set Volume Velocity] - defined at node(s) {self.typed_ids}")
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

            if imported_file.shape[1]<2:
                message = "The imported table has insufficient number of columns. The spectrum"
                message += " data must have only two columns to the frequencies and values."
                PrintMessageInput([title, message, window_title_1])
                return None, None
        
            imported_values = imported_file[:,1]

            if imported_file.shape[1] >= 2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
               
                if self.project.change_project_frequency_setup(imported_filename, list(self.frequencies)):
                    self.lineEdit_reset(self.lineEdit_load_table_path)
                    return None, None
                else:
                    self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)

            return imported_values, imported_filename

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            lineEdit.setFocus()
            return None, None


    def lineEdit_reset(self, lineEdit):
        lineEdit.setText("")
        lineEdit.setFocus()


    def save_table_file(self, node_id, values, filename):
        try:

            self.project.create_folders_acoustic("volume_velocity_files")
        
            real_values = np.real(values)
            imag_values = np.imag(values)
            abs_values = np.abs(values)
            data = np.array([self.frequencies, real_values, imag_values, abs_values]).T

            header = f"Vibra - imported table for volume velocity @ node {node_id} \n"
            header += f"\nSource filename: {filename}\n"
            header += "\nFrequency [Hz], real[m³/s], imaginary[m³/s], absolute[m³/s]"
            basename = f"volume_velocity_node_{node_id}.dat"
            
            new_path_table = os.path.join(self.volume_velocity_tables_folder_path, basename)
            np.savetxt(new_path_table, data, delimiter=",", header=header)
            return values, basename

        except Exception as log_error:
            title = "Error reached while saving table files"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            return None, None


    def load_volume_velocity_table(self):
        self.imported_values, self.filename_volume_velocity = self.load_table(self.lineEdit_load_table_path)


    def check_table_values(self):

        lineEdit_selection_id = self.lineEdit_selection_id.text()
        self.stop, self.typed_ids = self.check_input_surface_id(lineEdit_selection_id)
        if self.stop:
            self.lineEdit_selection_id.setFocus()
            return

        # self.project.remove_acoustic_pressure_table_files(self.typed_ids)
        # self.project.reset_compressor_info_by_node(self.typed_ids)

        list_table_names = self.get_list_table_names_from_selected_nodes(self.typed_ids)
        if self.lineEdit_load_table_path != "":
            for node_id in self.typed_ids:
                if self.filename_volume_velocity is None:
                    self.imported_values, self.filename_volume_velocity = self.load_table(  self.lineEdit_load_table_path, 
                                                                                            direct_load=True  )
                if self.imported_values is None:
                    return
                else:
                    self.volume_velocity, self.basename_volume_velocity = self.save_table_file( node_id, 
                                                                                                self.imported_values, 
                                                                                                self.filename_volume_velocity )
                    if self.basename_volume_velocity in list_table_names:
                        list_table_names.remove(self.basename_volume_velocity)

                    key_avg = int(self.checkBox_averaged_constant_values.isChecked())
                    data = {"entity_type" : "surface",
                            "entity_ids" : self.typed_ids,
                            "values" : self.volume_velocity,
                            "averaged" : key_avg,
                            "table_name" : self.basename_volume_velocity}

            self.project.set_volume_velocity(data)

            # self.process_table_file_removal(list_table_names)
            print(f"[Set Volume Velocity] - defined at node(s) {self.typed_ids}")   
            self.close()
        else:    
            title = "Additional inputs required"
            message = "You must inform at least one volume velocity\n" 
            message += "table path before confirming the input!"
            PrintMessageInput([title, message, window_title_1])
            self.lineEdit_load_table_path.setFocus()


    def get_list_table_names_from_selected_nodes(self, list_node_ids):
        list_table_names = []
        for node_id in list_node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.volume_velocity_table_name is not None:
                table_name = node.volume_velocity_table_name
                if table_name not in list_table_names:
                    list_table_names.append(table_name)
        return list_table_names


    def text_label(self, value):
        text = ""
        if isinstance(value, complex):
            value_label = str(value)
        elif isinstance(value, np.ndarray):
            value_label = 'Table'
        text = "{}".format(value_label)
        return text


    def on_click_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))


    def on_doubleclick_item(self, item):
        self.lineEdit_selection_id.setText(item.text(0))
        self.check_remove_bc_from_node()


    def check_remove_bc_from_node(self):
        if self.lineEdit_selection_id.text() != "":
            picked_id = int(self.lineEdit_selection_id.text())       
            if picked_id in self.properties.surfaces_with_volume_velocity.keys():
                section_key = f"surface - {picked_id}"           
                key_strings = ["volume velocity", "averaged", "table name"]
                message = f"The volume velocity attributed to the {picked_id} surface has been removed."
                self.project.file.remove_bc_from_file(section_key, self.acoustic_bc_info_path, key_strings, message)
                #TODO: remove imported volume velocity tables
                # list_table_names = self.get_list_table_names_from_selected_nodes([picked_id])
                # self.process_table_file_removal(list_table_names)
                self.properties.remove_volume_velocity(picked_id)
                self.load_info()
                self.lineEdit_selection_id.setText("")
                # self.close()


    def process_table_file_removal(self, list_table_names):
        if list_table_names != []:
            for table_name in list_table_names:
                self.project.remove_acoustic_table_files_from_folder(table_name, "volume_velocity_files")    


    def check_reset(self):
        if len(self.properties.surfaces_with_volume_velocity) > 0:
 
            title = f"Resetting of all applied volume velocities"
            message = "Do you really want to remove the volume velocity applied to the following surface(s)?\n\n"
            entity_ids = list(self.properties.surfaces_with_volume_velocity.keys())
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
                surfaces_ids = self.properties.surfaces_with_volume_velocity.keys()
                for _id in surfaces_ids:
                    key_strings = ["volume velocity", "averaged", "table name"]
                    sections.append(f"surface - {_id}")
                    table_name = None
                    if table_name is not None:
                        if table_name not in _list_table_names:
                            _list_table_names.append(table_name)
                self.project.file.remove_bc_from_file(sections, self.acoustic_bc_info_path, key_strings, None)
                self.properties.reset_volume_velocity()

                #TODO: remove imported tables
                # self.process_table_file_removal(_list_table_names)

                title = "Volume velocity resetting process complete"
                message = "All volume velocity applied to the acoustic " 
                message += "model have been removed from the model."
                PrintMessageInput([title, message, window_title_2])

                self.close()


    def reset_input_fields(self):
        self.lineEdit_real_value.setText("")
        self.lineEdit_imag_value.setText("")
        self.lineEdit_load_table_path.setText("")


    def update(self):
        # This method should be called to update qt widgets whenever some entity has been clicked 
        return


    def writeNodes(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        if self.current_tab != 2:
            self.lineEdit_selection_id.setText(text[:-2])


    def update_tabs_visibility(self):
        if len(self.properties.surfaces_with_volume_velocity) == 0:
            self.tabWidget_volume_velocity.setCurrentWidget(self.tab_constant_values)
            self.tab_remove.setDisabled(True)
        else:
            self.tab_remove.setDisabled(False)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_volume_velocity.currentIndex()==0:
                self.check_constant_values()
            if self.tabWidget_volume_velocity.currentIndex()==1:
                self.check_table_values()
        elif event.key() == Qt.Key_Delete:
            if self.tabWidget_volume_velocity.currentIndex()==2:
                self.check_remove_bc_from_node()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            return

    
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