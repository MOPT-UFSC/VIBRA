from pathlib import Path
from zipfile import ZipFile


class VibraFile:
    def __init__(self, path, open_mode="r") -> None:
        self.path = Path(path)
        self.open_mode = open_mode
        self.zip = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def open(self):
        self.zip = ZipFile(self.path, self.open_mode)

    def close(self):
        self.zip.close()
        self.zip = None

    def write(self, project):
        self._write_header(project)
        self._write_thumbnail(project)
        self._write_geometry(project)
        self._write_mesh(project)

    def read(self, project):
        project = Project()
        self._read_header(project)
        self._read_thumbnail(project)
        self._read_geometry(project)
        self._read_mesh(project)

    # GETTERS
    def get_thumbnail(self):
        pass

    def get_mesh(self):
        pass

    def get_geometry(self):
        pass

    # WRITER
    def _write_header(self, project):
        pass

    def _write_thumbnail(self, project):
        pass

    def _write_geometry(self, project):
        pass

    def _write_mesh(self, project):
        pass

    # READER
    def _read_header(self, project):
        pass

    def _read_thumbnail(self, project):
        pass

    def _read_geometry(self, project):
        pass

    def _read_mesh(self, project):
        pass

    # USEFULL
    def _file_exists(self, path: str) -> bool:
        file_paths = [member.filename for member in self.zip.infolist()]
        return path in file_paths

    def _write_string(self, arcname, data):
        self.zip.writestr(arcname, data)

    def _read_string(self, arcname):
        return self.zip.read(arcname)

    def _write_json(self, arcname, data):
        json_data = json.dumps(data, indent=2)
        self._write_string(arcname, json_data)

    def _read_json(self, arcname):
        data = self._read_string(arcname)
        json_data = json.loads(data)
        return dict(json_data)

    def _write_array(self, arcname, data, *args, delimiter=";", **kwargs):
        file = BytesIO()
        np.savetxt(file, data, *args, delimiter=delimiter, **kwargs)
        self._write_string(arcname, file.getvalue().decode())

    def _read_array(self, arcname, *args, delimiter=";", **kwargs):
        data = self._read_string(arcname)
        file = BytesIO(data)
        return np.loadtxt(file, *args, delimiter=delimiter, **kwargs)
