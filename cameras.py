import glm 

class Camera:
    def __init__(self):
        self.position = glm.vec3(278, 273, -800)
        self.direction = glm.vec3(0,0,1)
        self.up = glm.vec3(0,1,0)
        self.focal_length = 0.035
        self.width = 0.025
        self.height = 0.025