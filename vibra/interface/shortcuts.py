from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QAbstractSpinBox, QComboBox, QLineEdit, QPlainTextEdit, QTextEdit

from vibra import app


TEXT_INPUT_WIDGETS = (QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QAbstractSpinBox)

GLOBAL_SHORTCUTS = {
    "Ctrl+M": "generate_mesh_with_current_setup",
    "Ctrl+R": "run_analysis_shortcut",
    "Ctrl+A": "select_all_entities_shortcut",
    "Ctrl+Shift+S": "action_save_as_callback",
    "Ctrl+I": "action_import_geometry_callback",
    "Q": "workspace_model_shortcut",
    "W": "workspace_mesh_shortcut",
    "E": "workspace_results_shortcut",
}


def register_global_shortcuts(main_window):
    """
    Registers the global shortcuts that work from anywhere in the software,
    connecting each key to a method of the main window. The shortcuts are
    disabled while typing in text fields.

    Note: some shortcuts live elsewhere on purpose - the camera views
    (Ctrl+1..7) on the view toolbar actions and the menu shortcuts (Ctrl+S,
    Ctrl+H, Ctrl+U) defined in the generated UI files.
    """
    shortcuts = list()

    for keys, method_name in GLOBAL_SHORTCUTS.items():
        shortcut = QShortcut(QKeySequence(keys), main_window)
        shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        shortcut.activated.connect(getattr(main_window, method_name))
        shortcuts.append(shortcut)

    main_window._global_shortcuts = shortcuts

    def update_shortcuts_enabled(old_widget, new_widget):
        typing = isinstance(new_widget, TEXT_INPUT_WIDGETS)
        for shortcut in shortcuts:
            shortcut.setEnabled(not typing)

    app().focusChanged.connect(update_shortcuts_enabled)


def is_focus_on_text_input() -> bool:
    return isinstance(app().focusWidget(), TEXT_INPUT_WIDGETS)
