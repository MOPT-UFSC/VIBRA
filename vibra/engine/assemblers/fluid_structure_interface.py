
from collections import defaultdict

import numpy as np

from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class FluidStructureInterface:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()


    def reset(self):
        self.model_domains = defaultdict(list)
        self.nodes_per_domain = defaultdict(list)
        self.fluid_structure_interfaces = {}


    @property
    def mesh(self):
        return self.model.mesh


    def map_model_domains(self):
        self.model_domains.clear()
        for vol_id in self.mesh.elements_from_volume:

            fluid = self.properties._get_property("fluid", volume=vol_id)
            if isinstance(fluid, Fluid):
                self.model_domains["acoustic"].append(vol_id)
                continue

            material = self.properties._get_property("material", volume=vol_id)
            if isinstance(material, Material):
                self.model_domains["structural"].append(vol_id)

        self.fluid_structure_interfaces.clear()
        for surface_id, vol_ids in self.mesh.volumes_from_surface.items():
            if len(vol_ids) == 1:
                continue

            acoustic_volumes = self.model_domains.get("acoustic", [])
            structural_volumes = self.model_domains.get("structural", [])

            vol_a, vol_b = vol_ids
            if vol_a in acoustic_volumes and vol_b in structural_volumes:
                fluid_volume = vol_a
                structure_volume = vol_b

            elif vol_b in acoustic_volumes and vol_a in structural_volumes:
                fluid_volume = vol_b
                structure_volume = vol_a

            else:
                continue

            self.fluid_structure_interfaces[surface_id] = {
                "fluid_volume" : fluid_volume,
                "structure_volume" : structure_volume,
                }

    def map_nodes_domain(self):
        self.nodes_per_domain.clear()
        for domain, vol_ids in self.model_domains.items():
            rows = self.mesh.solids_connectivity[:, 1] == vol_ids
            self.nodes_per_domain[domain] = np.unique(self.mesh.solids_connectivity[rows, 4:].flatten())
