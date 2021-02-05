import glm

class Ray:
    def __init__(self, origin=glm.vec3(0), direction=glm.vec3(0,0,1)):
        self.origin = origin
        self.direction = direction