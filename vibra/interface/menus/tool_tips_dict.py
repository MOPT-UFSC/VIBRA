tool_tips: dict[str, str] = dict()

tool_tips["material"] = (
    "Use this feature to configure the materials from the materials library or set "
    "a material to selected entities."
    )

tool_tips["fluid"] = (
    "Use this feature to configure the fluids from the fluids library or set "
    "a fluid to selected entities."
)

tool_tips["mesh_setup"] = (
    "Use this feature to configure the mesher to discretize the model domains."
)

tool_tips["degrees_of_freedom_decoupling"] = (
    "Use this feature to disconnect the nodes from connected volumes and modifies "
    "the connectivity from all geometric entities. Both structural and acoustic "
    "and degrees of freedom will be increased and decoupled. "
)

tool_tips["surface_thickness"] = (
    "Use this feature to define the wall thickness of selected surfaces."
)

tool_tips["prescribed_dof"] = (
    "Use this feature to prescribed the known values for the structural degrees of freedom."
)

tool_tips["nodal_loads"] = (
    "Use this feature to assign equally distributed nodal loads."
    )

tool_tips["distributed_loads"] = (
    "Use this feature to assign distributed loads over a surface or along a line."
    )

tool_tips["normal_pressure_load"] = (
    "Use this featyre to distribute a normal pressure load over a surface surface."
    )   

tool_tips["acoustic_pressure"] = (
    "Use this feature to prescribed the known values for the acoustic pressure."
    )

tool_tips["mass_source"] = (
    "Use this feature to assign a mass source to a point, or over even a line, surface, or volume."
    )

tool_tips["surface_velocity"] = (
    "Define the velocity of a oscillating surface in the acoustic model."
    )

tool_tips["anechoic_termination"] = (
    "Define an anechoic termination (non-reflecting) boundary condition for the acoustic model."
)

tool_tips["absorption_surface"] = (
    "Use this feature to configure an absorption equivalent surface through the sound absorption coefficient."
    )

tool_tips["specific_impedance"] = (
    "Use this feature to assign a specific impedance to a surface."
    )

tool_tips["transfer_impedance"] = (
    "Use this feature to define an internal transfer impedance for the acoustic model."
)

tool_tips["perforated_plate_model"] = (
    "Use this feature to configure the internal perforated plate for the acoustic model."
    )

tool_tips["propotional_damping"] = (
    "Use this feature to configure the proportional damping for the acoustic model."
    )

tool_tips["porous_material_model"] = (
    "Use this feature to configure the porous material dissipation models for the acoustic model."
    )

tool_tips["viscous_thermal_model"] = (
    "Use this feature to enable the viscous-thermal losses for the acoustic model."
    )

tool_tips["reciprocating_compressor_excitation"] = (
    "Use this feature to add an equivalent reciprocating compressor excitation for the acoustic model."
    )

tool_tips["acoustic_transfer_element_setup"] = (
    "Use this feature to configure the surfaces where the acoustic transfer element will be computed."
    )

tool_tips["acoustic_properties_gradient"] = (
    "Use this feature to assign the gradient of acoustic properties "
    "to model properties variations along one defined axis."
    )