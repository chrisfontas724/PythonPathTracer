from ray import *

class BoundingBox:
    def __init__(self, vertices):
        min_pos = glm.vec3(100000000)
        max_pos = glm.vec3(-100000000)
        for v in vertices:
            if v.x < min_pos.x: min_pos.x = v.x
            if v.y < min_pos.y: min_pos.y = v.y
            if v.z < min_pos.z: min_pos.z = v.z
            if v.x > max_pos.x: max_pos.x = v.x
            if v.y > max_pos.y: max_pos.y = v.y
            if v.z > max_pos.z: max_pos.z = v.z
        self.min = min_pos
        self.max = max_pos

    def intersect(self, ray):
        tmin = (self.min.x - ray.origin.x) / (ray.direction.x + 0.0001)
        tmax = (self.max.x - ray.origin.x) / (ray.direction.x + 0.0001)
 
        if tmin > tmax:  tmin, tmax = tmax, tmin
 
        tymin = (self.min.y - ray.origin.y) / (ray.direction.y + 0.0001)
        tymax = (self.max.y - ray.origin.y) / (ray.direction.y + 0.0001)
 
        if tymin > tymax: tymin, tymax = tymax, tymin 
 
        if (tmin > tymax) or (tymin > tmax):
            return False 
 
        if tymin > tmin:
            tmin = tymin 
 
        if tymax < tmax:
            tmax = tymax 
 
        tzmin = (self.min.z - ray.origin.z) / (ray.direction.z + 0.0001)
        tzmax = (self.max.z - ray.origin.z) / (ray.direction.z + 0.0001)
 
        if tzmin > tzmax: tzmin, tzmax = tzmax, tzmin
 
        if (tmin > tzmax) or (tzmin > tmax):
            return False
 
        if tzmin > tmin:
            tmin = tzmin
 
        if tzmax < tmax:
            tmax = tzmax 
 
        return True; 

class Shape:
    def __init__(self):
        return

    # Intersects a ray with a shape - subclasses implement their own
    # intersection routines.
    def intersect(self, ray):
        return -1.0

class Mesh(Shape):
    def __init__(self, vertices, indices, material):
        self.vertices = vertices
        self.indices = indices
        self.material = material
        self.bbox = BoundingBox(vertices)

    def intersect(self, ray):
        if not self.bbox.intersect(ray):
            return (-1, None, None)

        closest_hit = 1000000000.0
        final_v0 = 0 
        final_v1 = 0 
        final_v2 = 0
        for i in range(0, len(self.indices), 3):
            v0 = self.vertices[self.indices[i]]
            v1 = self.vertices[self.indices[i+1]]
            v2 = self.vertices[self.indices[i+2]]
            curr_hit = Mesh.triangle_intersect(ray, v0, v1, v2)
            if curr_hit > 0.0 and curr_hit < closest_hit:
                closest_hit = curr_hit
                final_v0 = v0 
                final_v1 = v1 
                final_v2 = v2
            
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
    def normal(self, point):
        return glm.normalize(point - self.center)

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
            t = b - det 
        elif b + det > eps:
            t = b + det
        else:
            t = -1.0

        return (t, self.normal(ray.origin + t*ray.direction), self.material) if t != -1.0 else (-1, None, None)
