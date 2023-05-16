class Mesh:
    def __init__(self):
        self.points = [(0, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.lines = [(0, 1), (1, 2), (2, 0)]
        self.faces = [(0, 1, 2)]

        self.points_data = dict()
        self.lines_data = dict()
        self.faces_fata = dict()

    @classmethod
    def from_file(cls):
        pass

    def set_points(self, points):
        pass

    def set_lines(self, lines):
        pass

    def set_faces(self, faces):
        pass

    def set_points_data(self, name, array):
        pass

    def set_lines_data(self, name, array):
        pass

    def set_faces_data(self, name, array):
        pass