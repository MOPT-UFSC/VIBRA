from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QTableWidgetItem

from vibra import app
from vibra.interface.general.get_user_confirmation_input import GetUserConfirmationInput
from vibra.interface.ui_generated.model.general.volume_suppression_dialog_ui import (
    VolumeSuppressionDialog_UI,
)


class VolumeSuppressionDialog(VolumeSuppressionDialog_UI):
    def __init__(self, suppressed_volume_ids: list[int], parent=None):
        super().__init__(parent)

        self.previously_suppressed_ids = set(suppressed_volume_ids)
        self.suppressed_volume_ids = set(suppressed_volume_ids)
        self.pending_ids: set[int] = set()
        self.last_synced_ids: set[int] = set()
        self._previous_volume_selection: set[int] = set()

        self._config_window()
        self._configure_table()
        self._create_connections()
        self._populate_table()

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
        self.pushButton_add.clicked.connect(self._add_callback)
        self.pushButton_delete.clicked.connect(self._delete_callback)
        self.pushButton_confirm.clicked.connect(self._confirm)
        self.pushButton_apply.clicked.connect(self._confirm)
        self.pushButton_cancel.clicked.connect(self._cancel)
        self.lineEdit_selected_ids.returnPressed.connect(self._add_callback)
        app().main_window.selection.selection_changed.connect(
            self._geometry_selection_callback
        )

    def _populate_table(self):
        all_ids = sorted(self.suppressed_volume_ids | self.pending_ids)
        self.tableWidget_local_mesh_size_control_data.setRowCount(len(all_ids))

        for row, vol_id in enumerate(all_ids):
            id_item = QTableWidgetItem(str(vol_id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableWidget_local_mesh_size_control_data.setItem(row, 0, id_item)

            status = "Suppressed" if vol_id in self.previously_suppressed_ids else "Pending"
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableWidget_local_mesh_size_control_data.setItem(row, 1, status_item)

    def _add_callback(self):
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

    def _delete_callback(self):
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
            "Suppressing these volumes will remove all associated mesh data. "
            "These properties will become invalid and must be reassigned later.\n\n"
            "Do you want to proceed?"
        )

        buttons_config = {
            "left_button_label": "Cancel",
            "right_button_label": "Proceed",
        }

        confirmation = GetUserConfirmationInput(
            "Volume suppression warning",
            message,
            buttons_config=buttons_config,
        )

        return confirmation._continue

    def _confirm(self):
        if not self._check_properties_on_suppressed_volumes():
            return

        app().main_window.selection.volume_selection_mode = False
        self.accept()

    def _cancel(self):
        app().main_window.selection.volume_selection_mode = False
        self.reject()

    def closeEvent(self, event):
        app().main_window.selection.volume_selection_mode = False
        super().closeEvent(event)

    def get_suppressed_volume_ids(self) -> list[int]:
        return sorted(self.suppressed_volume_ids)
