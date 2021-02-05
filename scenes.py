from cameras import *
from materials import *
from shapes import *

class Scene:
    def __init__(self, camera, shapes):
        self.camera = camera
        self.shapes = shapes


class CornellBox(Scene):
    def __init__(self):
        camera = Camera()

        shapes = [
            # Floor - White
            Rectangle(glm.vec3(552.8, 0.0, 0.0),
                      glm.vec3(0),
                      glm.vec3(0,0, 559.2),
                      glm.vec3(549.6, 0.0, 559.2),
                      DiffuseMaterial(diffuse = glm.vec3(0.9))),

            # Left wall - Red
            Rectangle(glm.vec3(552.8,   0.0,   0.0),
                      glm.vec3(549.6,   0.0, 559.2),
                      glm.vec3(556.0, 548.8, 559.2),
                      glm.vec3(556.0, 548.8,   0.0),
                      DiffuseMaterial(diffuse = glm.vec3(0.9,0.05,0.05))),

            # Right wall - Green
            Rectangle(glm.vec3(0.0,  0.0, 559.2),
                      glm.vec3(0.0,   0.0,   0.0),
                      glm.vec3(0.0, 548.8,   0.0),
                      glm.vec3(0.0, 548.8, 559.2),
                      DiffuseMaterial(diffuse = glm.vec3(0.05,0.9,0.05))),

            # Back wall - White
            Rectangle(glm.vec3(549.6, 0.0, 559.2),
                      glm.vec3(0.0,  0.0, 559.2),
                      glm.vec3(0.0, 548.8, 559.2),
                      glm.vec3(556.0, 548.8, 559.2),
                      DiffuseMaterial(diffuse = glm.vec3(0.9))),

            # Ceiling - White
            Rectangle(glm.vec3(556.0, 548.8, 0.0),
                      glm.vec3(556.0, 548.8, 559.2),
                      glm.vec3(0.0, 548.8, 559.2),
                      glm.vec3(0.0, 548.8, 0.0),
                      DiffuseMaterial(diffuse = glm.vec3(0.9))),

            # Light
            Rectangle(glm.vec3(343.0, 548.75, 227.0),
                      glm.vec3(343.0, 548.75, 332.0),
                      glm.vec3(213.0, 548.75, 332.0),
                      glm.vec3(213.0, 548.75, 227.0),
                      DiffuseMaterial(diffuse = glm.vec3(0), emission = glm.vec3(50, 50, 50))),

            # Tall box - White
            Mesh([glm.vec3(423.0, 330.0, 247.0),
                  glm.vec3(265.0, 330.0, 296.0),
                  glm.vec3(314.0, 330.0, 456.0),
                  glm.vec3(472.0, 330.0, 406.0),

                  glm.vec3(423.0,   0.0, 247.0),
                  glm.vec3(423.0, 330.0, 247.0),
                  glm.vec3(472.0, 330.0, 406.0),
                  glm.vec3(472.0,   0.0, 406.0),

                  glm.vec3(472.0,   0.0, 406.0),
                  glm.vec3(472.0, 330.0, 406.0),
                  glm.vec3(314.0, 330.0, 456.0),
                  glm.vec3(314.0,   0.0, 456.0),

                  glm.vec3(314.0,   0.0, 456.0),
                  glm.vec3(314.0, 330.0, 456.0),
                  glm.vec3(265.0, 330.0, 296.0),
                  glm.vec3(265.0,   0.0, 296.0),

                  glm.vec3(265.0,   0.0, 296.0),
                  glm.vec3(265.0, 330.0, 296.0),
                  glm.vec3(423.0, 330.0, 247.0),
                  glm.vec3(423.0,   0.0, 247.0)],

                  [0, 1, 2, 0, 2, 3,
                  4, 5, 6, 4, 6, 7,
                  8, 9, 10, 8, 10, 11,
                  12, 13, 14, 12, 14, 15,
                  16, 17, 18, 16, 18, 19],

                  DiffuseMaterial(diffuse = glm.vec3(0.7))),

            # Short box - White
            Mesh([glm.vec3(130.0, 165.0, 65.0),
                  glm.vec3(82.0, 165.0, 225.0),
                  glm.vec3(240.0, 165.0, 272.0),
                  glm.vec3(290.0, 165.0, 114.0),

                  glm.vec3(290.0, 0.0, 114.0),
                  glm.vec3(290.0, 165.0, 114.0),
                  glm.vec3(240.0, 165.0, 272.0),
                  glm.vec3(240.0,   0.0, 272.0),

                  glm.vec3(130.0,   0.0,  65.0),
                  glm.vec3(130.0, 165.0,  65.0),
                  glm.vec3(290.0, 165.0, 114.0),
                  glm.vec3(290.0,   0.0, 114.0),

                  glm.vec3(82.0,   0.0, 225.0),
                  glm.vec3(82.0, 165.0, 225.0),
                  glm.vec3(130.0, 165.0,  65.0),
                  glm.vec3(130.0,   0.0,  65.0),

                  glm.vec3(240.0,   0.0, 272.0),
                  glm.vec3(240.0, 165.0, 272.0),
                  glm.vec3(82.0, 165.0, 225.0),
                  glm.vec3(82.0,   0.0, 225.0)],

                  [0, 1, 2, 0, 2, 3,
                   4, 5, 6, 4, 6, 7,
                   8, 9, 10, 8, 10, 11,
                   12, 13, 14, 12, 14, 15,
                   16, 17, 18, 16, 18, 19],

                DiffuseMaterial(diffuse = glm.vec3(0.7)))
            ]
        Scene.__init__(self, camera, shapes)
