from PIL import Image
from optparse import OptionParser
import numpy as np
import math
import glm
import random
from copy import deepcopy
from threading import Thread
from multiprocessing import JoinableQueue
import sys
import datetime

class Camera:
    def __init__(self):
        self.position = glm.vec3(278, 273, -800)
        self.direction = glm.vec3(0,0,1)
        self.up = glm.vec3(0,1,0)
        self.focal_length = 0.035
        self.width = 0.025
        self.height = 0.025

class Ray:
    def __init__(self, origin=glm.vec3(0), direction=glm.vec3(0,0,1)):
        self.origin = origin
        self.direction = direction

class Material:
    def __init__(self, diffuse=glm.vec3(1), specular=glm.vec3(0), emission = glm.vec3(0), percent=1):
        self.diffuse_color = diffuse
        self.specular_color = specular
        self.emissive_color = emission
        self.diffuse_percent = percent

class Shape:
    def __init__(self):
        return

    def intersect(self, ray):
        return -1.0

class Mesh(Shape):
    def __init__(self, vertices, indices, material):
        self.vertices = vertices
        self.indices = indices
        self.material = material

    def intersect(self, ray):
        closest_hit = 1000000000.0
        final_v0 = 0 
        final_v1 = 0 
        final_v2 = 0
        for i in range(0, len(self.indices), 3):
            v0 = self.vertices[self.indices[i]]
            v1 = self.vertices[self.indices[i+1]]
            v2 = self.vertices[self.indices[i+2]]
            #print("INDICES: " + str(self.indices[i]) + " " + str(self.indices[i+1]) + " " + str(self.indices[i+2]))
            curr_hit = Mesh.triangle_intersect(ray, v0, v1, v2)
            #print("CURR HIT: " + str(curr_hit))
            if curr_hit > 0.0 and curr_hit < closest_hit:
                closest_hit = curr_hit
                final_v0 = v0 
                final_v1 = v1 
                final_v2 = v2
            
       # print("NOW!")
        if closest_hit != 1000000000.0:
            return (closest_hit, Mesh.triangle_normal(final_v0, final_v1, final_v2), self.material)
        else:
            return (-1, None, None)
        

    def triangle_normal(v0, v1, v2):
        return glm.normalize(glm.cross(v0-v1, v0-v2))

    def triangle_intersect(r, v0, v1, v2):
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        pvec = glm.cross(r.direction, v0v2)

        det = glm.dot(v0v1, pvec)

        if det < 0.000001:
            return -1.0

        invDet = 1.0 / det
        tvec = r.origin - v0
        u = glm.dot(tvec, pvec) * invDet

        if u < 0 or u > 1:
            return float(-1.0)

        qvec = glm.cross(tvec, v0v1)
        v = glm.dot(r.direction, qvec) * invDet

        if v < 0 or u + v > 1:
            return -1.0
        return glm.dot(v0v2,qvec) * invDet

class Rectangle(Mesh):
    def __init__(self, v0, v1, v2, v3, material):
        Mesh.__init__(self, [v0, v1, v2, v3], [0, 1, 2, 0, 2, 3], material)

class Sphere(Shape):
    def __init__(self, radius=1.0, center=glm.vec3(0), diffuse=glm.vec3(1), specular=glm.vec3(0), percent=1.0):
        self.radius = radius
        self.center = center
        self.material = Material(diffuse, specular, percent)

    # Returns the normal vector at a particular point.
    def normal(point):
        return glm.normalize(point - self.center)

    # Intersects a ray with the sphere - returns -1 if there
    # is no intersection.
    def intersect(self, ray):
        op = self.center-ray.origin 
        eps = 1e-4
        b = glm.dot(op, ray.direction)
        det = b*b - glm.dot(op, op) + self.radius*self.radius
        if det < 0:
            return -1.0
        else:
            det = math.sqrt(det)
        t = b - det

        if b - det > eps:
            return b - det 
        elif b+det > eps:
            return b + det
        else:
            return -1.0

