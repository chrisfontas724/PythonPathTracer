Very basic naive pathtracer with minimal optimization written in python and to be used as a reference for other PBR renderers that may use other techniques such as Photon Mapping or Metropolis Light Transport. Currently hardcodes a CornelBox scene along with a hardcoded camera based on the specs found here: https://www.graphics.cornell.edu/online/box/data.html. Other scenes can be created and played around with by simply adding your own scene subclass.

The resolution and number of samples per pixel can be specified as follows:

python path_tracer.py --x_res=512 --y_res=512 --samples=100
