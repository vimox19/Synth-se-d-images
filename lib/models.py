import numpy as np

def read_obj(path_to_file):
    vertices = []
    faces = []
    texture_coords = []
    normals = []

    with open(path_to_file, 'r') as f:
        lines = f.readlines()


    for line in lines:
        line = line.strip()
        if line.startswith('v '):
            vertex = list(map(float, line.split()[1:]))
            vertices.append(vertex)
        elif line.startswith('vt '):
            texture_coord = list(map(float, line.split()[1:]))
            texture_coords.append(texture_coord)
        elif line.startswith('vn '):
            normal = list(map(float, line.split()[1:]))
            normals.append(normal)
        elif line.startswith('f '):
            face_indices = line.split()[1:]
            face = []
            for index in face_indices:
                vertex_index, texcoord_index, normal_index = map(int, index.split('/'))
                face.append((vertex_index, texcoord_index, normal_index))
            faces.append(face)

    vertex_data = np.array(vertices)
    index_data = np.array(faces, dtype=np.uint32)
    texture_data = np.array(texture_coords)
    normals_data = np.array(normals)

    return vertex_data

def calc_features(vertex_data):

    center_of_mass = np.mean(vertex_data, axis=0)

    Ix = 0
    Iy = 0
    Iz = 0
    average_distance_x = 0
    average_distance_y = 0
    average_distance_z = 0
    variance_x = 0
    variance_y = 0
    variance_z = 0

    #mass = len(vertex_data)

    for vertex in vertex_data:
        x = vertex[0] - center_of_mass[0]
        y = vertex[1] - center_of_mass[1]
        z = vertex[2] - center_of_mass[2]

    Ix += (y*y + z*z)
    Iy += (x*x + z*z)
    Iz += (x*x + y*y)

    average_distance_x += abs(x)
    average_distance_y += abs(y)
    average_distance_z += abs(z)

    variance_x += x * x
    variance_y += y * y
    variance_z += z * z

    average_distance_x /= len(vertex_data)
    average_distance_y /= len(vertex_data)
    average_distance_z /= len(vertex_data)

    variance_x /= len(vertex_data)
    variance_y /= len(vertex_data)
    variance_z /= len(vertex_data)

    shape_vec = np.array([[Ix,average_distance_x,variance_x],[Iy,average_distance_y,variance_y],[Iz,average_distance_z,variance_z]])

    return shape_vec

#vertex_data, index_data, texture_data, normals_data = read_obj("F:\Lessons and projects\Traitement d'image aitlkbir lsi\OpenGl aitkbir lsi\OpenGL\Mini project\Models\Alabastron1.obj")

