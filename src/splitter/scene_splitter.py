import numpy as np
from collections import defaultdict


class SceneSplitter:
    def __init__(self, scene, rows: int, cols: int, num_of_points: int):
        """
        Initializes the SceneSplitter with the scene data and grid dimensions.

        :param scene: dict
            A dictionary containing scene data including cameras and points.
        :param rows: int
            Number of rows to divide the scene into.
        :param cols: int
            Number of columns to divide the scene into.
        :param num_of_points: int
            Number of points in the scene
        """
        self.scene = scene
        self.rows = rows
        self.cols = cols
        self.num_of_points = num_of_points
        self.cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def create_cells(self):
        """
        Creates a grid of cells based on the bounding box of 3D point positions.
        """

        # Extract points from the scene
        points = self.scene['points']

        # Convert point positions to numpy array if it is not already
        xyz = np.array([point['xyz'] for point in points.values()])

        # Get the minimum X and Z
        min_x = np.min(xyz[:, 0])  # Minimum value of the first column (X)
        min_z = np.min(xyz[:, 2])  # Minimum value of the third column (Z)

        # Get the maximum X and Z
        max_x = np.max(xyz[:, 0])  # Maximum value of the first column (X)
        max_z = np.max(xyz[:, 2])  # Maximum value of the third column (Z)

        # Define the bounding box
        bounding_box = {
            "min": [min_x, min_z],  # Minimum X and Z values
            "max": [max_x, max_z]  # Maximum X and Z values
        }

        # Compute size of each cell
        col_size = (bounding_box['max'][0] - bounding_box['min'][0]) / self.cols
        row_size = (bounding_box['max'][1] - bounding_box['min'][1]) / self.rows

        # Divide bounding box into rows * cols cells
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col] = {
                    "min": [bounding_box['min'][0] + col_size * col, bounding_box['max'][1] - row_size * (row + 1)],
                    "max": [bounding_box['min'][0] + col_size * (col + 1), bounding_box['max'][1] - row_size * row]
                }

    def split_scene(self):
        """
        Splits the scene into grid cells and classifies points into these cells,
        also aggregates cameras that sees the points within each cell.
        """
        # Generate cells
        self.create_cells()

        # Extract points and cameras from the scene
        points = self.scene['points']
        cameras = self.scene['cameras']

        # Define cell points and cameras matrices
        cell_points = {(r, c): {} for r in range(self.rows) for c in range(self.cols)}
        cell_cameras = {(r, c): {} for r in range(self.rows) for c in range(self.cols)}

        cell_camera_freq = {(r, c): defaultdict(int) for r in range(self.rows) for c in range(self.cols)}

        id_error_count = 0  # ID correlation error count

        step = 0
        for point_id, point in points.items():
            # Log steps
            step = step + 1
            print(f"Splitting scene: {round(float(step / self.num_of_points) * 100.0, 2)}%")

            # Extract ground plane (XZ axis) 2D coordinates
            x, z = point['xyz'][0], point['xyz'][2]

            # Find the cell the point belongs to
            for row in range(self.rows):
                found_cell = False
                for col in range(self.cols):
                    cell = self.cells[row][col]
                    if cell['min'][0] <= x < cell['max'][0] and cell['min'][1] <= z < cell['max'][1]:
                        # Append point to the appropiate cell (use point_id as key)
                        cell_points[(row, col)][point_id] = point

                        # Append cameras in which the point is seen
                        for pt_image_id, _ in point['track']:
                            if pt_image_id in cameras.keys():
                                cell_cameras[(row, col)][pt_image_id] = cameras[pt_image_id]
                                # Initialize or increment frequency
                                if pt_image_id in cell_camera_freq[(row, col)]:
                                    cell_camera_freq[(row, col)][pt_image_id] += 1
                                else:
                                    cell_camera_freq[(row, col)][pt_image_id] = 1
                            else:
                                id_error_count = id_error_count + 1

                        # Found the cell, no need to check other cells
                        found_cell = True
                        break

                if found_cell:
                    break

        # Convert cell data to the same format as the scene
        split_scenes = []
        for row in range(self.rows):
            for col in range(self.cols):
                cell_num_cameras = len(cell_cameras[(row, col)])
                cell_num_points = len(cell_points[(row, col)])

                # Prune insignificant cameras
                cameras_to_remove = [image_id for image_id, freq in cell_camera_freq[(row, col)].items()
                                     if freq / cell_num_points < 0.003]
                for image_id in cameras_to_remove:
                    del cell_cameras[(row, col)][image_id]

                # Check if cell is empty or irrelevant
                if not cell_cameras[(row, col)]:
                    print(f"WARNING: Cell scene at the ({row}, {col}) position is empty!")
                    continue
                elif cell_num_cameras / cell_num_points > 0.5 or cell_num_points < 10:
                    print(f"WARNING: Cell scene at the ({row}, {col}) position is irrelevant!")
                    continue

                cell_scene = {
                    'points': cell_points[(row, col)],
                    'cameras': cell_cameras[(row, col)]
                }

                split_scenes.append(((row, col), cell_scene))

        # Log the ID correlation error count
        if id_error_count > 0:
            print(f"WARNING: {id_error_count} image IDs extracted from points do not match cameras' image IDs!")

        return self.cells, split_scenes