def find_hit(ray, shapes):
    closest_hit = 10000000000
    final_hit = (-1, None, None)
    for shape in shapes:
        hit = shape.intersect(ray)
        if hit[0] > 0 and hit[0] < closest_hit:
            closest_hit = hit[0]
            final_hit = hit

    return final_hit
    

# Returns a vector in the hemisphere around N with a cosine weighted
# distribution to avoid clumping.
def cosWeightedHemisphereDirection(N):
    xi1 = random.uniform(0, 1)
    xi2 = random.uniform(0, 1)
    
    theta = math.acos(math.sqrt(float(1.)-xi1))
    phi = 2.0*math.pi*xi2
    
    xs = math.sin(theta) * math.cos(phi)
    ys = math.cos(theta)
    zs = math.sin(theta) * math.sin(phi)
    
    y = deepcopy(N)
    h = deepcopy(y)
    if math.fabs(h.x) <= math.fabs(h.y) and math.fabs(h.x) <= math.fabs(h.z):
        h.x = 1.0
    elif math.fabs(h.y) <= math.fabs(h.x) and math.fabs(h.y) <= math.fabs(h.z):
        h.y= 1.0
    else:
        h.z = 1.0

    x = glm.normalize(glm.cross(h,y))
    z = glm.normalize(glm.cross(x,y))
    
    return glm.normalize(xs*x + ys*y + zs*z)

def trace_path(ray, shapes, depth, max_depth):
    if depth > max_depth:
        return glm.vec3(0)
    
    t, hit_normal, material = find_hit(ray, shapes)
    #print(str(t) + " " + str(normal))
    if t == -1.0:
        return glm.vec3(0)

    emittance = material.emissive_color
    hit_point = ray.origin + t*ray.direction

    # Pick a random direction
    newRay = Ray()
    newRay.direction = cosWeightedHemisphereDirection(hit_normal)
    assert glm.dot(newRay.direction, hit_normal) > 0.0, "Dir: " + str(newRay.direction)
    newRay.origin = hit_point + 0.001*newRay.direction

    # Probability of a new ray
    # cos_theta = glm.dot(newRay.direction, hit_normal)
    # p = cos_theta / math.pi
    # assert  p > 0.0, "P is " + str(p)

    # Compute the BRDF for the ray
    BRDF = material.diffuse_color # / math.pi 
    incoming_light = trace_path(newRay, shapes, depth + 1, max_depth)

    return emittance + BRDF * incoming_light  #* cos_theta)  #/ p
    

# Creates an image from the pixel data.
def numpy2pil(np_array: np.ndarray) -> Image:
    """
    Convert an HxWx3 numpy array into an RGB Image
    """
    assert_msg = 'Input shall be a HxWx3 ndarray'
    assert isinstance(np_array, np.ndarray), assert_msg
    assert len(np_array.shape) == 3, assert_msg
    assert np_array.shape[2] == 3, assert_msg

    img = Image.fromarray(np.uint8(np_array*255), 'RGB')
    return img

def get_options():
    parser = OptionParser(version="%prog 1.0")

    parser.add_option("-x", "--x_res",
                      action="store", # image width
                      dest="x_res",
                      default=512,
                      help="Pick the width of the output image in pixelspace")

    parser.add_option("-y", "--y_res",
                      action="store", # image height
                      dest="y_res",
                      default=512,
                      help="Pick the width of the output image in pixelspace")


    parser.add_option("-s", "--samples",
                      action="store", # The number of samples per pixel
                      dest="samples",
                      default=1,
                      help="The number of samples (rays) per pixel.")


    parser.add_option("-l", "--direct_lighting",
                      action="store", # Whether we use direct lighting or not
                      dest="use_direct_ligthing",
                      default=False,
                      help="Determines if we directly sample the light source or not")
    return parser.parse_args()


