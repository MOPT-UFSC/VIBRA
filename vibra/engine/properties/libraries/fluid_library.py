from vibra.engine.properties.fluid import Fluid

from .property_library import PropertyLibrary


class FluidLibrary(PropertyLibrary[Fluid]): ...


def default_fluid_library() -> FluidLibrary:
    fluids = [
        Fluid(
            name="Air std",
            identifier=1,
            fluid_density=1.204263,
            speed_of_sound=343.395034,
            isentropic_exponent=1.401985,
            thermal_conductivity=0.025503,
            specific_heat_Cp=1006.400178,
            dynamic_viscosity=1.8247e-5,
            temperature=293.15,
            pressure=101325,
            molar_mass=28.958601,
            color=(255, 170, 127),  # Blue
        ),
        Fluid(
            name="Air 2",
            identifier=2,
            fluid_density=0.945625,
            speed_of_sound=387.054839,
            isentropic_exponent=1.397945,
            thermal_conductivity=0.031167,
            specific_heat_Cp=1011.477011,
            dynamic_viscosity=2.1948e-5,
            temperature=373.15,
            pressure=101325,
            molar_mass=28.958601,
            color=(255, 85, 255),  # Blue
        ),
        Fluid(
            name="Hydrogen",
            identifier=3,
            fluid_density=0.077173,
            speed_of_sound=1357.568075,
            isentropic_exponent=1.402898,
            thermal_conductivity=0.19527,
            specific_heat_Cp=14367.266634,
            dynamic_viscosity=9.3092e-6,
            temperature=318.15,
            pressure=101325,
            molar_mass=2.01588,
            color=(116, 200, 255),  # Magenta
        ),
        Fluid(
            name="Hydrogen",
            identifier=4,
            fluid_density=0.767785,
            speed_of_sound=1365.114753,
            isentropic_exponent=1.404047,
            thermal_conductivity=0.1964,
            specific_heat_Cp=14388.94084,
            dynamic_viscosity=9.3137e-6,
            temperature=318.15,
            pressure=1013250,
            molar_mass=2.01588,
            color=(255, 102, 102),  # Magenta
        ),
        Fluid(
            name="Methane",
            identifier=5,
            fluid_density=0.66816,
            speed_of_sound=445.010623,
            isentropic_exponent=1.308321,
            thermal_conductivity=0.033271,
            specific_heat_Cp=2220.597802,
            dynamic_viscosity=1.0914e-5,
            temperature=293.15,
            pressure=101325,
            molar_mass=16.0428,
            color=(103, 255, 164),  # Cyan
        ),
    ]

    fluid_library = FluidLibrary()
    fluid_library.extend(fluids)
    return fluid_library