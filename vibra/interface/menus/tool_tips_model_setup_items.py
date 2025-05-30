tool_tips: dict[str, str] = dict()

tool_tips["material"] = (
    # "### Set material\n\n"
    "Configure materials to be added to a structure.\n\n"
    "Materials have properties such as:\n\n"
    "- **Density**: The mass per unit volume of the material.\n"
    "- **Elasticity Modulus**: The stiffness of the material when it is stretched or compressed.\n"
    "- **Poisson's Ratio**: A measure of the proportional decrease in one dimension when the material is stretched or compressed in another dimension.\n"
    "- **Thermal Expansion Coefficient**: A measure of the rate at which the material expands or contracts in response to temperature changes.\n"
    "- **Color**: A visual representation of the material in the 3D model.\n"
)

tool_tips["fluid"] = (
    # "### Set fluid\n\n"
    "Configure fluids to be added to the model.\n\n"
    "Fluids can be configured by property manually or combined using Refprop.\n\n"
    "Fluids have properties such as:\n"
    "- **Temperature**: The temperature of the fluid.\n"
    "- **Pressure**: The pressure of the fluid.\n"
    "- **Density**: The density of the fluid.\n"
    "- **Speed of sound**: The speed of sound in the fluid.\n"
    "- **Isentropic expoent**: The isentropic exponent of the fluid.\n"
    "- **Thermal conductivity**: The thermal conductivity of the fluid.\n"
    "- **Specific heat**: The specific heat of the fluid.\n"
    "- **Dynamic viscosity**: The dynamic viscosity of the fluid.\n"
    "- **Molar mass**: The molar mass of the fluid.\n"
    "- **Color**: A visual representation of the fluid in the 3D model.\n"
)

tool_tips["mesh_setup"] = (
    # "### Set mesh\n\n"
    "Create and refine a 3D mesh.\n\n"
    "Meshes can be of the following types:\n"
    "- tetrahedron\n"
    "- tetrahedron quadratic\n"
    "- hexahedron\n"
    "- hexahedron quadratic"
)

tool_tips["degrees_of_freedom_decoupling"] = (
    "A technique used to reduce computational complexity by separating or simplifying the interactions "
    "between different degrees of freedom (DOFs) in a system.\n\n"
    "In acoustics and multiphysics models, DOFs decoupling allows the treatment of coupled variables—"
    "such as pressure, velocity, or structural displacements—as independent or weakly coupled, depending "
    "on assumptions or physical constraints.\n\n"
    "This approach can significantly improve solver efficiency, stability, and convergence, especially "
    "in large-scale or frequency-domain problems.\n\n"
    "Common applications include modal analysis, simplified impedance models, and weak coupling between "
    "fluid and structural domains."
)

tool_tips["surface_thickness"] = (
    # "### Set surface thickness\n\n"
    "Defines the thickness of a region.\n\n"
    "This is used to indicate that a portion of the model is a shell."
)

tool_tips["prescribed_dofs"] = (
    # "### Set prescribed DOFs\n\n"
    "Configure previously known degrees of freedom.\n\n"
    "This option can be used to indicate that some region can not move by setting 0 to all degrees of freedom."
)

tool_tips["nodal_loads"] = (
    # "### Set nodal loads\n\n"
    "Apply a force in the structure.\n\n"
    "???"
    )

tool_tips["distributed_loads"] = (
    # "### Set Distributed Loads\n\n"
    "Apply forces distributed over a surface or along a line.\n\n"
    "This type of load is used to model pressure or forces that act over an extended area or length."
    )

tool_tips["normal_pressure_load"] = (
    # "### Set Normal Pressure Load\n\n"
    "Apply a pressure load that acts normal to the surface.\n\n"
    "This type of load is typically used to simulate forces exerted on a surface, such as wind pressure or fluid pressure."
    )   

tool_tips["acoustic_pressure"] = (
    # "### Set Acoustic Pressure\n\n"
    "Apply an acoustic pressure load to the structure.\n\n"
    "This load simulates the effects of sound waves or other acoustic phenomena acting on the structure."
    )

tool_tips["mass_flow_rate"] = (
    # "### Mass Flow Rate (Acoustics)\n\n"
    "The rate of mass flow associated with the oscillatory motion of particles in the medium.\n\n"
    "It represents the amount of mass passing through a surface per unit time due to acoustic "
    "fluctuations. Mass flow rate is directly related to particle velocity and the medium's density.\n\n"
    "It is a fundamental quantity in acoustic network elements such as ducts, tubes, and dissipative "
    "components, and is typically expressed in kg/s."
    )

