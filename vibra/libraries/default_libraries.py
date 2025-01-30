import configparser

from vibra import app

def default_material_library():
    config = configparser.ConfigParser()

    config["Steel"] = {
        "name" : "Steel",
        "identifier" : 1,
        "color" : "[170,170,170]",  # Light Gray
        "material_density" : 7860,
        "young_modulus" : 210,
        "poisson" : 0.3,
        "thermal_expansion_coefficient" : 1.2e-5,
    }

    config["Stainless_steel"] = {
        "name" : "Stainless_steel",
        "identifier" : 2,
        "color" : "[126,46,31]",  # Wood color
        "material_density" : 7750,
        "young_modulus" : 193,
        "poisson" : 0.31,
        "thermal_expansion_coefficient" : 1.7e-5,
    }

    config["Ni-Co-Cr_alloy"] = {
        "name" : "Ni-Co-Cr_alloy",
        "identifier" : 3,
        "color" : "[0,255,255]",  # Cyan
        "material_density" : 8220,
        "young_modulus" : 212,
        "poisson" : 0.315,
        "thermal_expansion_coefficient" : 1.2e-5,
    }

    config["Cast_iron"] = {
        "name" : "Cast_iron",
        "identifier" : 4,
        "color" : "[50,50,50]",  # Dark Grey
        "material_density" : 7200,
        "young_modulus" : 110,
        "poisson" : 0.28,
        "thermal_expansion_coefficient" : 1.1e-5,
    }

    config["Aluminum"] = {
        "name" : "Aluminum",
        "identifier" : 5,
        "color" : "[255,255,255]",  # White
        "material_density" : 2770,
        "young_modulus" : 71,
        "poisson" : 0.333,
        "thermal_expansion_coefficient" : 2.3e-5,
    }

    config["Brass"] = {
        "name" : "Brass",
        "identifier" : 6,
        "color" : "[181,166,66]",  # Brass color
        "material_density" : 8150,
        "young_modulus" : 96,
        "poisson" : 0.345,
        "thermal_expansion_coefficient" : 1.9e-5,
    }

    app().file.write_material_library_in_file(config)


def default_fluid_library():

    # Reference: RefProp v10.0

    config = configparser.ConfigParser()

    config["1"] = {
        "name" : "Air",
        "identifier" : 1,
        "color" : "[255,170,127]",  # Blue
        "fluid_density" : 1.204263,
        "speed_of_sound" : 343.395034,
        "isentropic_exponent" : 1.401985,
        "thermal_conductivity" : 0.025503,
        "specific_heat_Cp" : 1006.400178,
        "dynamic_viscosity" : float(1.8247e-5),
        "temperature" : 293.15,
        "pressure" : 101325,
        "molar_mass" : 28.958601
    }

    config["2"] = {
        "name" : "Air",
        "identifier" : 2,
        "color" : "[255,85,255]",  # Blue
        "fluid_density" : 0.945625,
        "speed_of_sound" : 387.054839,
        "isentropic_exponent" : 1.397945,
        "thermal_conductivity" : 0.031167,
        "specific_heat_Cp" : 1011.477011,
        "dynamic_viscosity" : float(2.1948e-5),
        "temperature" : 373.15,
        "pressure" : 101325,
        "molar_mass" : 28.958601
    }

    config["3"] = {
        "name" : "Hydrogen",
        "identifier" : 3,
        "color" : "[116,200,255]",  # Magenta
        "fluid_density" : 0.077173,
        "speed_of_sound" : 1357.568075,
        "isentropic_exponent" : 1.402898,
        "thermal_conductivity" : 0.19527,
        "specific_heat_Cp" : 14367.266634,
        "dynamic_viscosity" : float(9.3092e-6),
        "temperature" : 318.15,
        "pressure" : 101325,
        "molar_mass" : 2.01588
    }

    config["4"] = {
        "name" : "Hydrogen",
        "identifier" : 4,
        "color" : "[255,102,102]",  # Magenta
        "fluid_density" : 0.767785,
        "speed_of_sound" : 1365.114753,
        "isentropic_exponent" : 1.404047,
        "thermal_conductivity" : 0.1964,
        "specific_heat_Cp" : 14388.94084,
        "dynamic_viscosity" : float(9.3137e-6),
        "temperature" : 318.15,
        "pressure" : 1013250,
        "molar_mass" : 2.01588
    }

    config["5"] = {
        "name" : "Methane",
        "identifier" : 5,
        "color" : "[103,255,164]",  # Cyan
        "fluid_density" : 0.66816,
        "speed_of_sound" : 445.010623,
        "isentropic_exponent" : 1.308321,
        "thermal_conductivity" : 0.033271,
        "specific_heat_Cp" : 2220.597802,
        "dynamic_viscosity" : float(1.0914e-5),
        "temperature" : 293.15,
        "pressure" : 101325,
        "molar_mass" : 16.0428
    }

    app().file.write_fluid_library_in_file(config)