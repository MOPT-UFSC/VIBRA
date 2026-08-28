from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QTableWidgetItem

from vibra import app
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.interface.common.common_interface import generate_mesh_and_finalize
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.ui_generated.model.general.volume_suppression_dialog_ui import (
    VolumeSuppressionDialog_UI,
)


class VolumeSuppressionInputs(VolumeSuppressionDialog_UI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        app().main_window.set_input_widget(self)

        self.complete = False
        self.keep_window_open = True

        mesh = app().project.model.mesh
        mesh_setup = app().project.model.mesh_setup
        configured = set(mesh_setup.suppressed_volume_ids) if mesh_setup else set()
        applied = set(mesh.suppressed_volumes) if mesh else set()

        self.previously_suppressed_ids = applied
        self._configured_ids = configured
        self.pending_ids: set[int] = configured - applied
        self.suppressed_volume_ids = applied | self.pending_ids
        self.last_synced_ids: set[int] = set()
        self._previous_volume_selection: set[int] = set()

        self._config_window()
        self._configure_table()
        self._create_connections()
        self._populate_table()

        app().main_window.selection.volume_selection_mode = True
        self._geometry_selection_callback()

        while self.keep_window_open:
            self.exec()


    def _config_window(self):
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Volume Suppression")
        self.setMinimumSize(420, 400)

    def _configure_table(self):
        self.tableWidget_local_mesh_size_control_data.setColumnCount(2)
        self.tableWidget_local_mesh_size_control_data.setHorizontalHeaderLabels(
            ["Volume ID", "Status"]
        )
        self.tableWidget_local_mesh_size_control_data.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tableWidget_local_mesh_size_control_data.verticalHeader().setVisible(False)

    def _create_connections(self):
        self.pushButton_suppress.clicked.connect(self._suppress_callback)
        self.pushButton_unsuppress.clicked.connect(self._unsuppress_callback)
        # clicked() always fires with a checked bool, which would otherwise
        # sneak into `close` and make Ok behave like Apply. The lambda drops it
        # so Ok closes and Apply stays open.
        self.pushButton_ok.clicked.connect(lambda: self._confirm(close=True))
        self.pushButton_apply.clicked.connect(lambda: self._confirm(close=False))
        self.pushButton_cancel.clicked.connect(self._cancel)
        self.lineEdit_selected_ids.returnPressed.connect(self._suppress_callback)
        app().main_window.selection.selection_changed.connect(self._geometry_selection_callback)

    def _populate_table(self):
        all_ids = sorted(self.suppressed_volume_ids | self.pending_ids)
        self.tableWidget_local_mesh_size_control_data.setRowCount(len(all_ids))

        for row, vol_id in enumerate(all_ids):
            id_item = QTableWidgetItem(str(vol_id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableWidget_local_mesh_size_control_data.setItem(row, 0, id_item)

            if vol_id in self.previously_suppressed_ids:
                status = "Suppressed"
            elif vol_id in self._configured_ids:
                status = "Awaiting regeneration"
            else:
                status = "Pending"

            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableWidget_local_mesh_size_control_data.setItem(row, 1, status_item)

    def _suppress_callback(self):
        text = self.lineEdit_selected_ids.text().strip()
        if not text:

            return

        try:
            new_ids = [int(_id.strip()) for _id in text.split(",") if _id.strip()]
        except ValueError:
            return

        if not new_ids:
            return

        mesh = app().project.model.mesh
        if mesh is None:
            return

        _, error_data = mesh.check_selected_ids(new_ids, selection="volumes")
        if error_data is not None:
            return

        for vol_id in new_ids:
            if vol_id not in self.previously_suppressed_ids:
                self.pending_ids.add(vol_id)

        self.suppressed_volume_ids = self.previously_suppressed_ids | self.pending_ids

        self.lineEdit_selected_ids.clear()
        self.last_synced_ids.clear()

        self._populate_table()
        app().main_window.entity_visibility.hide_volumes(self.pending_ids)

    def _unsuppress_callback(self):
        current_row = self.tableWidget_local_mesh_size_control_data.currentRow()
        if current_row < 0:
            return

        id_item = self.tableWidget_local_mesh_size_control_data.item(current_row, 0)
        if id_item is None:
            return

        vol_id = int(id_item.text())

        if vol_id in self.pending_ids:
            self.pending_ids.discard(vol_id)
        elif vol_id in self.previously_suppressed_ids:
            self.previously_suppressed_ids.discard(vol_id)

        self.suppressed_volume_ids = self.previously_suppressed_ids | self.pending_ids
        self._populate_table()
        app().main_window.entity_visibility.unhide_all()
        if self.pending_ids:
            app().main_window.entity_visibility.hide_volumes(self.pending_ids)

    def _geometry_selection_callback(self):
        selection = app().main_window.selection
        current_volumes = selection.geometry_volumes
        if not current_volumes:
            self.lineEdit_selected_ids.setText("")
            self.last_synced_ids.clear()
            return

        if current_volumes == self._previous_volume_selection:
            return

        self._previous_volume_selection = set(current_volumes)

        current_ids = set(self._get_selected_ids())
        manually_edited = current_ids != self.last_synced_ids

        if manually_edited:
            merged_ids = set(current_volumes) | current_ids
            self.last_synced_ids = set(merged_ids)
        else:
            merged_ids = set(current_volumes)
            self.last_synced_ids = set(current_volumes)

        text = ", ".join(str(i) for i in sorted(merged_ids))
        self.lineEdit_selected_ids.setText(text)

    def _get_selected_ids(self) -> list[int]:
        text = self.lineEdit_selected_ids.text().strip()
        if not text:
            return []

        try:
            return [int(_id.strip()) for _id in text.split(",") if _id.strip()]
        except ValueError:
            return []

    def _check_properties_on_suppressed_volumes(self) -> bool:
        properties = app().project.model.properties
        if properties is None:
            return True

        surfaces_from_volume = app().project.model.mesh.surfaces_from_volume
        affected_surfaces = set()
        for vol_id in self.suppressed_volume_ids:
            affected_surfaces |= set(surfaces_from_volume.get(vol_id, []))

        if not affected_surfaces:
            return True

        assigned_properties = properties.get_properties_from_surfaces(affected_surfaces)
        if not assigned_properties:
            return True

        prop_names = sorted(set(prop_name for prop_name, _ in assigned_properties))
        message = (
            f"The following properties are assigned to surfaces of the selected volumes:\n\n"
            f"  {', '.join(prop_names)}\n\n"
            "Suppressing these volumes will remove all associated mesh data while the volume is suppressed.\n\n"
            "Do you want to proceed?"
        )

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Proceed",
        }

        return self._show_internal_confirmation(
            "Volume suppression warning",
            message,
            buttons_config=buttons_config,
        )

    def _confirm(self, close:bool):
        # can't use a default value on close (line 66)
        if not self._check_properties_on_suppressed_volumes():
            self.show()
            return

        new_ids = self.get_suppressed_volume_ids()
        mesh_setup = app().project.model.mesh_setup

        if mesh_setup is None:
            mesh_setup = MeshSetup(suppressed_volume_ids=new_ids)
            changed = bool(new_ids)
        else:
            changed = sorted(mesh_setup.suppressed_volume_ids) != new_ids
            mesh_setup.suppressed_volume_ids = new_ids

        regenerate_now = False

        if changed:
            app().project.configure_mesh(mesh_setup)
            self.complete = True
            model_setup_items = app().main_window.model_setup_widget.model_setup_items
            model_setup_items.update_items_appearance()

            regenerate_now = self._show_internal_confirmation(
                "Mesh regeneration required",
                "The volume suppression setup has been modified. The current "
                "mesh must be regenerated for these changes to take effect.\n\n"
                "Do you want to regenerate the mesh now?",
                buttons_config={
                    "left_button_label": "Later",
                    "right_button_label": "Regenerate",
                },
            )

        if close:
            self._close_dialog()

        if regenerate_now:
            generate_mesh_and_finalize()

        if not close and changed:
            self._refresh_after_regeneration()

    def _refresh_after_regeneration(self):
        mesh = app().project.model.mesh
        mesh_setup = app().project.model.mesh_setup

        applied = set(mesh.suppressed_volumes) if mesh else set()
        configured = set(mesh_setup.suppressed_volume_ids) if mesh_setup else set()

        self.previously_suppressed_ids = applied
        self._configured_ids = configured
        self.pending_ids = configured - applied
        self.suppressed_volume_ids = applied | self.pending_ids
        self._populate_table()

    def _close_dialog(self):
        app().main_window.selection.volume_selection_mode = False
        self.keep_window_open = False
        self.close()

    def _show_internal_confirmation(self, title: str, message: str, buttons_config: dict) -> bool:
        """Shows a confirmation dialog while keeping this window hidden."""
        self.hide()
        confirmation = GetUserConfirmationInput(title, message, buttons_config=buttons_config)
        return confirmation._continue

    def _cancel(self):
        self._close_dialog()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._cancel()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        app().main_window.selection.volume_selection_mode = False
        self.keep_window_open = False
        super().closeEvent(event)

    def get_suppressed_volume_ids(self) -> list[int]:
        return sorted(self.suppressed_volume_ids)
