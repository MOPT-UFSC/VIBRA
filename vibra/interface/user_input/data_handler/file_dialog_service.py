import platform
from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from collections import defaultdict


class FileDialogService:
    @staticmethod
    def open_file(file_extensions: list[str], caption: str = "Open file", last_folder: str | Path = None) -> Path | None:
        last_folder, caption, filter_str, kwargs = FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)

        path, selected_filter = QFileDialog.getOpenFileName(None, caption, str(last_folder), filter_str, **kwargs)

        if not path:
            return None

        path = Path(path)

        if not path.suffix:
            suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
            path = path.with_suffix(suffix)

        return path

    @staticmethod
    def open_multiple_files(file_extensions: list[str], caption: str = "Open multiple files", last_folder: str = None) -> list[Path] | None:
        last_folder, caption, filter_str, kwargs = FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder)

        paths, selected_filter = QFileDialog.getOpenFileNames(None, caption, str(last_folder), filter_str, **kwargs)

        if not paths:
            return None

        paths = [Path(path) for path in paths]

        for i, path in enumerate(paths):
            if not path.suffix:
                suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
                paths[i] = path.with_suffix(suffix)

        return paths

    @staticmethod
    def save_file(file_extensions: list[str], caption: str = "Save file", last_folder: str = None) -> Path | None:
        last_folder, caption, filter_str, kwargs = FileDialogService._build_dialog_kwargs(file_extensions, caption, last_folder, open_file=False)

        path, selected_filter = QFileDialog.getSaveFileName(None, caption, str(last_folder), filter_str, **kwargs)

        if not path:
            return None

        path = Path(path)

        if not path.suffix:
            suffix = f".{FileDialogService._get_path_extension(selected_filter)}"
            path = path.with_suffix(suffix)

        return path

    @staticmethod
    def _build_dialog_kwargs(file_extensions: list[str], caption: str, last_folder: str | None, open_file=True):
        if last_folder is None:
            last_folder = Path().home()

        kwargs = {}
        if platform.system() == "Linux":
            kwargs["options"] = QFileDialog.Option.DontUseNativeDialog

        filter_str = FileDialogService._generate_file_extensions_str(file_extensions, open_file)

        return last_folder, caption, filter_str, kwargs

    @staticmethod
    def _generate_file_extensions_str(file_extensions: list[str], all_files=True):
        file_extensions.sort(key=FileDialogService._sort_extensions)

        if not all_files or len(file_extensions) == 1:
            return ";;".join(f"{FileDialogService._get_file_label(ext)} (*.{ext.lower()})" for ext in file_extensions)

        ext_dict = defaultdict(list)
        for ext in file_extensions:
            ext_str = f"*.{ext}"
            ext_dict["All files"].append(ext_str)
            ext_dict[FileDialogService._get_file_label(ext)].append(ext_str)

        ext_str = ""
        for label, extensions in ext_dict.items():
            ext_str += f"{label} ({" ".join(extensions)});;"

        return ext_str
                
    @staticmethod
    def _get_file_label(extension: str) -> str:
        extension = extension.lower() 

        match extension:
            case "xlsx" | "xls":
                return "Spreadsheet files"
            case "dat" | "csv" | "txt":
                return "Text files"
            case "vibra":
                return "Project files"
            case "iges" | "igs" | "step" | "stp":
                return "Geometry files"
            case "msh" | "bdf" | "nas":
                return "Mesh files"
            case _:
                return f"{extension.title()} file"

    @staticmethod
    def _get_path_extension(string: str) -> str:
        return string.split("*.")[-1].rstrip(")")

    @staticmethod
    def get_existing_directory(caption: str, directory: str | Path) -> Path | None:
        existing_dir = QFileDialog.getExistingDirectory(caption=caption, dir=str(directory))
        existing_dir = Path(existing_dir)

        if existing_dir.exists():
            return existing_dir

    @staticmethod
    def _sort_extensions(extension: str) -> int:
        extension = extension.lower()

        match extension:
            case "xlsx":
                return 0
            case "xls":
                return 1
            case "dat":
                return 2
            case "txt":
                return 3
            case "csv":
                return 4
            case "vibra":
                return 5
            case "iges" | "igs" | "step" | "stp":
                return 6
            case "msh" | "bdf" | "nas":
                return 7
            case _:
                return 8
