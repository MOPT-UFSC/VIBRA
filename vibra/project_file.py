import configparser
import os
from pathlib import Path
from shutil import rmtree

import numpy as np

from vibra.interface.general.print_message_input import PrintMessageInput

class ProjectFile:
    def __init__(self):
        self._reset()
        self._set_default_filenames()
        self._set_default_foldernames()

    def _reset(self):
        self.project_path = Path("vibra")

    def _set_default_filenames(self):
        self.project_basename = "project.ini"
        self.fluid_library_filename = "fluid_library.dat"
        self.material_library_filename = "material_library.dat"
        self.acoustic_model_setup_filename = "acoustic_model_setup.dat"
        self.structural_model_setup_filename = "strucutral_model_setup.dat"

    def _set_default_foldernames(self):
        self.imported_data_folder_name = "imported_data"
        self.imported_data_folder_path = os.path.join(
            self.project_path, self.imported_data_folder_name
        )
        self.acoustic_imported_data_folder_path = os.path.join(
            self.imported_data_folder_path, "acoustic"
        )
        self.structural_imported_data_folder_path = os.path.join(
            self.imported_data_folder_path, "structural"
        )

    def add_frequency_in_file(self, data):
        temp_project_base_file_path = os.path.join(self.project_path, self.project_basename)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)

        config["Frequency setup"] = {}
        if "f_min" in data.keys():
            config["Frequency setup"]["frequency min"] = str(data["f_min"])
        if "f_max" in data.keys():
            config["Frequency setup"]["frequency max"] = str(data["f_max"])
        if "f_step" in data.keys():
            config["Frequency setup"]["frequency step"] = str(data["f_step"])

        self.write_data_in_file(temp_project_base_file_path, config)

    def add_dissipation_model_data_to_file(self, data):
        file_path = os.path.join(self.project_path, self.project_basename)
        config = configparser.ConfigParser()
        config.read(file_path)

        config["Acoustic dissipation model"] = {}
        section = config["Acoustic dissipation model"]

        section["model"] = data["model"]
        if data["model"] == "proportional damping":
            section["speed of sound complex factor"] = str(data["speed of sound factor"])
            section["fluid density complex factor"] = str(data["fluid density factor"])

        self.write_data_in_file(file_path, config)

    def add_structural_boundary_condition_to_file(self, data):
        file_path = os.path.join(self.project_path, self.structural_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        if "Contrained dofs" in sections:
            config["Constrained dofs"][data["entity_type"]] = data["entity_ids"]
            config["Constrained dofs"]["values"] = data["values"]
        else:
            config["Constrained dofs"] = {
                data["entity_type"]: data["entity_ids"],
                "values": data["values"],
            }

        self.write_data_in_file(file_path, config)

    def write_data_in_file(self, path, config):
        with open(path, "w") as config_file:
            config.write(config_file)

    def add_acoustic_pressure_to_file(self, data):
        file_path = os.path.join(self.project_path, self.acoustic_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        if "Acoustic pressure" in sections:
            config["Acoustic pressure"][data["entity_type"]] = data["entity_ids"]
            config["Acoustic pressure"]["values"] = data["values"]
        else:
            config["Acoustic pressure"] = {
                data["entity_type"]: data["entity_ids"],
                "values": data["values"],
            }

        self.write_data_in_file(file_path, config)

    def add_mass_flow_rate_to_file(self, data):
        file_path = os.path.join(self.project_path, self.acoustic_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        for entity_id in data["entity_ids"]:
            section = f"{data['entity_type']} - {entity_id}"
            if section in sections:
                config[section]["mass flow rate"] = str(data["values"])
                config[section]["averaged"] = str(data["averaged"])
            else:
                config[section] = {"mass flow rate": data["values"], "averaged": data["averaged"]}
            if "table_name" in data.keys():
                config[section]["table name"] = data["table_name"]

        self.write_data_in_file(file_path, config)

    def add_volume_velocity_to_file(self, data):
        file_path = os.path.join(self.project_path, self.acoustic_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        for entity_id in data["entity_ids"]:
            section = f"{data['entity_type']} - {entity_id}"
            if section in sections:
                config[section]["volume velocity"] = str(data["values"])
                config[section]["averaged"] = str(data["averaged"])
            else:
                config[section] = {"volume velocity": data["values"], "averaged": data["averaged"]}
            if "table_name" in data.keys():
                config[section]["table name"] = data["table_name"]

        self.write_data_in_file(file_path, config)

    def add_particle_velocity_to_file(self, data):
        file_path = os.path.join(self.project_path, self.acoustic_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        for entity_id in data["entity_ids"]:
            section = f"{data['entity_type']} - {entity_id}"
            if section in sections:
                config[section]["particle velocity"] = str(data["values"])
                config[section]["averaged"] = str(data["averaged"])
            else:
                config[section] = {
                    "particle velocity": data["values"],
                    "averaged": data["averaged"],
                }
            if "table_name" in data.keys():
                config[section]["table name"] = data["table_name"]

        self.write_data_in_file(file_path, config)

    def create_folders_structural(self, new_folder_name):
        """This method creates the 'imported_data', 'structural' and 'new_folder_name' folders
        in the project's directory if they do not exist yet.
        """
        if not os.path.exists(self.imported_data_folder_path):
            create_new_folder(self.project_path, "imported_data")
        if not os.path.exists(self.structural_imported_data_folder_path):
            create_new_folder(self.imported_data_folder_path, "structural")
        new_path = os.path.join(self.structural_imported_data_folder_path, new_folder_name)
        if not os.path.exists(new_path):
            create_new_folder(self.structural_imported_data_folder_path, new_folder_name)

    def create_folders_acoustic(self, new_folder_name):
        """This method creates the 'imported_data', 'acoustic' and 'new_folder_name' folders
        in the project's directory if they do not exist yet.
        """
        if not os.path.exists(self.imported_data_folder_path):
            create_new_folder(self.project_path, "imported_data")
        if not os.path.exists(self.acoustic_imported_data_folder_path):
            create_new_folder(self.imported_data_folder_path, "acoustic")
        new_path = os.path.join(self.acoustic_imported_data_folder_path, new_folder_name)
        if not os.path.exists(new_path):
            create_new_folder(self.acoustic_imported_data_folder_path, new_folder_name)

    def remove_bc_from_file(self, section_keys, path, keys_to_remove, message, equals_keys=False):
        try:
            if isinstance(section_keys, int):
                section_keys = [section_keys]

            if isinstance(section_keys, str):
                section_keys = [section_keys]

            bc_removed = False
            config = configparser.ConfigParser()
            config.read(path)
            sections = config.sections()

            for section_key in section_keys:
                if section_key in sections:
                    for key_to_remove in keys_to_remove:
                        if section_key in config.sections():
                            for key in config[section_key].keys():
                                if key_to_remove in key:
                                    if equals_keys:
                                        if key_to_remove != key:
                                            continue
                                    bc_removed = True
                                    config.remove_option(section=section_key, option=key)
                                    if list(config[section_key].keys()) == []:
                                        config.remove_section(section=section_key)

                if bc_removed:
                    if len(config.sections()) == 0:
                        if os.path.exists(path):
                            os.remove(path)
                    else:
                        with open(path, "w") as config_file:
                            config.write(config_file)

            if message is not None and bc_removed:
                PrintMessageInput(["Removal of selected boundary condition", message, "WARNING"])

        except Exception as log_error:
            PrintMessageInput(["Error while removing BC from file", str(log_error), "ERROR"])

    def remove_acoustic_table_files_from_folder(
        self, filename, folder_name, remove_empty_files=True
    ):
        _folder_path = os.path.join(self.acoustic_imported_data_folder_path, folder_name)
        if os.path.exists(_folder_path):
            list_filenames = os.listdir(_folder_path).copy()
            if filename in list_filenames:
                file_path = os.path.join(_folder_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

        if remove_empty_files:
            if os.path.exists(_folder_path):
                list_filenames = os.listdir(_folder_path).copy()
                if len(list_filenames) == 0:
                    rmtree(_folder_path)
                acoustic_folders = os.listdir(self.acoustic_imported_data_folder_path).copy()
                if len(acoustic_folders) == 0:
                    rmtree(self.acoustic_imported_data_folder_path)
                base_folders = os.listdir(self.imported_data_folder_path).copy()
                if len(base_folders) == 0:
                    rmtree(self.imported_data_folder_path)


def create_new_folder(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path