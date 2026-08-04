from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QDialog,
    QLineEdit,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from vibra import app


TEXT_INPUT_WIDGETS = (QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QAbstractSpinBox)

# Single source of truth for the application keymap.
# Each entry maps a key sequence to a (kind, target, description) tuple:
#   - kind "callback" -> application-wide QShortcut wired to a main window method
#   - kind "action"   -> applied to an existing QAction (dotted path on the main window)
SHORTCUTS = {
    "Ctrl+M": ("callback", "generate_mesh_with_current_setup", "Generate the mesh"),
    "Ctrl+R": ("callback", "run_analysis_shortcut", "Run the analysis"),
    "Ctrl+A": ("callback", "select_all_entities_shortcut", "Select all entities"),
    "Ctrl+E": ("callback", "action_export_mesh_callback", "Export the mesh"),
    "Ctrl+C": ("callback", "copy_screenshot_to_clipboard", "Copy screenshot to clipboard"),
    "Ctrl+D": ("callback", "reset_solution_shortcut", "Reset the solution"),
    "Ctrl+N": ("callback", "action_new_project_callback", "New project"),
    "Ctrl+W": ("callback", "action_home_exit_callback", "Go to home"),
    "Ctrl+Shift+S": ("callback", "action_save_as_callback", "Save the project as"),
    "Ctrl+I": ("callback", "action_import_geometry_callback", "Import geometry"),
    "F5": ("callback", "update_plots", "Refresh the plots"),
    "Alt+P": ("callback", "toggle_section_plane", "Toggle the section plane"),
    "?": ("callback", "show_shortcuts_help", "Show this shortcut list"),
    "Q": ("callback", "workspace_model_shortcut", "Model workspace"),
    "W": ("callback", "workspace_mesh_shortcut", "Mesh workspace"),
    "E": ("callback", "workspace_results_shortcut", "Results workspace"),
    "Ctrl+S": ("action", "action_save", "Save the project"),
    "Ctrl+H": ("action", "action_hide_selection", "Hide the selection"),
    "Ctrl+U": ("action", "action_unhide_all", "Unhide everything"),
    "Ctrl+1": ("action", "view_toolbar.action_top_view", "Top view"),
    "Ctrl+2": ("action", "view_toolbar.action_bottom_view", "Bottom view"),
    "Ctrl+3": ("action", "view_toolbar.action_right_view", "Right view"),
    "Ctrl+4": ("action", "view_toolbar.action_left_view", "Left view"),
    "Ctrl+5": ("action", "view_toolbar.action_front_view", "Front view"),
    "Ctrl+6": ("action", "view_toolbar.action_back_view", "Back view"),
    "Ctrl+7": ("action", "view_toolbar.action_isometric_view", "Isometric view"),
}

# Dialog conventions (Enter/Escape/Delete/Backspace) and widget-local keys are
# intentionally kept in their own widgets and are not listed in SHORTCUTS:
#   - Enter/Escape/Delete in the ~40 input dialogs (keyPressEvent handlers)
#   - Delete on the main window (must stay widget-scoped so those dialogs keep
#     their Delete-row behavior)
#   - Space on the play/pause buttons of the ModalAnalysisBar classes (currently
#     not instantiated)
#   - Ctrl+C in the plot navigation toolbar


def register_global_shortcuts(main_window):
    """
    Registers all shortcuts from the SHORTCUTS registry. This is the single
    source of truth for the application keymap.

    Callback entries become application-wide QShortcuts that are disabled while
    typing in text fields. Action entries set the shortcut of an existing
    QAction (resolved through the dotted path) and make it application-wide.
    """
    qshortcuts = list()

    for keys, (kind, target, description) in SHORTCUTS.items():
        if kind == "callback":
            shortcut = QShortcut(QKeySequence(keys), main_window)
            shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
            shortcut.activated.connect(getattr(main_window, target))
            qshortcuts.append(shortcut)

        elif kind == "action":
            action = _resolve_action(main_window, target)
            action.setShortcut(QKeySequence(keys))
            action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)

        else:
            raise ValueError(f"Unknown shortcut kind: {kind!r}")

    main_window._global_shortcuts = qshortcuts

    def update_shortcuts_enabled(old_widget, new_widget):
        typing = isinstance(new_widget, TEXT_INPUT_WIDGETS)
        for shortcut in qshortcuts:
            shortcut.setEnabled(not typing)

    app().focusChanged.connect(update_shortcuts_enabled)


def _resolve_action(main_window, dotted_path: str):
    obj = main_window
    for attribute in dotted_path.split("."):
        obj = getattr(obj, attribute)
    return obj


def is_focus_on_text_input() -> bool:
    return isinstance(app().focusWidget(), TEXT_INPUT_WIDGETS)


def open_shortcuts_help(parent):
    """
    Shows a dialog listing every shortcut defined in SHORTCUTS.
    """
    dialog = QDialog(parent)
    dialog.setWindowTitle("Keyboard Shortcuts")
    dialog.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    icon = getattr(app().main_window, "vibra_icon", None)
    if icon is not None:
        dialog.setWindowIcon(icon)

    table = QTableWidget(len(SHORTCUTS), 2)
    table.setHorizontalHeaderLabels(["Shortcut", "Action"])
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
    table.setAlternatingRowColors(True)

    for row, (keys, (kind, target, description)) in enumerate(SHORTCUTS.items()):
        table.setItem(row, 0, QTableWidgetItem(keys))
        table.setItem(row, 1, QTableWidgetItem(description))

    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)

    layout = QVBoxLayout(dialog)
    layout.addWidget(table)
    dialog.resize(440, 440)
    dialog.exec()
