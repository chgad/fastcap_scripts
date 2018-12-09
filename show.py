import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import re

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


def main(file_name):
    # 97 --> A-key --> rotation around x-axis of 90 deg
    # 100 --> D-key --> rotation around x-axis of -90 deg
    # 119 --> W-key --> rotation around y-axis of 90 deg
    # 115 --> S-key --> rotation around y-axis of -90 deg
    # 116 --> T-key --> rotation around z-axis of 90 deg
    # 103 --> G-key --> rotation around z-axis of -90 deg

    key_events = {"a": (30, 0, 1, 0),
                  "d": (-30, 0, 1, 0),
                  "w": (30, 1, 0, 0),
                  "s": (-30, 1, 0, 0),
                  "t": (30, 0, 0, 1),
                  "g": (-30, 0, 0, 1)
                  }
    quadrats = read_file(file_name)
    pygame.init()
    display = (1920, 1080)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(90, (display[0] / display[1]), 0.1, 600.0)
    glTranslate(0.0,0.0,-100.0)
    glTranslate(-46.0, -2.5, -103.5)
    one = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                glTranslate(46.0, 2.5, 3.5)
                glRotatef(*key_events.get(event.unicode))
                glTranslate(-46.0, -2.5, -3.5)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glTranslate(-46.0, -2.5, -103.5)

        structure(quadrats)
        # if one:
        #     glTranslate(-50.0, -2.5, -3.5)
        #     one = 0
        pygame.display.flip()
        pygame.time.wait(100)

file_name = "test_cond_file.txt"

main(file_name)
