from PIL import Image
from optparse import OptionParser
import numpy as np
from materials import *
from threading import Thread
from multiprocessing import JoinableQueue
import sys
import datetime
from scenes import *


def find_hit(ray, shapes):
    closest_hit = 10000000000
    final_hit = (-1, None, None)
    for shape in shapes:
        hit = shape.intersect(ray)
        if hit[0] > 0 and hit[0] < closest_hit:
            closest_hit = hit[0]
            final_hit = hit

    return final_hit

def trace_path(ray, shapes, depth, max_depth):
    if depth > max_depth:
        return glm.vec3(0)
    
    t, hit_normal, material = find_hit(ray, shapes)
    if t == -1.0:
        return glm.vec3(0)

    emittance = material.emissive_color
    hit_point = ray.origin + t*ray.direction

    # Pick a new ray direction which depends on the properties of the given material.
    newRay, pdf = material.sample_ray(ray, hit_normal, hit_point)

    # The percentage of light transmitted between the incoming and outgoing ray directions.
    # This changes depending on the type of material.
    brdf = material.brdf(-ray.direction, newRay.direction, hit_normal, hit_point)

    # Recurse with the new ray and continue accumulating radiance.
    incoming_light = trace_path(newRay, shapes, depth + 1, max_depth)

    # The integrand is emittance + BRDF * cosTheta * light.
    return emittance + brdf * glm.dot(newRay.direction, hit_normal) * incoming_light
    
# Creates an image from the pixel data.
def numpy2pil(np_array: np.ndarray) -> Image:
    """
    Convert an HxWx3 numpy array into an RGB Image
    """
    assert_msg = 'Input shall be a HxWx3 ndarray'
    assert isinstance(np_array, np.ndarray), assert_msg
    assert len(np_array.shape) == 3, assert_msg
    assert np_array.shape[2] == 3, assert_msg

    img = Image.fromarray(np.uint8(np.clip(np.power(np_array, 1.0/2.2), 0.0, 1.0)*255), 'RGB')
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


def main():
    # Grab the command line options.
    options, args = get_options()
    x_res = int(options.x_res)
    y_res = int(options.y_res)
    samples = int(options.samples)
    
    pixel_data = np.zeros((y_res, x_res, 3))

    scene = CornellBox()

    q = JoinableQueue()

    def worker():
        while True:
            pixel = q.get()
            if pixel is None:
                break

            x,y = pixel
            color = glm.vec3(0)
            for s in range(samples):
                ray = scene.camera.generate_ray(x, y, x_res, y_res)
                color += trace_path(ray, scene.shapes, 0, 7)
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

    image_name = "path_trace_" + str(x_res) + "x" + str(y_res) + "_" + str(samples) + ".png"
    image = numpy2pil(pixel_data)
    image.save(image_name, "PNG")

if __name__ == "__main__":
    main()