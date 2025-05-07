import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from invoke import task

UI_FILES_PATH = Path("vibra/interface/data/ui_files")
GENERATED_PATH = Path("vibra/interface/ui_generated")

def to_camel_case(filename):
    """Convert filename (snake_case or kebab-case) to CamelCase."""
    return "".join(word.capitalize() for word in re.split(r"[_\s-]+", filename))

def extract_class_names(ui_path):
    """Extracts Qt base class and UI class name from the .ui XML file."""
    try:
        tree = ET.parse(ui_path)
        root = tree.getroot()

        # Extract UI class name (inside <class> tag)
        ui_class = root.find("class")
        ui_class_name = ui_class.text if ui_class is not None else None

        # Extract Qt widget base class (from <widget class="QMainWindow">)
        widget = root.find("widget")
        qt_class_name = widget.attrib["class"] if widget is not None else None

        return ui_class_name, qt_class_name
    except Exception as e:
        print(f"⚠️ Error reading {ui_path}: {e}")
        return None, None

@task
def ui_codegen(c):
    """
    Recursively scans the directory and generates widget .py files from .ui files.
    The generated files are saved in `vibra/interface/ui_generated`, keeping 
    the relative structure from `vibra/interface/data/ui_files`.
    
    Usage example: invoke ui-codegen
    """
    root_dir = os.path.abspath(UI_FILES_PATH)
    output_root = os.path.abspath(GENERATED_PATH)

    if not os.path.exists(root_dir):
        print("❌ The specified directory does not exist.")
        return

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".ui"):
                ui_path = os.path.join(dirpath, filename)
                
                # Preserve the relative path structure
                relative_path = os.path.relpath(dirpath, root_dir)
                output_dir = os.path.join(output_root, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                py_path = os.path.join(output_dir, filename.replace(".ui", "_ui.py"))
                relative_ui_path = os.path.relpath(ui_path, root_dir)

                # Extract UI class and Qt base class from the .ui file
                ui_class_name, qt_class_name = extract_class_names(ui_path)

                if not ui_class_name or not qt_class_name:
                    print(f"⚠️ Skipping {ui_path} (Could not determine class names)")
                    continue

                # Convert filename to CamelCase for the wrapper class
                wrapper_class_name = to_camel_case(os.path.splitext(filename)[0])

                # Run pyuic5 to generate the Python file
                command = f"pyuic5 \"{ui_path}\" -o \"{py_path}\""
                result = c.run(command, warn=True)

                if result.ok:
                    # Read the generated file and update comments
                    with open(py_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()

                    modified_lines = []
                    for line in lines:
                        # Update the generated file comment to show the relative path
                        if line.startswith("# Form implementation generated from reading ui file"):
                            line = f"# Form implementation generated from reading ui file '{relative_ui_path}'\n"
                        modified_lines.append(line)

                    # Append the wrapper class
                    wrapper_class = f"""

class {wrapper_class_name}_UI(QtWidgets.{qt_class_name}, Ui_{ui_class_name}):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
"""
                    modified_lines.append(wrapper_class)

                    # Write back to the file
                    with open(py_path, "w", encoding="utf-8") as file:
                        file.writelines(modified_lines)

                    print(f"✅ Generated: {ui_path} → {py_path}")
                else:
                    print(f"❌ Error while generating: {ui_path}")
