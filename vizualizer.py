import os
import sys

import open3d as o3d
import numpy as np

def main(filepath):
    print("{} is loaded ... ".format(filepath))

    text_data = open(filepath, "r") 
    lines = text_data.readlines()

    scale = 0.1
    origin_coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 0.15, origin = [0,0,0])
    coordinates_list = [origin_coordinate]
    for i, line in enumerate(lines):
        if i == 0:
            # 0th line is Youtube-URL
            continue

        values = [float(v) for j, v in enumerate(line.split(' ')) if j > 6]

        R = np.array([[values[0], values[1], values[2]],
                      [values[4], values[5], values[6]],
                      [values[8], values[9], values[10]]])
        t = np.array([values[3],values[7],values[11]])
        R_inv = np.linalg.inv(R)
        T = -R_inv @ t
        if i == 1:
            transform_matrix0 = np.array([[R[0,0], R[0,1], R[0,2], t[0]],
                                         [R[1,0], R[1,1], R[1,2], t[1]],
                                         [R[2,0], R[2,1], R[2,2], t[2]],
                                         [0.0,    0.0,    0.0,    1.0]])
        inv_transform_matrix = np.array([[R_inv[0,0], R_inv[0,1], R_inv[0,2], T[0]],
                                         [R_inv[1,0], R_inv[1,1], R_inv[1,2], T[1]],
                                         [R_inv[2,0], R_inv[2,1], R_inv[2,2], T[2]],
                                         [0.0,       0.0,       0.0,       1.0]])

        inv_transform_matrix = transform_matrix0 @ inv_transform_matrix


        current_coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size = scale, origin = [0,0,0])
        current_coordinate.transform(inv_transform_matrix)
        coordinates_list.append(current_coordinate)


    o3d.visualization.draw_geometries(coordinates_list)

    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 this.py [/path/to/data]")
        quit()

    main(sys.argv[1])
