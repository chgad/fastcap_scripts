
from numpy import ndarray


class FaceTranslation:
    """
    Main class to provide Translation operation in a 3D real vector space
     with euklidian metric for geometrical faces.
    """
    def __init__(self):
        self.corners = []

    def __add__(self, other):
        if not isinstance(other, ndarray):
            raise ValueError("__add__ is a translation operation. A Face can only be added with a 3D vectore")
        for vector in self.corners:
            vector += other

        return self

    def __sub__(self, other):
        if not isinstance(other, ndarray):
            raise ValueError("__sub__ is a translation operation. A Face can only be added with a 3D vectore")
        for vector in self.corners:
            vector -= other

        return self


class FaceListTranslation:
    """
    Main class to provide Translation operation in a 3D real vector space
     with euklidian metric for a list of geometrical faces.
    """

    def __init__(self):
        self.faces = []

    def __add__(self, other):
        if not isinstance(other, ndarray):
            raise ValueError("__add__ is a translation operation. A Face can only be added with a 3D vectore")
        for face in self.faces:
            face += other

        return self

    def __sub__(self, other):
        if not isinstance(other, ndarray):
            raise ValueError("__sub__ is a translation operation. A Face can only be added with a 3D vectore")
        for face in self.faces:
            face -= other

        return self


class IdtTranslation:
    """
    Main class to provide Translation operation in a 3D real vector space
     with euklidian metric for a list of geometrical faces.
    """

    def __init__(self):
        self.base = None
        self.electrodes = None
        self.diel_faces = None

    def __add__(self, other):
        if not isinstance(other, ndarray):
            raise ValueError("__add__ is a translation operation. A Face can only be added with a 3D vectore")
        for elec in self.electrodes:
            elec + other
        self.base + other
        self.diel_faces + other

        return self

    def __sub__(self, other):
        if not isinstance(other, ndarray):
            raise ValueError("__add__ is a translation operation. A Face can only be added with a 3D vectore")
        for elec in self.electrodes:
            elec - other
        self.base - other
        self.diel_faces - other

        return self