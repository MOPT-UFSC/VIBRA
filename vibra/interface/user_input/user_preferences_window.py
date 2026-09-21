from copy import deepcopy
from molde.colors import Color
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QLabel,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QWidget,
)
from vibra import app
from vibra.interface.general.pick_color_input import PickColorInput
from vibra.interface.ui_generated.project.render.user_preferences_window_ui import UserPreferencesWindow_UI


class UserPreferencesInput(UserPreferencesWindow_UI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self.config = app().config
        self.tmp_user_preferences = deepcopy(app().config.user_preferences)

        self.swatches: dict[str, list[QLabel]] = {}
        self.spinboxes: dict[str, QSpinBox] = {}
        self.checkboxes: dict[str, QCheckBox] = {}
        self.rows: list[tuple[list[QWidget], str, str]] = []
        self.category_pages: dict[str, QWidget] = {}
        self._current_category = ""

        self._config_window()
        self._create_pages()
        self._create_connections()
        self._load_values()

        self.lineEdit_search.setFocus()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.lineEdit_search.setStyleSheet(
            "QLineEdit::placeholder { color: #999999; font-style: italic; }"
        )
        self.listWidget_categories.setStyleSheet(
            "QListWidget::item { padding: 6px; }"
            "QListWidget::item:selected { background-color: palette(highlight); color: palette(highlighted-text); }"
        )

    def _create_pages(self):
        placeholder = self.stackedWidget_categories.widget(0)
        self.stackedWidget_categories.removeWidget(placeholder)
        placeholder.deleteLater()

        self._create_geometry_renderer_page()
        self._create_mesh_renderer_page()
        self._create_renderer_page()
        self._create_general_page()
        self._create_subprocess_page()

        self.listWidget_categories.setCurrentRow(0)
        self.stackedWidget_categories.setCurrentIndex(0)

    def _create_connections(self):
        self.listWidget_categories.currentRowChanged.connect(self.stackedWidget_categories.setCurrentIndex)

        self.filter_timer = QTimer()
        self.filter_timer.setInterval(150)
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(self._filter_settings)
        self.lineEdit_search.textChanged.connect(self._start_filter_timer)

        self.pushButton_reset_to_default.clicked.connect(self.reset_to_default)
        self.pushButton_apply_settings.clicked.connect(self.apply_user_preferences)
        self.pushButton_update_settings.clicked.connect(self.confirm_and_update_user_preferences)

    def _add_category_page(self, name: str) -> QGridLayout:
        self._current_category = name

        page = QWidget()
        layout = QGridLayout(page)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(4, 1)

        self.stackedWidget_categories.addWidget(page)
        self.category_pages[name] = page
        QListWidgetItem(name, self.listWidget_categories)

        return layout

    def _finalize_page(self, layout: QGridLayout):
        layout.setRowStretch(layout.rowCount(), 1)

    #pages

    def _create_geometry_renderer_page(self):
        layout = self._add_category_page("Geometry Renderer")

        self._add_color_row(layout, "Points color", "nodes_points_color")
        self._add_color_row(layout, "Lines color", "lines_color")

        self._add_color_row(layout, "Selection lines color", "selection_lines_color")
        self._add_color_row(layout, "Selection points color", "selection_nodes_points_color")
        self._add_color_row(layout, "Selection faces color", "selection_faces_color")

        self._add_spinbox_row(layout, "Points size", "points_size", 1, 100)
        self._add_spinbox_row(layout, "Lines thickness", "lines_thickness", 1, 100)

        self._finalize_page(layout)

    def _create_mesh_renderer_page(self):
        layout = self._add_category_page("Mesh Renderer")

        self._add_color_row(layout, "Nodes color", "nodes_points_color")
        self._add_color_row(layout, "Edges color", "edges_color")
        self._add_color_row(layout, "Volumes color", "volumes_color")

        self._add_color_row(layout, "Selection nodes color", "selection_nodes_points_color")
        self._add_color_row(layout, "Selection faces color", "selection_faces_color")

        self._add_spinbox_row(layout, "Nodes size", "nodes_size", 1, 100)
        self._add_spinbox_row(layout, "Edges thickness", "edges_thickness", 1, 100)

        self._finalize_page(layout)

    def _create_renderer_page(self):
        layout = self._add_category_page("Renderer")

        self._add_color_row(layout, "Font color", "renderer_font_color")
        self._add_color_row(layout, "Background color 1", "renderer_background_color_1")
        self._add_color_row(layout, "Background color 2", "renderer_background_color_2")

        self._add_spinbox_row(layout, "Font size", "renderer_font_size", 1, 72)

        self._finalize_page(layout)

    def _create_general_page(self):
        layout = self._add_category_page("General")

        self._add_checkbox_row(layout, "Show reference scale", "show_reference_scale_bar")
        self._add_checkbox_row(layout, "Compatibility mode", "compatibility_mode")

        self._finalize_page(layout)

    def _create_subprocess_page(self):
        layout = self._add_category_page("Subprocess")

        self._add_checkbox_row(layout, "Run analysis in subprocess", "run_analysis_in_subprocess")
        self._add_checkbox_row(layout, "Generate mesh in subprocess", "generate_mesh_in_subprocess")

        self._finalize_page(layout)

    #rows

    def _add_color_row(self, layout: QGridLayout, label_text: str, field_name: str):
        row_index = layout.rowCount()

        label = QLabel(f"{label_text}:")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        swatch = QLabel()
        swatch.setFixedSize(90, 26)

        button = QPushButton("Pick color")
        button.setMinimumWidth(110)

        layout.addWidget(label, row_index, 1)
        layout.addWidget(swatch, row_index, 2)
        layout.addWidget(button, row_index, 3)

        self.swatches.setdefault(field_name, []).append(swatch)
        button.clicked.connect(lambda: self._pick_color(field_name, label_text))

        self.rows.append(([label, swatch, button], self._current_category, label_text.lower()))

    def _add_spinbox_row(self, layout: QGridLayout, label_text: str, field_name: str, minimum: int, maximum: int):
        row_index = layout.rowCount()

        label = QLabel(f"{label_text}:")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        spin = QSpinBox()
        spin.setRange(minimum, maximum)
        spin.setFixedWidth(90)

        layout.addWidget(label, row_index, 1)
        layout.addWidget(spin, row_index, 2)

        self.spinboxes[field_name] = spin
        spin.valueChanged.connect(lambda value: setattr(self.tmp_user_preferences, field_name, value))

        self.rows.append(([label, spin], self._current_category, label_text.lower()))

    def _add_checkbox_row(self, layout: QGridLayout, label_text: str, field_name: str):
        row_index = layout.rowCount()

        label = QLabel(f"{label_text}:")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        checkbox = QCheckBox()

        layout.addWidget(label, row_index, 1)
        layout.addWidget(checkbox, row_index, 2)

        self.checkboxes[field_name] = checkbox
        checkbox.toggled.connect(lambda checked: setattr(self.tmp_user_preferences, field_name, checked))

        self.rows.append(([label, checkbox], self._current_category, label_text.lower()))

    #updates

    def _pick_color(self, field_name: str, label_text: str):
        read = PickColorInput(title=f"Pick the {label_text.lower()}")
        if read.complete:
            color = Color(*read.color)
            setattr(self.tmp_user_preferences, field_name, color)
            self._refresh_swatches(field_name)

    def _refresh_swatches(self, field_name: str | None = None):
        field_names = [field_name] if field_name else list(self.swatches.keys())
        for name in field_names:
            color: Color = getattr(self.tmp_user_preferences, name)
            for swatch in self.swatches.get(name, []):
                swatch.setStyleSheet(
                    f"background-color: {color.to_hex()}; border: 1px solid palette(mid); border-radius: 3px;"
                )

    def _load_values(self):
        self._refresh_swatches()

        for field_name, spin in self.spinboxes.items():
            spin.blockSignals(True)
            spin.setValue(getattr(self.tmp_user_preferences, field_name))
            spin.blockSignals(False)

        for field_name, checkbox in self.checkboxes.items():
            checkbox.blockSignals(True)
            checkbox.setChecked(getattr(self.tmp_user_preferences, field_name))
            checkbox.blockSignals(False)

    #filter

    def _start_filter_timer(self):
        self.filter_timer.start()

    def _filter_settings(self):
        filter_text = self.lineEdit_search.text().strip().lower()
        category_has_match = {name: False for name in self.category_pages}

        for widgets, category, search_text in self.rows:
            matches = (not filter_text) or (filter_text in search_text)
            for widget in widgets:
                widget.setVisible(matches)
            if matches:
                category_has_match[category] = True

        first_visible_row = -1
        for index in range(self.listWidget_categories.count()):
            item = self.listWidget_categories.item(index)
            visible = category_has_match[item.text()]
            item.setHidden(not visible)
            if visible and first_visible_row == -1:
                first_visible_row = index

        if filter_text and first_visible_row != -1:
            current_item = self.listWidget_categories.currentItem()
            if current_item is None or current_item.isHidden():
                self.listWidget_categories.setCurrentRow(first_visible_row)

    #apply

    def apply_user_preferences(self):
        app().config.user_preferences = self.tmp_user_preferences

        app().main_window.selection.selection_changed.emit()
        self.update_settings()
        self.config.update_config_file()

    def confirm_and_update_user_preferences(self):
        self.apply_user_preferences()
        self.accept()

    def update_settings(self):
        app().main_window.update_scale_bar(self.tmp_user_preferences.show_reference_scale_bar)
        app().main_window.update_renderer_font_size()
        app().main_window.update_plots(reset_camera=False)

    def reset_to_default(self):
        if self.config.user_preferences.interface_theme == "dark":
            app().config.user_preferences.set_dark_theme()
        else:
            app().config.user_preferences.set_light_theme()

        app().config.user_preferences.reset_attributes()
        self.tmp_user_preferences = deepcopy(app().config.user_preferences)

        self._load_values()
        self.apply_user_preferences()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.confirm_and_update_user_preferences()
        elif event.key() == Qt.Key_Escape:
            self.close()
