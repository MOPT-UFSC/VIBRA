tool_tips: dict[str, str] = dict()

tool_tips["material"] = (
    "Add/edit materials from the materials library or assign "
    "a material to selected entities."
)

tool_tips["fluid"] = (
    "Add/edit fluids from the fluids library or assign "
    "a fluid to selected entities."
)

tool_tips["mesh_setup"] = (
    "Configure the mesher parameters to discretize the model domains and boundaries "
    "using solid, surface, and line elements."
)

tool_tips["mesh_decoupling"] = (
    "Decouple the nodes of selected surfaces shared by at least two volumes, "
    "creating per-volume twin nodes at the interface. This is a permanent, "
    "mesh-level modification that takes effect when the mesh is generated "
    "(requires 'Merge nodes' in the volumes interface behavior)."
)

tool_tips["degrees_of_freedom_decoupling"] = (
    "This feature disconnects nodes from connected volumes and modifies the "
    "connectivity of all geometric entities. As a consequence, both structural "
    "and acoustic degrees of freedom will be decoupled."
)

tool_tips["surface_thickness"] = (
    "Define the wall thickness of selected surfaces for face elements."
)

tool_tips["prescribed_dof"] = (
    "Define the prescribed values for the structural degrees of freedom."
)

tool_tips["nodal_loads"] = (
    "Set equally distributed structural nodal loads on the selected entities."
)

tool_tips["distributed_loads"] = (
    "Set distributed loads on selected surfaces or along lines."
)

tool_tips["normal_pressure_load"] = (
    "Set distributed normal pressure loads on selected surfaces."
)

tool_tips["acoustic_pressure"] = (
    "Create a boundary condition that prescribes an acoustic pressure at the domain boundary."
)

tool_tips["mass_source"] = (
    "Add a mass source to a point, node, line, surface, or volume."
)

tool_tips["surface_velocity"] = (
    "Set a normal surface velocity on the selected surfaces."
)

tool_tips["anechoic_termination"] = (
    "Define an anechoic termination (non-reflecting) boundary condition for the selected surface."
)

tool_tips["absorption_surface"] = (
    "Set a boundary condition that absorbs a percentage of the incident sound energy."
)

tool_tips["specific_impedance"] = (
    "Define a specific impedance (real or complex) at a domain boundary."
)

tool_tips["transfer_impedance"] = (
    "Set an internal transfer impedance at an interface boundary between two domains."
)

tool_tips["perforated_plate_model"] = (
    "Set an internal perforated plate in the acoustic model to simulate the pressure drop "
    "across this component."
)

tool_tips["proportional_damping"] = (
    "Configure the proportional damping model for acoustic analyses."
)

tool_tips["porous_material_model"] = (
    "Set a domain as a porous material modeled in a homogenized way using an equivalent "
    "fluid model such as Delany-Bazley, Delany-Bazley-Miki, JCA, or JCAL."
)

tool_tips["viscous_thermal_model"] = (
    "Set an equivalent fluid model for viscous-thermal boundary-layer induced losses in circular, "
    "rectangular, quadrangular, or narrow slit ducts of constant cross-section."
)

tool_tips["reciprocating_compressor_excitation"] = (
    "Add an idealized reciprocating compressor excitation in the form of an equivalent surface velocity."
)

tool_tips["acoustic_properties_gradient"] = (
    "Assign a gradient of acoustic properties to model variations along a defined axis."
)

tool_tips["acoustic_transfer_element_setup"] = (
    "Configure the surfaces where the acoustic transfer element will be computed."
)