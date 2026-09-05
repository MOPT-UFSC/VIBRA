

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
                all_entities_ids = self.domains_processor.volumes_of_domain.get(domain, [])
            case "surfaces":
                all_entities_ids = self.domains_processor.surfaces_of_domain.get(domain, [])
            case "lines":
                all_entities_ids = self.domains_processor.lines_of_domain.get(domain, [])
            case "points":
                all_entities_ids = self.domains_processor.points_of_domain.get(domain, [])
            case "nodes":
                all_entities_ids = self.domains_processor.nodes_of_domain.get(domain, [])
            case _:
                return []

        filtered_ids = [int(_id) for _id in np.intersect1d(all_entities_ids, selected_ids)]

        return filtered_ids


    def check_selected_ids(
        self, input_ids: str | int | list[int] | np.ndarray, selection_label: str, domain: str = "both", single_id: bool = False
    ):
        """
        This method checks and filters the selected IDs based on the available ones for a specific domain.

            Parameters
        ----------
        input_ids: list or np.ndarray
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
        
        try:

            message = ""
            if isinstance(input_ids, str):
                tokens = input_ids.replace(" ", "").split(",")
                selected_ids = [int(_id) for _id in tokens]

            elif isinstance(input_ids, list):
                selected_ids = input_ids

            elif isinstance(input_ids, tuple | np.ndarray):
                selected_ids = list(input_ids)

            elif isinstance(input_ids, int):
                selected_ids = [input_ids]

            all_ids = []

            match selection_label:
                case "nodes":
                    all_ids = list(self.mesh.nodal_coordinates[:, 0])

                case "face_elements":
                    all_ids = list(self.mesh.faces_connectivity[:, 0])

                case "solid_elements":
                    all_ids = list(self.mesh.solids_connectivity[:, 0])

                case "points":
                    all_ids = self.domains_processor.points_of_domain.get("both")
                    
                case "lines":
                    all_ids = self.domains_processor.lines_of_domain.get("both")

                case "surfaces":
                    all_ids = self.domains_processor.surfaces_of_domain.get("both")

                case "volumes":
                    all_ids = self.domains_processor.volumes_of_domain.get("both", [])

                case _:
                    return None, None

            _size = len(all_ids)

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
                                message += f"Please enter a valid ID between 1 and {_size}."
                                break

                    except Exception as error_log:
                        message = "The selected ID must be an integer. "
                        message += f"Please enter a valid ID between 1 and {_size}.\n\n"
                        message += str(error_log)

        except Exception as log_error:
            message = "Invalid input for the Selected ID.\n\n"
            message += str(log_error)

        filtered_ids = self.filter_selected_entities_based_on_domain(selected_ids, selection_label, domain)

        if not filtered_ids:
            message = f"The selected {selected_ids} ID(s) does not belong to the {domain} domain. Please, "
            message += "enter or selected at least one valid ID to proceed."

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Selection ID"
            error_data = [window_title, title, message]
            return None, error_data

        if single_id:
            return filtered_ids[0], None

        return filtered_ids, None