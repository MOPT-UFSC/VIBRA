from pathlib import Path

from vibra.engine.mesher.mesh import Mesh


class MeshSerializer:
    """Reads and writes meshes from and to disk.

    Supports the native ``.vmsh`` format and all formats handled by gmsh
    (e.g. ``.msh``, ``.nas``, ``.stl``). The format is selected by extension.
    """

    @staticmethod
    def read(path: Path | str) -> Mesh:
        """Reads a mesh from disk.

        The reader is selected by extension: ``.vmsh`` uses the native format;
        other gmsh-supported extensions load through gmsh.

        Args:
            path: Path of the mesh file to load.

        Returns:
            The mesh read from ``path``, or an empty ``Mesh`` for unknown
            extensions.
        """
        path = Path(path)

        match path.suffix:
            case ".vmsh":
                return MeshSerializer._read_vmsh_meshes(path)
            case ".msh":
                return MeshSerializer._read_gmsh_meshes(path)

        return Mesh()

    @staticmethod
    def write(mesh: Mesh, file_path: Path | str):
        """Writes a mesh to disk.

        The format is selected by extension.

        Args:
            mesh: The mesh to serialize.
            file_path: Destination file path.
        """

    @staticmethod
    def _read_vmsh_meshes(file_path: Path) -> Mesh:
        """Reads a mesh in the native vibra ``.vmsh`` format.

        Args:
            file_path: Path of the ``.vmsh`` file to load.

        Returns:
            The mesh read from ``file_path``.
        """
        return Mesh()

    @staticmethod
    def _read_gmsh_meshes(file_path: Path) -> Mesh:
        """Reads a mesh in any format supported by gmsh.

        Args:
            file_path: Path of the mesh file to load.

        Returns:
            The mesh read from ``file_path``.
        """
        return Mesh()

    @staticmethod
    def _write_vmsh_meshes(mesh: Mesh, file_path: Path | str):
        """Writes a mesh to the native vibra ``.vmsh`` format.

        Args:
            mesh: The mesh to serialize.
            file_path: Destination ``.vmsh`` file path.
        """

    @staticmethod
    def _write_gmsh_meshes(mesh: Mesh, file_path: Path | str):
        """Writes a mesh to a format supported by gmsh.

        The format is selected by extension.

        Args:
            mesh: The mesh to serialize.
            file_path: Destination file path.
        """
