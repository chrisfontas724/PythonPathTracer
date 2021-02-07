from ray import *
import random
import math

class Material:
    # The bidirectional reflectance distribution function which returns
    # the percentage of light reflected in direction w_o from direction w_i
    # at location p with normal N.
    def brdf(self, w_i, w_o, n, p):
        return glm.vec3(0)

    # Material subclasses implement their own sample functions which
    # return a new ray along with the pdf of that ray.
    def sample_ray(self, ray, N, P):
        return (None, 0)

    def emission(self):
        return glm.vec3(0)

class DiffuseMaterial(Material):
    def __init__(self, diffuse=glm.vec3(1), emission = glm.vec3(0)):
        self.diffuse_color = diffuse
        self.emissive_color = emission

    # The diffuse BRDF is equal in all directions with a cosine falloff.
    def brdf(self, w_i, w_o, n, p):
        return self.diffuse_color / math.pi

    def emission(self):
        return self.emissive_color

    # Returns a vector in the hemisphere around N with a cosine weighted
    # distribution to avoid clumping along with the pdf of cos(theta) / Pi.
    def sample_ray(self, ray, N, P):
        xi1 = random.uniform(0, 1)
        xi2 = random.uniform(0, 1)
    
        theta = math.acos(math.sqrt(float(1.)-xi1))
        phi = 2.0*math.pi*xi2
    
        xs = math.sin(theta) * math.cos(phi)
        ys = math.cos(theta)
        zs = math.sin(theta) * math.sin(phi)
    
        y = glm.vec3(N)
        h = glm.vec3(y)
        if math.fabs(h.x) <= math.fabs(h.y) and math.fabs(h.x) <= math.fabs(h.z):
            h.x = 1.0
        elif math.fabs(h.y) <= math.fabs(h.x) and math.fabs(h.y) <= math.fabs(h.z):
            h.y= 1.0
        else:
            h.z = 1.0

        x = glm.normalize(glm.cross(h,y))
        z = glm.normalize(glm.cross(x,y))

        new_dir = glm.normalize(xs*x + ys*y + zs*z)
        assert glm.dot(new_dir, N)

        new_ray = Ray()
        new_ray.direction = new_dir

        # Add a small epsilon to the new ray starting point to prevent self-intersection
        # with the object its already on.
        new_ray.origin = P + 0.001 * new_dir
        return (new_ray, glm.dot(new_dir, N) / math.pi)


class MirrorMaterial(Material):
    def __init__(self, color=glm.vec3(1)):
        self.color = color

    def emission(self):
        return glm.vec3(0)

    # The brdf is only valid if w_o is the perfect reflected vector to w_i.
    def brdf(self, w_i, w_o, n, p):
        test_ray = Ray()
        test_ray.origin = p
        test_ray.direction = -w_i
        ray, _ = self.sample_ray(test_ray, n, p)
        return self.color if glm.dot(ray.direction, w_o) >= 0.99 else glm.vec3(0)

    # Simply return the mirrored ray across the normal with a pdf of 1.
    def sample_ray(self, ray, N, P):
        d = glm.vec3(ray.direction)
        new_dir = glm.normalize(d - 2.0 * glm.dot(d, N) * N)
        new_ray = Ray() 
        new_ray.direction = new_dir
        new_ray.origin = P + 0.001 * new_dir
        return (new_ray, 1.0)
