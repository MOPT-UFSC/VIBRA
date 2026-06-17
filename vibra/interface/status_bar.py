from PySide6.QtWidgets import QLabel, QStatusBar

from vibra import app


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)

        self._create_qt_variables()
        self._config_widgets()
        self._config_sizes()

    def _create_qt_variables(self):
        self.selected_points_label = QLabel("Selected pooints:\t")
        self.selected_lines_label = QLabel("Selected lines:\t")
        self.selected_faces_label = QLabel("Selected surfaces:\t")
        self.selected_volumes_label = QLabel("Selected volumes:\t")
        self.points_label = QLabel("Points: \t")
        self.lines_label = QLabel("Lines: \t")
        self.surfaces_label = QLabel("Faces: \t")
        self.volumes_label = QLabel("Volumes: \t")
        self.nodes_label = QLabel("Nodes: \t")
        self.solid_elements_label = QLabel("Solid elements: \t")
        self.surface_elements_label = QLabel("Face elements: \t")
    
    def _config_widgets(self):
        # adding label to status bar
        self.addWidget(self.selected_lines_label)
        self.addWidget(self.selected_points_label)
        self.addWidget(self.selected_faces_label)
        self.addWidget(self.selected_volumes_label)
        self.addWidget(self.points_label)
        self.addWidget(self.lines_label)
        self.addWidget(self.surfaces_label)
        self.addWidget(self.volumes_label)
        self.addWidget(self.nodes_label)
        self.addWidget(self.surface_elements_label)
        self.addWidget(self.solid_elements_label)
        self.reset_labels_visibility()
    
    def _config_sizes(self):
        self.selected_points_label.setFixedWidth(160)
        self.selected_lines_label.setFixedWidth(160)
        self.selected_faces_label.setFixedWidth(160)
        self.selected_volumes_label.setFixedWidth(160)
        self.points_label.setFixedWidth(100)
        self.lines_label.setFixedWidth(100)
        self.surfaces_label.setFixedWidth(100)
        self.volumes_label.setFixedWidth(100)
        self.nodes_label.setFixedWidth(140)
        self.surface_elements_label.setFixedWidth(180)
        self.solid_elements_label.setFixedWidth(180)

    def set_selection(self, points, lines, faces, volumes):
        self.reset_selections_visibility()
        if points:
            self.selected_points_label.setVisible(True)
            self.show_points(points)
        if lines:
            self.selected_lines_label.setVisible(True)
            self.show_lines(lines)
        if faces:
            self.selected_faces_label.setVisible(True)
            self.show_faces(faces)
        if volumes:
            self.selected_volumes_label.setVisible(True)
            self.show_volumes(volumes)

    def show_points(self, n_points):
        str_points = ", ".join([str(i) for i in n_points])
        if len(n_points) > 1:
            if len(n_points) <= 3:
                self.selected_points_label.setText(f"Selected points: {str_points}")
            else:
                self.selected_points_label.setText(f"Selected points: [{len(n_points)}]")
        else:
            self.selected_points_label.setText(f"Selected point: {str_points}")

    def show_lines(self, n_lines):
        str_lines = ", ".join([str(i) for i in n_lines])
        if len(n_lines) > 1:
            if len(n_lines) <= 3:
                self.selected_lines_label.setText(f"Selected lines: {str_lines}")
            else:
                self.selected_lines_label.setText(f"Selected lines: [{len(n_lines)}]")
        else:
            self.selected_lines_label.setText(f"Selected line: {str_lines}")

    def show_faces(self, n_faces):
        str_faces = ", ".join([str(i) for i in n_faces])
        if len(n_faces) > 1:
            if len(n_faces) <= 3:
                self.selected_faces_label.setText(f"Selected surfaces: {str_faces}")
            else:
                self.selected_faces_label.setText(f"Selected surfaces: [{len(n_faces)}]")
        else:
            self.selected_faces_label.setText(f"Selected surface: {str_faces}")

    def show_volumes(self, n_volumes):
        str_volumes = ", ".join([str(i) for i in n_volumes])
        if len(n_volumes) > 1:
            if len(n_volumes) <= 3:
                self.selected_volumes_label.setText(f"Selected volumes: {str_volumes}")
            else:
                self.selected_volumes_label.setText(f"Selected volumes: [{len(n_volumes)}]")
        else:
            self.selected_volumes_label.setText(f"Selected volume: {str_volumes}")

    def update_mesh_information(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        nodes, surface_elements, solid_elements = mesh.get_mesh_info()
        self.nodes_label.setText(f"Nodes: {nodes}")
        self.surface_elements_label.setText(f"Surface elements: {surface_elements}")
        self.solid_elements_label.setText(f"Solid elements: {solid_elements}")
        self.reset_mesh_info_visibility(key=True)

    def update_geometry_information(self):
        mesh = app().project.model.mesh
        if mesh is None:
            return

        geometry_info = mesh.geometry_information

        points = geometry_info.get("points", "--")
        if isinstance(points, list):
            points = len(points)

        lines = geometry_info.get("lines", "--")
        if isinstance(lines, list):
            lines = len(lines)

        surfaces = geometry_info.get("surfaces", "--")
        if isinstance(surfaces, list):
            surfaces = len(surfaces)

        volumes = geometry_info.get("volumes", "--")
        if isinstance(volumes, list):
            volumes = len(volumes)

        self.points_label.setText(f"Points: {points}")
        self.lines_label.setText(f"Curves: {lines}")
        self.surfaces_label.setText(f"Faces: {surfaces}")
        self.volumes_label.setText(f"Volumes: {volumes}")
        self.reset_geometry_info_visibility(key=True)

    def reset_labels_visibility(self):
        self.reset_geometry_info_visibility()
        self.reset_selections_visibility()
        self.reset_mesh_info_visibility()

    def reset_geometry_info_visibility(self, key=False):
        self.points_label.setVisible(key)
        self.lines_label.setVisible(key)
        self.surfaces_label.setVisible(key)
        self.volumes_label.setVisible(key)

    def reset_selections_visibility(self, key=False):
        self.selected_lines_label.setVisible(key)
        self.selected_points_label.setVisible(key)
        self.selected_faces_label.setVisible(key)
        self.selected_volumes_label.setVisible(key)

    def reset_mesh_info_visibility(self, key=False):
        self.nodes_label.setVisible(key)
        self.surface_elements_label.setVisible(key)
        self.solid_elements_label.setVisible(key)

    def clear_selections(self):
        self.set_selection([], [], [], [])