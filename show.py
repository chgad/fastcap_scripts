import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import re
import numpy as np
import argparse


AXIS = {
    "x": (1, 0, 0),
    "y": (0, 1, 0),
    "z": (0, 0, 1)
}


def prep_points(string_list):
    final_list = []
    for index, point in enumerate(string_list):
        # print(index, point)
        splitted = point.split(" ")
        final_list.append(tuple(map(lambda x: float(x), splitted)))
    return final_list


def get_center(quads):
    max_vec = np.min(np.min(quads, axis=0), axis=0)
    min_vec = np.max(np.max(quads, axis=0), axis=0)
    return 0.5 * (max_vec + min_vec)


def read_file(file_name):
    pattern = re.compile(r"-?[0-9]*\.[0-9e\-]* -?[0-9]*\.[0-9e\-]* -?[0-9]*\.[0-9e\-]*")
    with open(file_name, "r") as f:
        quads = [prep_points(pattern.findall(line)) for line in f.readlines() if line.startswith("Q")]

    return quads


def structure(quadrats):
    # glColor3f(0.52, 0.804, 0.918)
    # glBegin(GL_QUADS)
    #
    # for quad in quadrats:
    #     for point in quad:
    #         glVertex3fv(point)
    #
    # glEnd()
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
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
    glTranslate(*((-1)**negative_dir*10*vector))


def main(file_name):
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

    quadrats = read_file(file_name)
    center = -1*get_center(quadrats)

    key_events = {97: (rotate, {"axis": "y", "center": center, "clock_wise": 0, "angle": 10.0}),  # A-key
                  100: (rotate, {"axis": "y", "center": center, "clock_wise": 1, "angle": 10.0}),  # D-key
                  119: (rotate, {"axis": "x", "center": center, "clock_wise": 0, "angle": 10.0}),  # W-key
                  115: (rotate, {"axis": "x", "center": center, "clock_wise": 1, "angle": 10.0}),  # S-key
                  116: (rotate, {"axis": "z", "center": center, "clock_wise": 0, "angle": 10.0}),  # T-key
                  103: (rotate, {"axis": "z", "center": center, "clock_wise": 1, "angle": 10.0}),  # G-key
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
    glEnable(GL_PROGRAM_POINT_SIZE)
    gluPerspective(90, (display[0] / display[1]), 0.1, 600.0)
    glTranslate(0.0, 0.0, -100)
    glTranslate(*center)
    # glColor3f(0.52, 0.804, 0.918)
    # light_ambient = [0.2, 0.2, 0.2, 1.0]
    # light_diffuse = [1.0, 1.0, 1.0, 1.0]
    # light_specular = [0.0, 0.0, 0.0, 1.0]
    #
    # glLightfv(GL_LIGHT7, GL_AMBIENT, light_ambient)
    # glLightfv(GL_LIGHT7, GL_DIFFUSE, light_diffuse)
    # glLightfv(GL_LIGHT7, GL_SPECULAR, light_specular)
    #
    # mat_specular = [0.0, 0.0, 0.0, 1.0]
    # mat_diffuse = [0.8, 0.6, 0.4, 1.0]
    # mat_ambient = [0.8, 0.6, 0.4, 1.0]
    # mat_shininess = 20.0
    # glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    # glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    # glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    # glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

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


parser = argparse.ArgumentParser(description="Visualize FastCap2 List-Files")
parser.add_argument("file_name", metavar="f", type=str)

name_of_file = parser.parse_args().file_name
print(name_of_file)
main(name_of_file)


