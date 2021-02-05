import glm 
import math
import random
from ray import *

class Camera:
    def __init__(self):
        self.position = glm.vec3(278, 273, -800)
        self.direction = glm.vec3(0,0,1)
        self.up = glm.vec3(0,1,0)
        self.focal_length = 0.035
        self.width = 0.025
        self.height = 0.025

    def generate_ray(self, pixel_x, pixel_y, image_width, image_height):
        image_aspect_ratio = float(image_width) / float(image_height)

        alpha = 2.0 * math.atan(1.0 / (2.0 * self.focal_length)) 

        s_1 = random.uniform(0,1)
        s_2 = random.uniform(0,1)

        pixel_ndc_x = (pixel_x + s_1) / image_width
        pixel_ndc_y = (pixel_y + s_2) / image_height 

        pixel_screen_x = 2.0 * pixel_ndc_x - 1.0
        pixel_screen_y = 2.0 * pixel_ndc_y - 1.0

        pixel_camera_x = pixel_screen_x * self.width * image_aspect_ratio * math.tan(alpha/2)
        pixel_camera_y = pixel_screen_y * self.height * math.tan(alpha/2)

        camera_point = glm.vec3(pixel_camera_x, pixel_camera_y, -1.0)
        return Ray(self.position, glm.normalize(-camera_point))