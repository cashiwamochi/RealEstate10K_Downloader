import os
import sys

import cv2
import open3d as o3d
import numpy as np

def main(filepath):
    print("{} is loaded ... ".format(filepath))

    text_data = open(filepath, "r") 
    lines = text_data.readlines()

    scale = 0.01
    origin_coordinate = o3d.create_mesh_coordinate_frame(size = scale, origin = [0,0,0])
    coordinates_list = [origin_coordinate]
    for i, line in enumerate(lines):
        if i == 0:
            # 0th line is Youtube-URL
            continue

        values = [float(v) for j, v in enumerate(line.split(' ')) if j > 6]
        if False: # this is not correct transformation in RealEstate10K
            inv_transform_matrix = np.array([[values[0], values[1], values[2], values[3]],
                                             [values[4], values[5], values[6], values[7]],
                                             [values[8], values[9], values[10],values[11]],
                                             [0.0,       0.0,       0.0,       1.0]])
        else:
            R = np.array([[values[0], values[1], values[2]],
                          [values[4], values[5], values[6]],
                          [values[8], values[9], values[10]]])
            t = np.array([values[3],values[7],values[11]])
            R_inv = np.linalg.inv(R)
            T = -R_inv @ t
            inv_transform_matrix = np.array([[R_inv[0,0], R_inv[0,1], R_inv[0,2], T[0]],
                                             [R_inv[1,0], R_inv[1,1], R_inv[1,2], T[1]],
                                             [R_inv[2,0], R_inv[2,1], R_inv[2,2], T[2]],
                                             [0.0,       0.0,       0.0,       1.0]])

        current_coordinate = o3d.create_mesh_coordinate_frame(size = scale, origin = [0,0,0])
        current_coordinate.transform(inv_transform_matrix)
        coordinates_list.append(current_coordinate)


    o3d.draw_geometries(coordinates_list)

    return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 this.py [/path/to/data]")
        quit()

    main(sys.argv[1])
