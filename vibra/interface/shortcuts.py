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
    "Ctrl+Shift+G": ("callback", "generate_mesh_with_current_setup", "Generate the mesh"),
    "Ctrl+R": ("action", "analysis_toolbar.run_analysis_action", "Run the analysis"),
    "Ctrl+A": ("callback", "select_all_entities_shortcut", "Select all entities"),
    "Ctrl+E": ("action", "action_export_mesh", "Export the mesh"),
    "Ctrl+C": ("callback", "copy_screenshot_to_clipboard", "Copy screenshot to clipboard"),
    "Ctrl+P": ("action", "action_capture_image", "Capture the image"),
    "Ctrl+D": ("action", "analysis_toolbar.reset_solution_action", "Reset the solution"),
    "Ctrl+N": ("action", "action_new_project", "New project"),
    "Ctrl+O": ("action", "action_open_project", "Open a project"),
    "Ctrl+W": ("action", "action_home_exit", "Go to home"),
    "Ctrl+Shift+S": ("action", "action_save_as", "Save the project as"),
    "Ctrl+I": ("action", "action_import_geometry", "Import geometry"),
    "Ctrl+Shift+I": ("action", "action_import_mesh", "Import mesh"),
    "F5": ("callback", "update_plots", "Refresh the plots"),
    "Alt+P": ("callback", "toggle_section_plane", "Toggle the section plane"),
    "?": ("callback", "show_shortcuts_help", "Show this shortcut list"),
    "Q": ("action", "action_model_workspace", "Model workspace"),
    "W": ("action", "action_mesh_workspace", "Mesh workspace"),
    "E": ("action", "action_results_workspace", "Results workspace"),
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
# The plot navigation toolbar keeps its own Ctrl+C (copy graph) shortcut; it is
# window-scoped and coexists with the app-wide Ctrl+C, which is disabled while
# typing in text fields.


def register_global_shortcuts(main_window):
    """
    Registers all shortcuts from the SHORTCUTS registry. This is the single
    source of truth for the application keymap.

    Callback entries become application-wide QShortcuts. Action entries set the
    shortcut of an existing QAction (resolved through the dotted path) and make
    it application-wide, so Qt also shows the shortcut next to the toolbar
    button and in the menu. While typing in a text field, both QShortcuts and
    the guarded QActions are disabled (the enabled state of the actions is
    restored afterwards).
    """
    qshortcuts = list()
    actions = list()
    action_states = dict()

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
            actions.append(action)

        else:
            raise ValueError(f"Unknown shortcut kind: {kind!r}")

    main_window._global_shortcuts = qshortcuts

    def update_shortcuts_enabled(old_widget, new_widget):
        typing = isinstance(new_widget, TEXT_INPUT_WIDGETS)
        for shortcut in qshortcuts:
            shortcut.setEnabled(not typing)
        for action in actions:
            if typing:
                action_states[action] = action.isEnabled()
                action.setEnabled(False)
            elif action in action_states:
                action.setEnabled(action_states.pop(action))

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
