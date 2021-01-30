Very basic naive pathtracer with minimal optimization written in a single Python file to use as a reference. Currently hardcodes a CornelBox scene along with a hardcoded camera based on the specs found here: https://www.graphics.cornell.edu/online/box/data.html. Only supports pure lambertian surfaces at the moment.

The resolution and number of samples per pixel can be specified as follows:

python path_tracer.py --x_res=512 --y_res=512 --samples=100
