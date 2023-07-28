import os
import configparser
import numpy as np
from pathlib import Path

# Essa classe se destina a controlar todos os arquivos do projeto

class ProjectFile:
    def __init__(self):
        self._reset()
        self._set_default_filenames()

    def _reset(self):
        self.project_path = Path("vibra")
        self.project_basename = ""

    def _set_default_filenames(self):
        self.fluid_library_filename = "fluid_library.dat"
        self.material_library_filename = "material_library.dat"
        self.acoustic_model_setup_filename = "acoustic_model_setup.dat"
        self.structural_model_setup_filename = "strucutral_model_setup.dat"

    def add_frequency_in_file(self, min_, max_, step_):
        min_ = str(min_)
        max_ = str(max_)
        step_ = str(step_)
        temp_project_base_file_path =  os.path.join(self.project_path, self.project_basename)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        # sections = config.sections()
        config["Frequency setup"] = {}
        config['Frequency setup']['frequency min'] = min_
        config['Frequency setup']['frequency max'] = max_
        config['Frequency setup']['frequency step'] = step_

        self.write_data_in_file(temp_project_base_file_path, config)

    def add_structural_boundary_condition_to_file(self, data):

        file_path = os.path.join(self.project_path, self.structural_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        if "Contrained dofs" in sections:
            config["Constrained dofs"][data["entity_type"]] = data["entity_ids"]
            config["Constrained dofs"]["values"] = data["values"]
        else:
            config["Constrained dofs"] = {  data["entity_type"] : data["entity_ids"],
                                            "values" : data["values"]  }

        self.write_data_in_file(file_path, config)

    def write_data_in_file(self, path, config):
        with open(path, 'w') as config_file:
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
            config["Acoustic pressure"] = { data["entity_type"] : data["entity_ids"],
                                            "values" : data["values"]  }

        self.write_data_in_file(file_path, config)


    def add_mass_flow_rate_to_file(self, data):

        file_path = os.path.join(self.project_path, self.acoustic_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        if "Mass flow rate" in sections:
            config["Mass flow rate"][data["entity_type"]] = data["entity_ids"]
            config["Mass flow rate"]["values"] = data["values"]
        else:
            config["Mass flow rate"] = { data["entity_type"] : data["entity_ids"],
                                            "values" : data["values"]  }

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
                config[section] = {"volume velocity" : data["values"],
                                    "averaged" : data["averaged"]}

        self.write_data_in_file(file_path, config)


    def add_particle_velocity_to_file(self, data):

        file_path = os.path.join(self.project_path, self.acoustic_model_setup_filename)
        config = configparser.ConfigParser()
        config.read(file_path)
        sections = config.sections()

        if "Particle velocity" in sections:
            config["Particle velocity"][data["entity_type"]] = data["entity_ids"]
            config["Particle velocity"]["values"] = data["values"]
        else:
            config["Particle velocity"] = { data["entity_type"] : data["entity_ids"],
                                            "values" : data["values"]  }

        self.write_data_in_file(file_path, config)