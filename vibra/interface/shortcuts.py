from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QDialog,
    QLineEdit,
    QMenu,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from vibra import app

# --- How to add a shortcut -------------------------------------------------
# Add an entry to the SHORTCUTS dict below. Each key is a Qt key sequence; each value is a
# (kind, target, description) tuple:
#
#   "callback" -> call a method on the main window, e.g.:
#       "F5": ("callback", "update_plots", "Refresh the plots")
#
#   "action"   -> trigger an existing QAction, addressed as a dotted path
#       from the main window, e.g.:
#       "Ctrl+S": ("action", "action_save", "Save the project")
#       "Ctrl+1": ("action", "view_toolbar.action_front_view", "Front view")
#
# register_global_shortcuts() wires everything at startup and the "?" dialog
# lists the keymap automatically.
# ---------------------------------------------------------------------------

TEXT_INPUT_WIDGETS = (QLineEdit, QTextEdit, QPlainTextEdit, QAbstractSpinBox)


def is_typing_input(widget) -> bool:
    """
    True when the focused widget actually accepts keyboard text input.

    Non-editable QComboBoxes (selection-only) and read-only widgets should not
    count as text input: they never consume letters/arrows for typing, so we
    should not grey out shortcut actions while the user is simply picking an
    option (e.g. analysis type / physical domain).
    """
    if isinstance(widget, QComboBox):
        return widget.isEditable()
    return isinstance(widget, TEXT_INPUT_WIDGETS)

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
    "E": ("action", "action_results_workspace", "Results workspace"
    ),
    "Ctrl+S": ("action", "action_save", "Save the project"),
    "Ctrl+H": ("action", "action_hide_selection", "Hide the selection"),
    "Ctrl+U": ("action", "action_unhide_all", "Unhide everything"),

    "Ctrl+1": ("action", "view_toolbar.action_front_view", "Front view"),
    "Ctrl+2": ("action", "view_toolbar.action_back_view", "Back view"),
    "Ctrl+3": ("action", "view_toolbar.action_left_view", "Left view"),
    "Ctrl+4": ("action", "view_toolbar.action_right_view", "Right view"),
    "Ctrl+5": ("action", "view_toolbar.action_top_view", "Top view"),
    "Ctrl+6": ("action", "view_toolbar.action_bottom_view", "Bottom view"),
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
    Registers every entry of the SHORTCUTS registry as a standalone
    application-wide QShortcut, wired to a target.

    - kind "callback" -> the QShortcut triggers a main window method.
    - kind "action"   -> the QShortcut triggers the resolved QAction.

    The QActions themselves are never disabled, so their toolbar/menu icons
    stay enabled and visible the whole time. Only the QShortcut objects are
    toggled while the focus is in a widget that truly accepts text input, so
    keystrokes are not stolen while the user types (non-editable QComboBoxes
    are not treated as text input).

    Because the key sequences are not attached to the QActions anymore, Qt
    will no longer draw the shortcut next to a menu entry/toolbar button by
    itself. Use the SHORTCUTS registry (shown by the "?" help) to discover
    and/or display the hints in the UI as needed.
    """
    all_shortcuts = list()

    for keys, (kind, target, description) in SHORTCUTS.items():
        shortcut = QShortcut(QKeySequence(keys), main_window)
        shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)

        if kind == "callback":
            shortcut.activated.connect(getattr(main_window, target))
        elif kind == "action":
            action = _resolve_action(main_window, target)
            shortcut.activated.connect(action.trigger)
        else:
            raise ValueError(f"Unknown shortcut kind: {kind!r}")

        all_shortcuts.append(shortcut)

    main_window._global_shortcuts = all_shortcuts

    def update_shortcuts_enabled(old_widget, new_widget):
        typing = is_typing_input(new_widget)
        for shortcut in all_shortcuts:
            shortcut.setEnabled(not typing)

    app().focusChanged.connect(update_shortcuts_enabled)

    _label_menu_shortcuts(main_window)


def _resolve_action(main_window, dotted_path: str):
    obj = main_window
    for attribute in dotted_path.split("."):
        obj = getattr(obj, attribute)
    return obj


def _label_menu_shortcuts(main_window):
    """
    Appends each shortcut's key sequence to the text of the actions that are
    shown inside a QMenu (e.g. Project > Save, Open…). Using a tab separator
    makes Qt right-align the key in menu items, so users see "Save  Ctrl+S"
    even though the shortcut itself is held by a separate QShortcut (not by the
    action). Toolbar/button-only actions are left untouched.
    """
    menus = main_window.findChildren(QMenu)
    menu_actions = set()
    for menu in menus:
        menu_actions.update(menu.actions())

    for keys, (kind, target, description) in SHORTCUTS.items():
        if kind != "action":
            continue

        action = _resolve_action(main_window, target)
        if action in menu_actions:
            action.setText(f"{action.text()}\t{keys}")


def is_focus_on_text_input() -> bool:
    return is_typing_input(app().focusWidget())


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
