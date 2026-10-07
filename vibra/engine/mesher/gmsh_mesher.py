import logging
from copy import deepcopy
from pathlib import Path

import gmsh

from vibra.engine.mesher.element_setup import GMSH_VISUAL_MESH
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import LocalMeshSizeControlSetup, MeshSetup
from vibra.errors import IncompleteSetupError, InvalidGeometryError, MeshingAlgorithmError

logger = logging.getLogger(__name__)


class GmshMesher:
    def __init__(self, path: str | Path | None = None):
        self.setup = MeshSetup()
        self.path: Path | None = None

        if path is not None:
            self.set_path(path)

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def set_mesh_setup(self, setup: MeshSetup):
        self.setup = setup

    def generate(self, threads: int = 0) -> Mesh:
        if self.path is None:
            message = "Geometry not defined"
            context = (
                "The geometry file has not been defined yet."
                "Import a supported CAD file format to proceed."
                "\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise IncompleteSetupError(message, context=context)

        if not gmsh.is_initialized():
            gmsh.initialize("", False, interruptible=False)
            gmsh.option.set_number("General.Terminal", 0)
            gmsh.option.set_number("General.Verbosity", 0)
            gmsh.option.set_number("Geometry.Tolerance", self.setup.geometry_tolerance)

            gmsh.option.set_number("General.NumThreads", threads)
            gmsh.option.set_number("Mesh.MaxNumThreads1D", threads)
            gmsh.option.set_number("Mesh.MaxNumThreads2D", threads)
            gmsh.option.set_number("Mesh.MaxNumThreads3D", threads)

            logger.info("Loading geometry... [10/100]")
            gmsh.open(str(self.path))

        if self.setup.suppressed_volume_ids:
            dim_tags = [(3, vid) for vid in self.setup.suppressed_volume_ids]
            gmsh.model.setVisibility(dim_tags, 0, recursive=True)

        if self.setup.merge_connected_volumes:
            self._merge_nodes_from_adjacent_volumes(self.setup.suppressed_volume_ids)

        logger.info("Configuring mesh... [20/100]")
        self._configure_mesh()

        logger.info("Processing geometry data... [35/100]")

        try:
            dimension = self.setup.element_setup.dimensions
            gmsh.model.mesh.generate(dimension)
        except Exception as e:
            gmsh.finalize()

            exception = MeshingAlgorithmError(
                "A problem occurred while generating the mesh.\n"
                "Reducing the size of the elements and/or changing the 3D meshing "
                "algorithm may help resolve the issue.\n"
                "If neither of these options works, we suggest reviewing the CAD geometry "
                "to eliminate any potential underlying geometric issues."
            )
            logger.error(str(exception))
            raise exception from e

        mesh = Mesh()

        mesh.process_geometry_information()
        mesh.process_downwards_adjacencies_from_entities()
        mesh.process_upwards_adjacencies_from_entities()

        logger.info("Post-processing mesh... [60/100]")
        mesh.suppressed_volumes = set(self.setup.suppressed_volume_ids)
        mesh.post_process_mesh_data()

        mesh.update_element_topology_based_on_connectivity()

        logger.info("Post-processing mesh... [95/100]")
        if self.setup.compute_quality_metrics:
            mesh.compute_mesh_quality_parameters()

        gmsh.finalize()

        logger.info(
            f"Mesh generated with {len(mesh.nodal_coordinates)} nodes"
            f", {len(mesh.lines_connectivity)} dim 1"
            f", {len(mesh.faces_connectivity)} dim 2"
            f"and {len(mesh.solids_connectivity)} dim 3 elements"
        )

        return mesh

    def generate_visual_mesh(self) -> tuple[Mesh, MeshSetup]:
        if self.path is None:
            context = (
                "Geometry not defined\n\n"
                "The geometry file has not been defined yet.\n"
                "Import a supported CAD file format to proceed.\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise InvalidGeometryError(context)

        mesh = Mesh()
        element_size = mesh.compute_initial_mesh_size(str(self.path))
        exception = None

        for _min, _max in [(element_size * 0.4, element_size), (5, 10)]:
            try:
                self.setup = MeshSetup(
                    minimum_element_size=_min,
                    maximum_element_size=_max,
                    custom_element_setup=GMSH_VISUAL_MESH,
                )
                return self.generate(), self.setup
            except Exception as error:
                exception = error

        raise exception

    def _merge_nodes_from_adjacent_volumes(self, suppressed_volume_ids: list[int] | None = None):
        """This method merges all nodes from adjacent volumes."""
        gmsh.model.occ.synchronize()
        volumes_list = gmsh.model.getEntities(3)

        if suppressed_volume_ids:
            volumes_list = [v for v in volumes_list if v[1] not in suppressed_volume_ids]

        if len(volumes_list) < 2:
            return

        gmsh.model.occ.fragment(volumes_list, volumes_list)
        gmsh.model.occ.synchronize()

    def _configure_mesh(self):
        if self.setup.local_mesh_size_control_parameters:
            self._apply_local_mesh_size_control(
                self.setup.maximum_element_size,
                self.setup.local_mesh_size_control_parameters,
            )
        else:
            gmsh.option.setNumber("Mesh.MeshSizeMin", self.setup.minimum_element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", self.setup.maximum_element_size)

        gmsh.option.setNumber("Mesh.RandomSeed", self.setup.random_seed)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", self.setup.size_factor)
        gmsh.option.setNumber("Mesh.Algorithm", self.setup.element_setup.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", self.setup.element_setup.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", self.setup.element_setup.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", self.setup.element_setup.subdivision_algorithm)
        gmsh.option.setNumber("Mesh.RecombineAll", self.setup.element_setup.recombine_all)
        gmsh.option.setNumber("Mesh.ElementOrder", self.setup.element_setup.element_order)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", self.setup.element_setup.second_order_incomplete)
        gmsh.option.setNumber("Mesh.MeshOnlyVisible", 1)

        gmsh.model.mesh.clear()
        gmsh.model.occ.synchronize()

    def _apply_local_mesh_size_control(self, global_size: float, size_control_setups: list[LocalMeshSizeControlSetup]):
        setup_sizes = [setup.element_size for setup in size_control_setups]
        max_size = max([global_size, *setup_sizes])

        fields_list = []

        for setup in size_control_setups:
            match setup.entity_type:
                case "surfaces":
                    entity_type = "SurfacesList"
                case "volumes":
                    entity_type = "VolumesList"
                case _:
                    continue

            # this is the actual size control part
            setup_size_control_field = gmsh.model.mesh.field.add("Constant")
            gmsh.model.mesh.field.setNumbers(setup_size_control_field, entity_type, setup.entity_ids)
            gmsh.model.mesh.field.setNumber(setup_size_control_field, "VIn", setup.element_size)
            fields_list.append(setup_size_control_field)

        # this is the complementary set of entities size control part
        if max_size > global_size:
            # Coarsening: the global size is applied as a refinement of every
            # region that is not explicitly coarsened.

            gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)  # Necessary call for the fields to override this setting

            all_volumes = {tag for dim, tag in gmsh.model.getEntities(3)}
            all_faces = {tag for dim, tag in gmsh.model.getEntities(2)}

            # Pin (i.e. spefifically defining the global size for NOT coarsened entities) the complement:
            # every entity that is not to be coarsened is forced to the global size
            targeted_volumes, targeted_faces = self._get_coarsened_entities(size_control_setups, global_size)
            coarsened_volumes = targeted_volumes
            pinned_volumes = all_volumes - coarsened_volumes

            coarsened_faces = self._get_faces_to_coarsen(
                targeted_faces, targeted_volumes
            )  # needed beacause faces of targeted volumes would be pinned otherwise
            pinned_faces = all_faces - coarsened_faces

            pinned_curves, pinned_points = self._get_pinned_boundary_entities(all_faces, pinned_faces, coarsened_faces)

            global_size_control_field = gmsh.model.mesh.field.add("Constant")
            gmsh.model.mesh.field.setNumbers(global_size_control_field, "VolumesList", sorted(pinned_volumes))
            gmsh.model.mesh.field.setNumbers(global_size_control_field, "SurfacesList", sorted(pinned_faces))
            gmsh.model.mesh.field.setNumbers(global_size_control_field, "CurvesList", sorted(pinned_curves))
            gmsh.model.mesh.field.setNumbers(global_size_control_field, "PointsList", sorted(pinned_points))
            gmsh.model.mesh.field.setNumber(global_size_control_field, "VIn", global_size)
            gmsh.model.mesh.field.setNumber(global_size_control_field, "VOut", max_size)
            gmsh.model.mesh.field.setNumber(global_size_control_field, "IncludeBoundary", 0)
            gmsh.model.mesh.field.setNumber(global_size_control_field, "IncludeEmbedded", 0)
            fields_list.append(global_size_control_field)
        else:
            # Refining only: a constant upper bound, the per-setup fields
            # refine their targets below it.
            max_size_control_field = gmsh.model.mesh.field.add("Constant")
            gmsh.model.mesh.field.setNumbers(max_size_control_field, "SurfacesList", [])
            gmsh.model.mesh.field.setNumbers(max_size_control_field, "VolumesList", [])
            gmsh.model.mesh.field.setNumber(max_size_control_field, "VOut", global_size)
            fields_list.append(max_size_control_field)

        minimum_field = gmsh.model.mesh.field.add("Min")
        gmsh.model.mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
        gmsh.model.mesh.field.setAsBackgroundMesh(minimum_field)

    def _get_coarsened_entities(
        self,
        size_control_setups: list[LocalMeshSizeControlSetup],
        global_size: float,
    ) -> tuple[set[int], set[int]]:
        """Returns the volumes and surfaces explicitly targeted by a coarsening setup."""
        targeted_volumes: set[int] = set()
        targeted_faces: set[int] = set()
        for setup in size_control_setups:
            if setup.element_size <= global_size:
                continue
            if setup.entity_type == "volumes":
                targeted_volumes.update(setup.entity_ids)
            elif setup.entity_type == "surfaces":
                targeted_faces.update(setup.entity_ids)
        return targeted_volumes, targeted_faces

    def _get_faces_to_coarsen(
        self,
        targeted_faces: set[int],
        targeted_volumes: set[int],
    ) -> set[int]:
        """Faces left at the coarsest size.

        The explicitly targeted faces and every boundary face of the volumes
        directly targeted by a coarsening setup stay coarse; every other face
        is pinned to the global size. A face shared with a volume that is not
        coarsened is left coarse as well: it is meshed once, and the coarse
        size carries over to the neighbouring volume, which grades back down to
        the global size.
        """
        faces_to_coarsen = set(targeted_faces)
        for volume in targeted_volumes:
            for dim, face in gmsh.model.getBoundary([(3, volume)], recursive=False, oriented=False):
                faces_to_coarsen.add(face)
        return faces_to_coarsen

    def _get_pinned_boundary_entities(
        self,
        all_faces: set[int],
        pinned_faces: set[int],
        coarsened_faces: set[int],
    ) -> tuple[set[int], set[int]]:
        """Curves and points that must be pinned to the global size.

        The boundary of a pinned face must be pinned as well, otherwise it
        would stay at the coarse size and constrain the finer mesh on the
        pinned face. A curve shared between a pinned and a coarse face is kept
        coarse instead, so that the coarse size carries over onto the coarse
        face through its boundary.
        """
        faces_per_curve: dict[int, set[int]] = {}
        faces_per_point: dict[int, set[int]] = {}
        for face in all_faces:
            for dim, tag in gmsh.model.getBoundary([(2, face)], recursive=False, oriented=False):
                if dim == 1:
                    faces_per_curve.setdefault(tag, set()).add(face)
            for dim, tag in gmsh.model.getBoundary([(2, face)], recursive=True, oriented=False):
                if dim == 0:
                    faces_per_point.setdefault(tag, set()).add(face)

        pinned_curves = {curve for curve, faces in faces_per_curve.items() if (faces & pinned_faces) and not (faces & coarsened_faces)}
        pinned_points = {point for point, faces in faces_per_point.items() if (faces & pinned_faces) and not (faces & coarsened_faces)}
        return pinned_curves, pinned_points
