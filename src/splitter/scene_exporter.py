import struct
import os


class SceneExporter:
    def __init__(self, scene, output_dir: str):
        """
        Initializes the SceneExporter class with the scene and output path.

        :param scene: dict
            A dictionary containing scene data including cameras and points.
        :param output_dir: str
            A string containing the directory to save the exported binary files.
        """
        self.scene = scene
        self.output_dir = output_dir

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def pack_cameras(self):
        """
        Packs and writes the camera data into a COLMAP-compatible 'images.bin' file.
        """
        # Open the output file in binary write mode
        with open(os.path.join(self.output_dir, 'images.bin'), 'wb') as f:
            cameras = self.scene['cameras']

            # Write the number of cameras (images)
            f.write(struct.pack('<Q', len(cameras)))

            for image_id, camera in cameras.items():
                # Write image_id (4 bytes)
                f.write(struct.pack('<I', image_id))

                # Write quaternion (qvec) (4 * 8 bytes)
                f.write(struct.pack('<dddd', *camera['qvec']))

                # Write translation vector (tvec) (3 * 8 bytes)
                f.write(struct.pack('<ddd', *camera['tvec']))

                # Write camera_id (4 bytes)
                f.write(struct.pack('<I', camera['camera_id']))

                # Write image name (null-terminated string)
                f.write(camera['name'].encode('utf-8') + b'\x00')

                # Write the number of 2D points (8 bytes)
                num_points2d = len(camera['xys'])
                f.write(struct.pack('<Q', num_points2d))

                # Write 2D points (x, y) coordinates (2 * 8 bytes each)
                for xy in camera['xys']:
                    f.write(struct.pack('<dd', *xy))

                # Write 3D point ids associated with each 2D point (8 bytes each)
                for point3d_id in camera['point3d_ids']:
                    f.write(struct.pack('<q', point3d_id))

    def pack_points(self):
        """
        Packs and writes the 3D point data into a COLMAP-compatible 'points3D.bin' file.
        """
        # Open the output file in binary write mode
        with open(os.path.join(self.output_dir, 'points3D.bin'), 'wb') as f:
            points = self.scene['points']

            # Write the number of 3D points
            f.write(struct.pack('<Q', len(points)))

            for point3d_id, point in points.items():
                # Write point3d_id (8 bytes)
                f.write(struct.pack('<Q', point3d_id))

                # Write the 3D coordinates (x, y, z) (3 * 8 bytes)
                f.write(struct.pack('<ddd', *point['xyz']))

                # Write the RGB color values (3 bytes)
                f.write(struct.pack('<BBB', *point['rgb']))

                # Write the reprojection error (8 bytes)
                f.write(struct.pack('<d', point['error']))

                # Write the number of observations (track length) (8 bytes)
                track_length = len(point['track'])
                f.write(struct.pack('<Q', track_length))

                # Write the track elements (image_id and point2d_idx for each observation)
                for image_id, point2d_idx in point['track']:
                    f.write(struct.pack('<I', image_id))       # image_id (4 bytes)
                    f.write(struct.pack('<I', point2d_idx))   # point2d_idx (4 bytes)

    def export_scene(self):
        """
        Exports the entire scene into binary files ('images.bin' and 'points3D.bin').
        """
        # Pack and export points3D.bin
        self.pack_points()

        # Pack and export images.bin
        self.pack_cameras()

        print(f"Scene successfully exported to {self.output_dir}")
