from PySide6.QtWidgets import QFileDialog

from vibra import app
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput

from utils.utils import get_new_path
from pathlib import Path

import os
import numpy as np

error_title = "Error"
warning_title = "Warning"

class RefpropInterface:
    def __init__(self, *args, **kwargs):
        super().__init__()

        self._initialize()

    def _initialize(self):
        self.refprop = None

        # self.isentropic_label = "ISENK"   # isentropic exponent (real gas)
        self.isentropic_label = "CP/CV"     # isentropic expansion coefficient (ideal gas)

        self.map_properties = { "D" : "fluid_density",
                                "CP" : "specific_heat_Cp",
                                "CV" : "specific_heat_Cv",
                                self.isentropic_label : "isentropic_exponent",
                                "W" : "speed_of_sound",
                                "VIS" : "dynamic_viscosity",
                                "TCX" : "thermal_conductivity",
                                "PRANDTL" : "Prandtl_number",
                                "TD" : "thermal_diffusivity",
                                "KV" : "kinematic_viscosity",
                                "M" : "molar_mass",
                                "BS" : "adiabatic_bulk_modulus",
                                "KKT" : "isothermal_bulk_modulus",
                                "Z" : "compressibility_factor"  }

    def get_refprop_path(self) -> None | str:

        REFPROP_PATH = os.environ.get('RPPREFIX')
        if REFPROP_PATH is None:
            REFPROP_PATH = app().config.get_refprop_path_from_file()
        
        if isinstance(REFPROP_PATH, str):
            if os.path.exists(REFPROP_PATH):
                return REFPROP_PATH

        user_path = os.path.expanduser("~")
        title = 'Choose the REFPROP folder'
        REFPROP_PATH = QFileDialog.getExistingDirectory(None, title, user_path)

        if REFPROP_PATH == "":
            return None

        if not os.path.exists(REFPROP_PATH):
            return None
    
        if os.path.basename(REFPROP_PATH) in ["REFPROP", "Refprop", "refprop"]:
            app().config.write_refprop_path_in_file(REFPROP_PATH)
            return REFPROP_PATH

        else:
            title = "Invalid folder selected"
            message = f"The selected folder path {REFPROP_PATH} does not match with the REFPROP installation folder. "
            message += "As suggestion, try to find the default installation folder in 'C:/Program Files (x86)/REFPROP'. "
            message += "You should select the valid REFPROP installation folder to proceed."
            PrintMessageInput([error_title, title, message])
            return None

    def get_REFPROP_version(self):
        return self.refprop.RPVersion()

    def check_refprop_version(self):
        version = self.refprop.RPVersion()
        if version[:3] != "10.":
            title = "Invalid REFPROP version"
            message = "The installed REFPROP version is incompatible with the Vibra requirements. It is recommended "
            message += "to install a newer REFPROP version to maintain the compatibility with the application.\n\n"
            message += f"Current version: {version}\n"
            message +=  "Required version: >= 10.0"
            PrintMessageInput([warning_title, title, message])
            return True

    def initialize_REFPROP(self):
        try:
            
            from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

            refProp_path = self.get_refprop_path()
            if refProp_path is None:
                return True

            elif not Path(refProp_path).exists():
                title = "REFPROP installation not detected"
                message = "Dear user, the REFPROP application files were not found in the computer's default paths. "
                message += "Please, install the REFPROP on your computer to enable the set-up of the fluids mixture."
                PrintMessageInput([error_title, title, message])
                return True

            self.refprop = REFPROPFunctionLibrary(refProp_path)
            if self.check_refprop_version():
                return True

            self.refprop.SETPATHdll(refProp_path)
            refProp_fluids_path = get_new_path(refProp_path, "FLUIDS")
            list_files = os.listdir(refProp_fluids_path)

            self.refprop_fluids = dict()
            self.fluid_file_to_final_name = dict()

            for fluid_file in list_files:
                if ".BNC" not in fluid_file:
                    filepath = get_new_path(refProp_fluids_path, fluid_file)
                    
                    f = open(filepath, 'r')
                    line_0 = f.readline()
                    line_1 = f.readline()
                    line_2 = f.readline()

                    f.close()
                    short_name = line_0.split("!")[0]
                    full_name = line_2.split("!")[0]
            
                    letter = " "
                    while letter == " ":
                        short_name = short_name[:-1]
                        letter = short_name[-1]
                        
                    letter = " "
                    while letter == " ":
                        full_name = full_name[:-1]
                        letter = full_name[-1]

                    final_name = short_name if short_name == full_name else f"{short_name} ({full_name})"
                    self.refprop_fluids[final_name] = [fluid_file, short_name, full_name]
                    self.fluid_file_to_final_name[fluid_file] = final_name

        except Exception as error_log:
            title = "Error while loading REFPROP"
            message = "An error has been reached while trying to load REFPROP data. If the REFPROP module has already been "
            message += "installed we recommend running the 'pip install ctREFPROP' command at the terminal to install the "
            message += "necessary libraries.\n\n"
            message += f"Details: {str(error_log)}"
            PrintMessageInput([error_title, title, message])
            return True
        
    def get_specific_fluid_property(self, **kwargs):

        fluids_string = kwargs.get("fluids_string", "")
        molar_fractions = kwargs.get("molar_fractions", list())
        property_key = kwargs.get("property_key")
        temperature_K = kwargs.get("temperature_K")
        pressure_Pa = kwargs.get("pressure_Pa")
        state_properties = kwargs.get("state_properties", "TP")
        
        units = self.refprop.GETENUMdll(0, "MASS BASE SI").iEnum
        read = self.refprop.REFPROPdll( 
                                        fluids_string, 
                                        state_properties, 
                                        property_key, 
                                        units, 
                                        0, 
                                        0, 
                                        temperature_K, 
                                        pressure_Pa, 
                                        molar_fractions
                                        )

        if read.herr:
            return None, read.herr

        if property_key == "M":
            fluid_property = 1000*read.Output[0]   
        else:
            fluid_property = read.Output[0]

        return fluid_property, None
    
    def compute_fluid_properties_for_multiple_state_properties(self, **kwargs):

        fluid_name = kwargs.get("fluid_name", "")
        fluids_string = kwargs.get("fluids_string", "")
        molar_fractions = kwargs.get("molar_fractions", list())
        state_properties = kwargs.get("state_properties", list())

        if not state_properties:
            return None, None

        fluid_properties_for_all_states = dict()
        temperatures_K, pressures_Pa, rgb_colors = state_properties

        for j, temperature_K in enumerate(temperatures_K):
            fluid_properties = dict()
            pressure_Pa = pressures_Pa[j]

            for prop_key, prop_label in self.map_properties.items():
                fluid_property, errors = self.get_specific_fluid_property(
                                                                          fluids_string = fluids_string,
                                                                          molar_fractions = molar_fractions,
                                                                          property_key = prop_key,
                                                                          temperature_K = temperature_K,
                                                                          pressure_Pa = pressure_Pa,
                                                                          )

                if errors:
                    print(errors)
                    return None, errors

                fluid_properties[prop_label] = fluid_property

            if fluid_name != "":
                fluid_properties["name"] = f"{fluid_name} ({j+1})"

            fluid_properties["temperature"] = float(temperature_K)
            fluid_properties["pressure"] = float(pressure_Pa)
            fluid_properties["color"] = rgb_colors[j]

            fluid_properties_for_all_states[j+1] = {
                                                    "fluid_string" : fluids_string,
                                                    "molar_fractions" : molar_fractions,
                                                    "fluid_properties" : fluid_properties,
                                                    }

        return fluid_properties_for_all_states, None

    def get_red_blue_color_scale(self, N_fluids: int):
        x_values = np.linspace(255, 0, N_fluids)
        rgb_colors = [[int(x), 0, int(255-x)] for x in x_values]
        return rgb_colors

    def get_state_properties(self, **kwargs):

        temperatures_K = kwargs.get("temperatures_K")
        pressures_Pa = kwargs.get("pressures_Pa")
        N_fluids = kwargs.get("N_fluids", 10)
        distribution_type = kwargs.get("distribution_type", "linear")

        if distribution_type == "linear":
            if len(temperatures_K) != 2:
                return

            if len(pressures_Pa) != 2:
                return

            T_start, T_end = temperatures_K
            P_start, P_end = pressures_Pa

            temperatures = np.linspace(T_start, T_end, N_fluids)
            pressures = np.linspace(P_start, P_end, N_fluids)
            colors = self.get_red_blue_color_scale(N_fluids)

            # print(np.array([temperatures, pressures]).T)
            return (temperatures, pressures, colors)

        return None          