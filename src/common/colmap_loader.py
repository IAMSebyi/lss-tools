import struct
import sys

import numpy as np


class COLMAPLoader:
    def __init__(self, path_to_scene: str):
        """
        Initializes the COLMAPLoader with the path to the scene directory.

        :param path_to_scene: Path to the directory containing COLMAP binary files.
        """
        self.path_to_scene = path_to_scene

    def load_points3D(self):
        """
        Loads the 3D points from the COLMAP binary file 'points3D.bin'.

        :return: A dictionary where keys are point3D_ids and values are dictionaries containing
                 point coordinates (xyz), RGB color values, reprojection error, and track information.
        """
        points3D = {}
        # Open the binary file for reading
        with open(self.path_to_scene + '/points3D.bin', "rb") as f:
            # Read the number of 3D points
            num_points3D = struct.unpack('<Q', f.read(8))[0]

            # Iterate over each 3D point
            for i in range(num_points3D):
                print(f"Loading #{i} point...")

                # Read point3d_id
                point3d_id = struct.unpack('<Q', f.read(8))[0]

                # Read the coordinates of the point (x, y, z)
                xyz = struct.unpack('<ddd', f.read(8 * 3))

                # Read the RGB color values of the point
                rgb = struct.unpack('<BBB', f.read(3))

                # Read the reprojection error of the point
                error = struct.unpack('<d', f.read(8))[0]

                # Read the length of the track (number of observations)
                track_length = struct.unpack('<Q', f.read(8))[0]

                # Read the track elements (image_id and point2d_idx for each observation)
                track_elements = []
                for _ in range(track_length):
                    image_id = struct.unpack('<I', f.read(4))[0]
                    point2d_idx = struct.unpack('<I', f.read(4))[0]
                    track_elements.append((image_id, point2d_idx))

                # Store the information in the dictionary
                points3D[point3d_id] = {
                    "xyz": np.array(xyz),
                    "rgb": np.array(rgb),
                    "error": error,
                    "track": track_elements
                }

        return points3D

    def load_images(self):
        """
        Loads the images from the COLMAP binary file 'images.bin'.

        :return: A dictionary where keys are image_ids and values are dictionaries containing
                 quaternion (qvec), translation vector (tvec), camera_id, image name, 2D points coordinates (xys),
                 and associated 3D point ids (point3d_ids).
        """
        images = {}
        # Open the binary file for reading
        with open(self.path_to_scene + '/images.bin', "rb") as f:
            # Read the number of images
            num_images = struct.unpack('<Q', f.read(8))[0]

            # Iterate over each image
            for i in range(num_images):
                print(f"Loading #{i} image...")

                # Read image_id
                image_id = struct.unpack('<I', f.read(4))[0]

                # Read the quaternion (qvec) representing the camera orientation
                qvec = struct.unpack('<dddd', f.read(8 * 4))

                # Read the translation vector (tvec) representing the camera position
                tvec = struct.unpack('<ddd', f.read(8 * 3))

                # Read the camera_id used for this image
                camera_id = struct.unpack('<I', f.read(4))[0]

                # Read the image name, which is terminated by a null byte
                name = ""
                while True:
                    char = f.read(1).decode('utf-8')
                    if char == '\x00':
                        break
                    name += char

                # Read the number of 2D points in this image
                num_points2d = struct.unpack('<Q', f.read(8))[0]

                # Read the coordinates of the 2D points (x, y)
                xys = struct.unpack('<' + 'dd' * num_points2d, f.read(8 * 2 * num_points2d))

                # Read the 3D point ids associated with each 2D point
                point3d_ids = struct.unpack('<' + 'q' * num_points2d, f.read(8 * num_points2d))

                # Store the information in the dictionary
                images[image_id] = {
                    "qvec": np.array(qvec),
                    "tvec": np.array(tvec),
                    "camera_id": camera_id,
                    "name": name,
                    "xys": np.array(xys).reshape(-1, 2),
                    "point3d_ids": np.array(point3d_ids)
                }

        return images

    def load_scene(self):
        """
        Loads the complete COLMAP scene data, including 3D points and camera information.

        This method aggregates and loads all necessary components of a COLMAP scene:
        - 3D points from the 'points3D.bin' file
        - Camera and image data from the 'images.bin' file

        The loaded data is stored in a dictionary with two keys:
        - "points": A dictionary where keys are point IDs and values are dictionaries containing point information
        (e.g., coordinates, color, and track information).
        - "cameras": A dictionary where keys are image IDs and values are dictionaries containing camera parameters
        (e.g., rotation vectors, translation vectors, camera IDs, and image names).

        :return: dict
            A dictionary containing:
            - "points": A dictionary of 3D points
            - "cameras": A dictionary of camera and image information
        """
        # Load points
        points3D = self.load_points3D()

        # Load cameras
        images = self.load_images()

        # Store scene information in the dictionary
        scene = {
            "points": points3D,
            "cameras": images
        }

        return scene
