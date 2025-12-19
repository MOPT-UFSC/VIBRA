import tempfile

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QDialog, QHBoxLayout
from PySide6.QtCore import Qt

from simple_cad.service.geometry_service import GeometryCollection, exportSolidsToStep
from simple_cad.view.components.occ_window import OCCWindowWithViewToolBar


class SimpleCAD(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Select geometry volumes to create a model")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize services
        self.geometry_collection = GeometryCollection()
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create horizontal layout for control panel and 3D window
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Setup control panel for volume selection
        self._setup_volume_selection_control_panel()
        content_layout.addWidget(self.control_panel)
        
        # Create the main widget
        self.occ_window = OCCWindowWithViewToolBar(
            self,
            self.geometry_collection,
        )
        content_layout.addWidget(self.occ_window, 1)
        
        main_layout.addLayout(content_layout)
        
        # Store current geometry for selection
        self._current_geometry = None
        
        # Connect to volume selection handler
        if self.occ_window.volume_selection_handler:
            self.occ_window.volume_selection_handler.set_selection_changed_callback(
                self._on_selection_changed
            )
        self.geometry_file = None
    
    def _setup_volume_selection_control_panel(self):
        """Setup control panel widget for volume selection."""
        self.control_panel = QWidget()
        self.control_panel.setFixedWidth(280)
        
        layout = QVBoxLayout(self.control_panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Info label
        self.info_label = QLabel("Click on volumes in 3D view to select/deselect them.\nSelected volumes will turn yellow.")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # Selection count label
        self.count_label = QLabel("Selected: 0 volume(s)")
        layout.addWidget(self.count_label)
        
        # Export button
        self.export_button = QPushButton("Create model from selection")
        self.export_button.setToolTip("Create model from selected volumes")
        self.export_button.clicked.connect(self._export_selected_volumes)

        self.export_all_button = QPushButton("Create model with all volumes")
        self.export_all_button.setToolTip("Create model with all volumes")
        self.export_all_button.clicked.connect(lambda: self.close())
        
        layout.addWidget(self.export_button)
        layout.addWidget(self.export_all_button)
        
        layout.addStretch()
        
        # Initially hidden
        self.control_panel.hide()
    
    def _on_selection_changed(self, selected_count, total_count):
        """Callback when volume selection changes."""
        self.count_label.setText(f"Selected: {selected_count} of {total_count} volume(s)")
    
    def importStep(self, file_path):
        """Import a STEP file and add it to the geometry collection."""
        
        if file_path:
            try:
                # Add to geometry collection
                geometry = self.geometry_collection.loadStep(file_path)
                self._current_geometry = geometry
                
                # Start volume selection mode
                self.occ_window.startVolumeSelectionMode(self._current_geometry)
                
                # Show control panel
                self.control_panel.show()
                
                # Fit the view
                self.occ_window.occ_window.display.FitAll()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to import STEP file:\n{str(e)}"
                )
    
    def exportVolumes(self):
        """Export selected volumes from the imported geometry."""
        if not self._current_geometry:
            QMessageBox.warning(
                self,
                "No Geometry",
                "Please import a STEP file first."
            )
            return
        
        # Start volume selection mode
        self.occ_window.startVolumeSelectionMode(self._current_geometry)
        
        # Show control panel
        self.control_panel.show()
    
    def _export_selected_volumes(self):
        """Export selected volumes to STEP file."""
        if not self.occ_window.volume_selection_handler:
            return
        
        selected_volumes = self.occ_window.volume_selection_handler.get_selected_volumes()
        
        if not selected_volumes:
            QMessageBox.warning(
                self,
                "No Volumes Selected",
                "Please select at least one volume to export."
            )
            return

        temp_file = tempfile.NamedTemporaryFile(suffix='.step', delete=False)
        temp_file_path = temp_file.name
        
        success = exportSolidsToStep(selected_volumes, temp_file_path)
        if success:
            self.geometry_file = temp_file_path
            self.occ_window.volume_selection_handler.deactivate()
            self.control_panel.hide()
            # Close the dialog
            self.close()
        else:
            QMessageBox.critical(
                self,
                "Export Failed",
                "Failed to export selected volumes."
            )
