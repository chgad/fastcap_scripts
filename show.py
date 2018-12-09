import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import re
import numpy as np


AXIS = {
    "x": (1, 0, 0),
    "y": (0, 1, 0),
    "z": (0, 0, 1)
}


def prep_points(string_list):
    final_list = []
    for point in string_list:
        splitted = point.split(" ")
        final_list.append(tuple(map(lambda x: float(x), splitted)))
    return final_list


def read_file(file_name):
    pattern = re.compile(r"-?[0-9]*\.[0-9]* -?[0-9]*\.[0-9]* -?[0-9]*\.[0-9]*")
    with open(file_name, "r") as f:
        quads = [prep_points(pattern.findall(line)) for line in f.readlines() if line.startswith("Q")]
        f.close()

    return quads


def structure(quadrats):
    glBegin(GL_LINES)
    order = [(0, 1), (1, 2), (2, 3), (3, 0)]
    for quad in quadrats:
        for i, j in order:
            glVertex3fv(quad[i])
            glVertex3fv(quad[j])

    glEnd()


def rotate(axis, center, clock_wise=0, angle=30.0):
    """

    :param axis: string (x, y or z)
    :param center: numpy array with the center of the structure to be displayed
    :param clock_wise: 0 symbolizes False, 1 True
    :param angle: angle of rotation
    :return:
    """
    if axis not in AXIS:
        pass

    glTranslate(*-center)
    glRotatef((-1) ** clock_wise * angle, *AXIS.get(axis))
    glTranslate(*center)


def translate(axis, negative_dir=1):
    vector = np.array(AXIS.get(axis))
    glTranslate(*((-1)**negative_dir*20.0*vector))


def main(file_name, center=np.array([0, 0, 0])):

    if not isinstance(center, np.ndarray):
        raise ValueError("The center must be an instance of Numpy ndarray but is {}".format(type(center)))

    # 97 --> A-key --> rotation around x-axis of 90 deg
    # 100 --> D-key --> rotation around x-axis of -90 deg
    # 119 --> W-key --> rotation around y-axis of 90 deg
    # 115 --> S-key --> rotation around y-axis of -90 deg
    # 116 --> T-key --> rotation around z-axis of 90 deg
    # 103 --> G-key --> rotation around z-axis of -90 deg

    # 276 --> left-arrow-key --> move in -x direction
    # 275 --> right-arrow-key --> move in x direction
    # 274 --> down-arrow-key --> move in -y direction
    # 273 --> up-arrow-key --> move in y direction
    # 45  --> - -key --> move in -z direction
    # 43  --> +-key --> move in z direction

    key_events = {97: (rotate, {"axis": "y", "center": center, "clock_wise": 0, "angle": 30.0}),  # A-key
                  100: (rotate, {"axis": "y", "center": center, "clock_wise": 1, "angle": 30.0}),  # D-key
                  119: (rotate, {"axis": "x", "center": center, "clock_wise": 0, "angle": 30.0}),  # W-key
                  115: (rotate, {"axis": "x", "center": center, "clock_wise": 1, "angle": 30.0}),  # S-key
                  116: (rotate, {"axis": "z", "center": center, "clock_wise": 0, "angle": 30.0}),  # T-key
                  103: (rotate, {"axis": "z", "center": center, "clock_wise": 1, "angle": 30.0}),  # G-key
                  276: (translate, {"axis": "x", "negative_dir": 1}),  # left-arrow-key
                  275: (translate, {"axis": "x", "negative_dir": 0}),  # right-arrow-key
                  274: (translate, {"axis": "y", "negative_dir": 1}),  # down-arrow-key
                  273: (translate, {"axis": "y", "negative_dir": 0}),  # up-arrow-key
                  45: (translate, {"axis": "z", "negative_dir": 1}),  # - -key
                  43: (translate, {"axis": "z", "negative_dir": 0})  # +-key
                  }

    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    quadrats = read_file(file_name)

    gluPerspective(90, (display[0] / display[1]), 0.1, 600.0)
    glTranslate(0.0, 0.0, -100.0)
    glTranslate(*center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 27:  # 27 --> ESC-key --> Stop programm
                    pygame.quit()
                    quit()
                try:
                    func, args = key_events.get(event.key)
                    func(**args)
                except TypeError:
                    pass

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        structure(quadrats)
        pygame.display.flip()
        pygame.time.wait(100)


name_of_file = "test_cond_file.txt"

main(name_of_file, center=np.array([-46.0, -2.5, -3.5]))