def generate_ray(pixel_x, pixel_y, image_width, image_height, camera):
    image_aspect_ratio = float(image_width) / float(image_height)

    alpha = 2.0 * math.atan(1.0 / (2.0 * camera.focal_length)) 

    s_1 = random.uniform(0,1)
    s_2 = random.uniform(0,1)

    pixel_ndc_x = (pixel_x + s_1) / image_width
    pixel_ndc_y = (pixel_y + s_2) / image_height 

    pixel_screen_x = 2.0 * pixel_ndc_x - 1.0
    pixel_screen_y = 2.0 * pixel_ndc_y - 1.0

    pixel_camera_x = pixel_screen_x * camera.width * image_aspect_ratio * math.tan(alpha/2)
    pixel_camera_y = pixel_screen_y * camera.height * math.tan(alpha/2)

    camera_point = glm.vec3(pixel_camera_x, pixel_camera_y, -1.0)
    return Ray(camera.position, glm.normalize(-camera_point))

def main():
    # Grab the command line options.
    options, args = get_options()
    x_res = int(options.x_res)
    y_res = int(options.y_res)
    samples = int(options.samples)
    
    pixel_data = np.zeros((y_res, x_res, 3))

    camera = Camera()

    shapes = [
        # Floor
        Rectangle(glm.vec3(552.8, 0.0, 0.0),
                  glm.vec3(0),
                  glm.vec3(0,0, 559.2),
                  glm.vec3(549.6, 0.0, 559.2),
                  Material()),

        # Left wall - Red
        Rectangle(glm.vec3(552.8,   0.0,   0.0),
                  glm.vec3(549.6,   0.0, 559.2),
                  glm.vec3(556.0, 548.8, 559.2),
                  glm.vec3(556.0, 548.8,   0.0),
                  Material(diffuse = glm.vec3(1,0,0))),

        # Right wall - Green
        Rectangle(glm.vec3(0.0,  0.0, 559.2),
                  glm.vec3(0.0,   0.0,   0.0),
                  glm.vec3(0.0, 548.8,   0.0),
                  glm.vec3(0.0, 548.8, 559.2),
                  Material(diffuse = glm.vec3(0,1,0))),

        # Back wall - White
        Rectangle(glm.vec3(549.6, 0.0, 559.2),
                  glm.vec3(0.0,  0.0, 559.2),
                  glm.vec3(0.0, 548.8, 559.2),
                  glm.vec3(556.0, 548.8, 559.2),
                  Material(diffuse = glm.vec3(1,1,1))),

        # Ceiling - White
        Rectangle(glm.vec3(556.0, 548.8, 0.0),
                  glm.vec3(556.0, 548.8, 559.2),
                  glm.vec3(0.0, 548.8, 559.2),
                  glm.vec3(0.0, 548.8, 0.0),
                  Material(diffuse = glm.vec3(1,1,1))),

        # Light
        Rectangle(glm.vec3(343.0, 548.75, 227.0),
                  glm.vec3(343.0, 548.75, 332.0),
                  glm.vec3(213.0, 548.75, 332.0),
                  glm.vec3(213.0, 548.75, 227.0),
                  Material(diffuse = glm.vec3(0), emission = glm.vec3(20000, 20000, 20000)))
    ]

    q = JoinableQueue()

    def worker():
        while True:
            pixel = q.get()
            if pixel is None:
                break

            x,y = pixel
            color = glm.vec3(0)
            for s in range(samples):
                ray = generate_ray(x, y, x_res, y_res, camera)
                color += trace_path(ray, shapes, 0, 7)
            color /= samples
            pixel_data[y, x, 0] = color.x
            pixel_data[y, x, 1] = color.y
            pixel_data[y, x, 2] = color.z
            q.task_done()

    threads = []
    num_worker_threads = 10
    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.start()
        threads.append(t)

    a = datetime.datetime.now()
    for y in range(y_res):
        for x in range(x_res):
            q.put((x,y))

    q.join()

    # stop workers
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()
    
    b = datetime.datetime.now()
    print("Time Elapsed: " + str(b-a))

    image = numpy2pil(pixel_data)
    image.save("path_tracing_multithread_final.png", "PNG")

if __name__ == "__main__":
    main()