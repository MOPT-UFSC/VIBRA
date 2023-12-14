from PyQt5.QtWidgets import QLabel, QStatusBar


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.points_label = QLabel("Selected Points:\t")
        self.lines_label = QLabel("Selected Lines:\t")
        self.faces_label = QLabel("Selected Faces:\t")
        self.volumes_label = QLabel("Selected Volumes:\t")
        self.nodes_label = QLabel("Nodes: \t")
        self.solid_elements_label = QLabel("Solid Elements: \t")
        self.face_elements_label = QLabel("Face Elements: \t")

        # adding label to status bar
        self.addWidget(self.lines_label)
        self.addWidget(self.points_label)
        self.addWidget(self.faces_label)
        self.addWidget(self.volumes_label)
        self.addWidget(self.nodes_label)
        self.addWidget(self.face_elements_label)
        self.addWidget(self.solid_elements_label)

        self.faces_label.setFixedWidth(160)
        self.points_label.setFixedWidth(160)
        self.lines_label.setFixedWidth(160)
        self.volumes_label.setFixedWidth(160)
        self.nodes_label.setFixedWidth(140)
        self.face_elements_label.setFixedWidth(160)
        self.solid_elements_label.setFixedWidth(160)

    def set_selection(self, points, lines, faces, volumes):
        self.show_points(points)
        self.show_lines(lines)
        self.show_faces(faces)
        self.show_volumes(volumes)

    def show_points(self, n_points):
        str_points = ", ".join([str(i) for i in n_points])
        if len(n_points) > 1:
            if len(n_points) <= 3:
                self.points_label.setText(f"Selected Points: {str_points}")
            else:
                self.points_label.setText(f"Selected Points: [{len(n_points)}]")
        else:
            self.points_label.setText(f"Selected Point: {str_points}")

    def show_lines(self, n_lines):
        str_lines = ", ".join([str(i) for i in n_lines])
        if len(n_lines) > 1:
            if len(n_lines) <= 3:
                self.lines_label.setText(f"Selected Lines: {str_lines}")
            else:
                self.lines_label.setText(f"Selected Lines: [{len(n_lines)}]")
        else:
            self.lines_label.setText(f"Selected Line: {str_lines}")

    def show_faces(self, n_faces):
        str_faces = ", ".join([str(i) for i in n_faces])
        if len(n_faces) > 1:
            if len(n_faces) <= 3:
                self.faces_label.setText(f"Selected Faces: {str_faces}")
            else:
                self.faces_label.setText(f"Selected Faces: [{len(n_faces)}]")
        else:
            self.faces_label.setText(f"Selected Face: {str_faces}")

    def show_volumes(self, n_volumes):
        str_volumes = ", ".join([str(i) for i in n_volumes])
        if len(n_volumes) > 1:
            if len(n_volumes) <= 3:
                self.volumes_label.setText(f"Selected Volumes: {str_volumes}")
            else:
                self.volumes_label.setText(f"Selected Volumes: [{len(n_volumes)}]")
        else:
            self.volumes_label.setText(f"Selected Volume: {str_volumes}")

    def update_mesh_information(self, nodes, face_elements, solid_elements):
        self.update_number_of_nodes(nodes)
        self.update_number_of_face_elements(face_elements)
        self.update_number_of_solid_elements(solid_elements)

    def update_number_of_nodes(self, number_of_nodes):
        self.nodes_label.setText(f"Nodes: {number_of_nodes}")

    def update_number_of_face_elements(self, number_of_face_elements):
        self.face_elements_label.setText(f"Face Elements: {number_of_face_elements}")

    def update_number_of_solid_elements(self, number_of_solid_elements):
        self.solid_elements_label.setText(f"Solid Elements: {number_of_solid_elements}")

    def clear_selections(self):
        self.set_selection([], [], [], [])