tool_tips["surface_velocity"] = (
    # "### Set Surface Velocity\n\n"
    "Define the velocity of a surface in the model.\n\n"
    "This type of load is used to specify the speed at which a surface is moving, which can be important for dynamic simulations."
    )

tool_tips["anechoic_termination"] = (
    # "### Set Anechoic Termination\n\n"
    "Define an anechoic termination condition for the model.\n\n"
    "This condition is used to simulate the behavior of a surface or boundary that absorbs sound waves without reflecting them."
)

tool_tips["absorption_surface"] = (
    # "### Absorption Surface\n\n"
    "A surface that dissipates acoustic energy by converting sound energy into heat through friction, "
    "viscous effects, or material properties.\n\n"
    "It is characterized by its sound absorption coefficient, which defines how much incident sound energy "
    "is absorbed versus reflected. Absorption surfaces are essential in controlling reverberation, echoes, "
    "and overall acoustic comfort in spaces.\n\n"
    "Common examples include porous materials, foam panels, fabric walls, and acoustic diffusers."
    )

tool_tips["specific_impedance"] = (
    # "### Set Specific Impedance\n\n"
    "Define the specific impedance at a surface or boundary.\n\n"
    "Specific impedance characterizes the relationship between pressure and particle velocity at a surface, important for acoustic simulations."
    )

tool_tips["transfer_impedance"] = (
    "A complex acoustic property that relates the pressure difference across an element to the resulting "
    "acoustic volume velocity or mass flow rate.\n\n"
    "It characterizes how an acoustic component impedes the transmission of sound between two points, "
    "accounting for both resistive (energy dissipation) and reactive (inertial and compliance) effects.\n\n"
    "Commonly used to model elements like perforated plates, meshes, membranes, or porous materials, "
    "where the relationship between pressure drop and particle motion is significant.\n\n"
    "Typical units are Pa·s/m³ or equivalent, depending on whether it is referenced to volume velocity "
    "or mass flow rate."
)

tool_tips["dissipation_model"] = (
    # "### Set Dissipation Model\n\n"
    "Define the dissipation model for the simulation.\n\n"
    "This model is used to simulate energy loss due to various physical processes, such as friction or heat generation, within the system."
    )

tool_tips["porous_material_model"] = (
    # "### Set Porous Material Model\n\n"
    "Define the porous material model for the simulation.\n\n"
    "This model is used to simulate materials with a porous structure, where air or fluid can flow through the material, affecting its behavior."
    )

tool_tips["viscous-thermal_loss_model"] = (
    # "### Set Viscous-thermal Loss Model\n\n"
    "Define the viscous-thermal loss model for the simulation.\n\n"
    "This model is used to simulate heat loss due to viscous friction in the system."
    )

tool_tips["perforated_plate_model"] = (
    # "### Set Perforated Plate Model\n\n"
    "Define the perforated plate model for the simulation.\n\n"
    "This model is used to simulate materials with perforations, where air or fluid can flow through the material, affecting its behavior."
    )

tool_tips["acoustic_properties_gradient"] = (
    # "### Set Acoustic Properties Gradient\n\n"
    "Define the gradient of acoustic properties in the model.\n\n"
    "This option allows you to vary the acoustic properties such as density, speed of sound, or impedance across the domain, enabling more realistic simulations in heterogeneous media."
    )

tool_tips["viscous_thermal_model"] = (
    "A model that accounts for energy losses due to viscous friction and thermal conduction "
    "in narrow channels, porous materials, or boundary layers of acoustic systems.\n\n"
    "These losses occur when oscillating particles interact with surfaces, causing shear stress (viscous loss) "
    "and heat exchange between the fluid and boundaries (thermal loss).\n\n"
    "Including viscous and thermal losses is essential for accurately modeling high-frequency behavior, "
    "small geometries, and components like perforated plates, capillaries, and porous absorbers.\n\n"
    "This model improves the realism of acoustic simulations, especially in systems where dissipation is significant."
    )

tool_tips["reciprocating_compressor_excitation"] = (
    # "### Add Reciprocating Compressor Excitation\n\n"
    "Add excitation from a reciprocating compressor to the model.\n\n"
    "This excitation simulates the dynamic forces generated by a reciprocating compressor, which can be important for analyzing vibrations or acoustic emissions in machinery."
    )

tool_tips["acoustic_transfer_element_setup"] = (
    # "### Process Acoustic Transfer Element Data\n\n"
    "Process the data related to acoustic transfer elements in the simulation.\n\n"
    "This step is used to calculate and process the acoustic transfer functions between different parts of the model, enabling the analysis of sound propagation and interactions in complex systems."
    )