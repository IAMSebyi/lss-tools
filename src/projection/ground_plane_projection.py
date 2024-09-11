import numpy as np


class GroundPlaneProjector:
    def __init__(self, scene):
        """
        Initializes the Ground Plane Projector with the loaded COLMAP scene

        :param scene: dict
            A dictionary containing:
            - "points": A dictionary of 3D points where each key is a point ID and value is a dictionary with point attributes
             (e.g., "xyz" for coordinates).
            - "cameras": A dictionary of camera and image information where each key is an image ID and value is a dictionary with camera parameters
             (e.g., "tvec" for translation vectors).
        """
        self.scene = scene

    def project_to_2d(self):
        """
        Projects the COLMAP scene from 3D to 2D using a ground plane projection for visualization purposes.

        This method assumes that the z-coordinate is used as depth and ignores it in the 2D projection. The resulting projection
        maps the x and y coordinates of points and camera positions onto a 2D plane.

        :return: dict
            A dictionary containing:
            - "points": A numpy array of projected 3D points on the ground plane (x and z coordinates).
            - "cameras": A numpy array of projected camera positions on the ground plane (x and z coordinates).
        """
        # Extract points and cameras from the scene dictionary
        points = self.scene['points']
        cameras = self.scene['cameras']

        # Convert points and cameras to numpy arrays if they are not already
        points_xyz = np.array([point['xyz'] for point in points.values()])
        cameras_tvec = np.array([camera['tvec'] for camera in cameras.values()])

        # Project 3D points to 2D (ignoring the y-coordinate)
        projected_points = points_xyz[:, [0, 2]]

        # Project camera positions to 2D (ignoring the y-coordinate)
        projected_cameras = cameras_tvec[:, [0, 2]]

        # Organize the projected data into a dictionary
        projected_scene = {
            "points": projected_points,
            "cameras": projected_cameras
        }

        return projected_scene
