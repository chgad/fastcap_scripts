# This File is for Testing of the Capability of prepareing Blender PyAPI conform
# Lists for Vertices and Faces.
from faces import GeomFace, GeomFaceList
from structures import Cuboid
import numpy as np


# First we test the capability of GeomFace class
# With 4 corners (Rectangle)

def test_geomface_blender_lists():
    # parameter definition for a Cube
    # length --> dist in y , width --> dist in x
    length, width= 1.0, 1.0
    # Definition of a 1x1 Face in the z-plane
    # Corners defined in clockwise order
    zero = np.array([0.0, 0.0, 0.0])
    one = np.array([0.0, length, 0.0])
    two = np.array([width, length, 0.0])
    three = np.array([width, 0.0, 0.0])
    face = GeomFace(vertice_cnt=4, corners=[zero, one, two, three])
    assert hasattr(face, "prep_blender_data")
    assert callable(getattr(face ,"prep_blender_data"))
    assert isinstance(getattr(face, "prep_blender_data")(), tuple)
    assert len(getattr(face, "prep_blender_data")()) == 2
    assert len(getattr(face, "prep_blender_data")()[0]) == face.vertice_cnt
    assert len(getattr(face, "prep_blender_data")()[1]) == face.vertice_cnt

# Second we test the Capability of GeomFaceList class


def test_geomfacelist_blender_lists():
    length, width = 1.0, 1.0
    # Definition of a 1x1 Face in the z-plane
    # Corners defined in clockwise order
    zero = np.array([0.0, 0.0, 0.0])
    one = np.array([0.0, length, 0.0])
    two = np.array([width, length, 0.0])
    three = np.array([width, 0.0, 0.0])
    face = GeomFace(vertice_cnt=4, corners=[zero, one, two, three])

    # generate list of 3 faces translated by (1.0, 1.0, 1.0)
    dummy_list = []
    for i in range(3):
        dummy_list.append(face.copy() + np.array([i*1.0, 0.0, 0.0]))

    assert len(dummy_list) == 3

    face_list = GeomFaceList(dummy_list)
    expected_vertices = [
        # First plane
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        # Second plane
        np.array([1.0, 0.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
        np.array([2.0, 1.0, 0.0]),
        np.array([2.0, 0.0, 0.0]),
        # Third plane
        np.array([2.0, 0.0, 0.0]),
        np.array([2.0, 1.0, 0.0]),
        np.array([3.0, 1.0, 0.0]),
        np.array([3.0, 0.0, 0.0]),
    ]

    expected_faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
    ]

    assert hasattr(face_list, "prep_blender_data")
    assert callable(getattr(face_list, "prep_blender_data"))
    assert isinstance(getattr(face_list, "prep_blender_data")(), tuple)
    assert len(getattr(face_list, "prep_blender_data")()) == 2
    assert len(getattr(face_list, "prep_blender_data")()[0]) == 12
    assert len(getattr(face_list, "prep_blender_data")()[1]) == 3

    vertices, faces = face_list.prep_blender_data()

    for i, j in zip(expected_vertices, vertices):
        assert (i == j).sum() == 3

    for i, j in zip(expected_faces, faces):
        assert i == j

# Third we test the capability of Cuboid

def test_cuboid_blender_lists():
    # parameter definition
    # length --> dist in y , width --> dist in x, height --> dist in z
    length, width, height = 1.0, 1.0, 1.0
    cube = Cuboid(length=length, width=width, height=height)

    assert hasattr(cube, "prep_blender_data")
    assert callable(getattr(cube ,"prep_blender_data"))
    assert isinstance(getattr(cube, "prep_blender_data")(), tuple)
    assert len(getattr(cube, "prep_blender_data")()) == 2
    # we expect that the corners are contained multiple times (3 if exact)
    assert len(getattr(cube, "prep_blender_data")()[0]) == 24
    assert len(getattr(cube, "prep_blender_data")()[1]) == 6

    # We expect the order of the vertices/faces to be
    # front - back - left - right - bottom - top
    expected_vertices = [
        # Left Face
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 1.0, 1.0]),
        np.array([0.0, 0.0, 1.0]),
        # Right Face
        np.array([1.0, 0.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
        np.array([1.0, 1.0, 1.0]),
        np.array([1.0, 0.0, 1.0]),
        # Front Face
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 1]),
        np.array([1, 0.0, 1]),
        np.array([1, 0.0, 0.0]),
        # Back Face
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 1.0, 1.0]),
        np.array([1.0, 1.0, 1.0]),
        np.array([1.0, 1.0, 0.0]),
        # Bottom Face
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        # Top Face
        np.array([0.0, 0.0, 1.0]),
        np.array([0.0, 1.0, 1.0]),
        np.array([1.0, 1.0, 1.0]),
        np.array([1.0, 0.0, 1.0]),
    ]

    expected_faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
        (12, 13, 14, 15),
        (16, 17, 18, 19),
        (20, 21, 22, 23),
    ]
    vertices, faces = cube.prep_blender_data()

    for i, j in zip(expected_vertices, vertices):
        assert (i == j).sum() == 3

    for i, j in zip(expected_faces, faces):
        assert i == j
