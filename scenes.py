from cameras import *
from materials import *
from shapes import *
from ray import *

class Scene:
    def __init__(self, camera, shapes):
        self.camera = camera
        self.shapes = shapes
  
    def name(self):
        return ""

    def find_hit(self, ray):
        closest_hit = 10000000000.0
        final_hit = (-1, None, None)
        for shape in self.shapes:
            hit = shape.intersect(ray)
            if hit[0] > 0 and hit[0] < closest_hit:
                closest_hit = hit[0]
                final_hit = hit

        return final_hit

    def trace_path(self, ray, depth):
        # We apply russian roulette to the current ray on the path,
        # increasing the termination probability with each new level of depth.
        # If the ray is not terminated, its contribution is weighted by the
        # inverse of the termination probability, ensuring that we keep the
        # final radiance unbiased without having to set a predetermined
        # bounce depth. We always do at least 5 bounces though before starting
        # russian roulette to speed up convergence.
        termination_probability = 0.0 if depth <= 5 else 1.0 - math.pow(0.9, depth)
        terminate = random.uniform(0, 1)
        if terminate <= termination_probability:
            return glm.vec3(0)
    
        # Try to find an intersection between the ray and the scene geometry.
        # Stop traversing and return black if nothing is hit.
        t, hit_normal, material = self.find_hit(ray)
        if t == -1.0:
            return glm.vec3(0)

<<<<<<< HEAD
=======
        # Grab the material emittance and calculate the hit point.
>>>>>>> 76b6aeeedd5e4213f4dda0f0babf5fb16e59d0d7
        emittance = material.emission()
        hit_point = ray.origin + t*ray.direction

        # Pick a new ray direction which depends on the properties of the given material.
        newRay, pdf = material.sample_ray(ray, hit_normal, hit_point)
        assert pdf >= 0.000001 and pdf <= 1.0

        # The percentage of light transmitted between the incoming and outgoing ray directions.
        # This changes depending on the type of material.
        brdf = material.brdf(-ray.direction, newRay.direction, hit_normal, hit_point)

        # Recurse with the new ray and continue accumulating radiance.
        incoming_light = self.trace_path(newRay, depth + 1) / (1.0 - termination_probability)

        # The integrand is emittance + BRDF * cosTheta * light.
        return emittance + brdf * glm.dot(newRay.direction, hit_normal) * incoming_light / pdf


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
    
    def name(self):
        return "CornellBox"


class MirrorBalls(Scene):
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

            # Large Mirror Ball
<<<<<<< HEAD
            Sphere(radius=150, center=glm.vec3(230, 150, 200), material=MirrorMaterial())
=======
            Sphere(radius=150, center=glm.vec3(370, 150, 350), material=MirrorMaterial()),
>>>>>>> 76b6aeeedd5e4213f4dda0f0babf5fb16e59d0d7

            # Small Mirror ball
            Sphere(radius=100, center=glm.vec3(130, 100, 100), material=MirrorMaterial())
        ]
            
        Scene.__init__(self, camera, shapes)
    
    def name(self):
        return "MirrorBalls"