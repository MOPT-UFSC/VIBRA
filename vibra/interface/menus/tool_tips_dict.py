tool_tips: dict[str, str] = dict()

tool_tips["material"] = (
    "Add/edit the materials from the materials library or set "
    "a material to selected entities."
    )

tool_tips["fluid"] = (
    "Add/edit the fluids from the fluids library or set "
    "a fluid to selected entities."
)

tool_tips["mesh_setup"] = (
    "Configure the mesher parameters to discretize the model domains and boundaries "
    "using solid, face, and line elements."
)

tool_tips["degrees_of_freedom_decoupling"] = (
    "This feature disconnects the nodes from connected volumes and modifies the "
    "connectivity from all geometric entities. As a consequence, both structural "
    "and acoustic degrees of freedom will be decoupled."
)

tool_tips["surface_thickness"] = (
    "Define the wall thickness of selected surfaces for face elements."
)

tool_tips["prescribed_dof"] = (
    "Define the known values for the structural degrees of freedom."
)

tool_tips["nodal_loads"] = (
    "Set equally distributed structural nodal loads for the selected entities."
    )

tool_tips["distributed_loads"] = (
    "Set distributed loads over selected surfaces or along lines."
    )

tool_tips["normal_pressure_load"] = (
    "Set distributed normal pressure loads over selected surfaces."
    )

tool_tips["acoustic_pressure"] = (
    "Create a boundary condition that prescribe an acoustic pressure at the boundary of the domain."
    )

tool_tips["mass_source"] = (
    "Add a mass source to a point, node, or over a line, surface, or volume."
    )

tool_tips["surface_velocity"] = (
    "Set a normal surface velocity in the selected surfaces."
    )

tool_tips["anechoic_termination"] = (
    "Define an anechoic termination (non-reflecting) boundary condition for the selected surface."
)

tool_tips["absorption_surface"] = (
    "Set a boundary condition that absorbs, in percentage, the incident sound energy."
    )

tool_tips["specific_impedance"] = (
    "Define a specific impedance (real or complex) at a boundary of the domain."
    )

tool_tips["transfer_impedance"] = (
    "Set an internal transfer impedance at an interface boundary between two domains."
)

tool_tips["perforated_plate_model"] = (
    "Set an internal perforated plate for the acoustic model to simulate the pressure drop "
    "across this component."
    )

tool_tips["propotional_damping"] = (
    "Configure the proportional damping factors for the acoustic model."
    )

tool_tips["porous_material_model"] = (
    "Set a domain as a porous material modeled in a homogenized way using a so-called equivalent "
    "fluid by Delany-Bazley, Delany-Bazley-Miki, JCA and JCAL model."
    )

tool_tips["viscous_thermal_model"] = (
    "Set an equivalent fluid model for viscous thermal boundary-layer induced loss in circular, "
    "rectangular, quadrangular or narrow slits ducts of constant cross section."
    )

tool_tips["reciprocating_compressor_excitation"] = (
    "Add an idealized reciprocating compressor excitation in the form of an equivalent surface velocity."
    )

tool_tips["acoustic_properties_gradient"] = (
    "Assign a gradient of acoustic properties to model properties variations along one defined axis."
    )

tool_tips["acoustic_transfer_element_setup"] = (
    "Use this feature to configure the surfaces where the acoustic transfer element will be computed."
    )