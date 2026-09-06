

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from vibra.engine.model import Model


class ModelSelectionTools:
    def __init__(self, model: "Model"):

        self.model = model

    @property
    def mesh(self):
        return self.model.mesh

    @property
    def domains_processor(self):
        return self.model.domains_processor

    def filter_selected_entities_based_on_domain(self, selected_ids: list[int] | np.ndarray, selection_label: str, domain: str):
        """
        This method filters the selected entities from the available ones for a specific domain.

        Parameters
        ----------
        selected_ids: list or np.ndarray
            A list or an array with the selected entities IDs.

        selection_label: str
            The selection label type (surface, lines, points or nodes).

        domain: str
            The domain label (acoustic or structural).

        Return
        ------
        filtered_ids: list
            A list with the filtered entities IDs accoring with the 
            available ones for a specific domain.

        """

        match selection_label:
            case "volumes":
                all_ids = self.domains_processor.volumes_of_domain.get(domain, [])
            case "surfaces":
                all_ids = self.domains_processor.surfaces_of_domain.get(domain, [])
            case "lines":
                all_ids = self.domains_processor.lines_of_domain.get(domain, [])
            case "points":
                all_ids = self.domains_processor.points_of_domain.get(domain, [])
            case "nodes":
                all_ids = self.domains_processor.nodes_of_domain.get(domain, [])
            case _:
                return []

        filtered_ids = [int(_id) for _id in np.intersect1d(all_ids, selected_ids)]

        return filtered_ids

    def check_selected_ids(self, input_ids: str | int | Iterable, selection_label: str, domain: str = "both", single_id: bool = False):
        """
        This method checks and filters the selected IDs based on the available ones for a specific domain.

            Parameters
        ----------
        input_ids: list or np.ndarray
            A list or an array with the selected entities IDs.

        selection_label: str
            The selection label type (surface, lines, points or nodes).

        domain: str, optional (default=both)
            The domain label (acoustic or structural).

        Return
        ------
        filtered_ids: list
            A list with the filtered entities IDs accoring with the 
            available ones for a specific domain.

        """
        
        try:

            all_ids = []
            selected_ids = check_input_values(input_ids)

            match selection_label:
                case "nodes":
                    all_ids = list(self.mesh.nodal_coordinates[:, 0])

                case "face_elements":
                    all_ids = list(self.mesh.faces_connectivity[:, 0])

                case "solid_elements":
                    all_ids = list(self.mesh.solids_connectivity[:, 0])

                case "points":
                    all_ids = self.mesh.all_point_ids()
                    
                case "lines":
                    all_ids = self.mesh.all_line_ids()

                case "surfaces":
                    all_ids = self.mesh.all_surface_ids()

                case "volumes":
                    all_ids = self.mesh.all_volume_ids()

                case _:
                    return None, None

            message = ""
            if len(selected_ids) == 0:
                message = "The Selected ID field is empty. Please, enter "
                message += "or select at least one valid IDs to proceed."

            else:
                if single_id and len(selected_ids) > 1:
                    message = "Only one Selected ID is allowed here."

                else:
                    try:
                        for _id in selected_ids:
                            if _id not in all_ids:
                                message = "The selected ID does not exist in the geometry. "
                                message += f"Please enter a valid ID between 1 and {len(all_ids)}."
                                break

                    except Exception as error_log:
                        message = "The selected ID must be an integer. "
                        message += f"Please enter a valid ID between 1 and {len(all_ids)}.\n\n"
                        message += str(error_log)

        except Exception as log_error:
            message = "Invalid input for the Selected ID.\n\n"
            message += str(log_error)

        # filter selected IDs based on a specific domain
        if domain != "both":
            filtered_ids = self.filter_selected_entities_based_on_domain(selected_ids, selection_label, domain)
            if not filtered_ids:
                message = f"The selected ID(s) {selected_ids} does not belong to the {domain} domain. Please, "
                message += "enter or selected at least one valid ID to proceed."

            selected_ids = filtered_ids.copy()

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Selection ID"
            error_data = [window_title, title, message]
            return None, error_data

        if single_id:
            return selected_ids[0], None

        return selected_ids, None

def check_input_values(input_ids: str | list | tuple | np.ndarray):

    if isinstance(input_ids, str):
        tokens = input_ids.replace(" ", "").split(",")
        return [int(_id) for _id in tokens]

    if isinstance(input_ids, int):
        return [input_ids]

    if isinstance(input_ids, Iterable):
        return [int(_id) for _id in input_ids]

    return []