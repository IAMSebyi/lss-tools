import numpy as np


class SceneSplitter:
    def __init__(self, scene, rows: int, cols: int):
        """
        Initializes the SceneSplitter with the scene data and grid dimensions.

        :param scene: dict
            A dictionary containing scene data including cameras and points.
        :param rows: int
            Number of rows to divide the scene into.
        :param cols: int
            Number of columns to divide the scene into.
        """
        self.scene = scene
        self.rows = rows
        self.cols = cols
        self.cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def create_cells(self):
        """
        Creates a grid of cells based on the bounding box of camera positions.
        """
        # Extract cameras from the scene
        cameras = self.scene['cameras']

        # Convert camera positions (tvecs) to numpy array if it is not already
        tvecs = np.array([camera['tvec'] for camera in cameras.values()])

        # Get the minimum X and Z
        min_x = np.min(tvecs[:, 0])  # Minimum value of the first column (X)
        min_z = np.min(tvecs[:, 2])  # Minimum value of the third column (Z)

        # Get the maximum X and Z
        max_x = np.max(tvecs[:, 0])  # Maximum value of the first column (X)
        max_z = np.max(tvecs[:, 2])  # Maximum value of the third column (Z)

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
        Splits the scene into grid cells and classifies cameras into these cells,
        also aggregates points seen by cameras within each cell.
        """
        # Generate cells
        self.create_cells()

        # Find cameras and points that belong to each cell
        cameras = self.scene['cameras']
        points = self.scene['points']

        cell_cameras = {(r, c): {} for r in range(self.rows) for c in range(self.cols)}
        cell_points = {(r, c): {} for r in range(self.rows) for c in range(self.cols)}

        step = 0
        for image_id, camera in cameras.items():
            # Log steps
            step = step + 1
            print(f"Current splitting step: {step}")

            x, z = camera['tvec'][0], camera['tvec'][2]
            for row in range(self.rows):
                found_cell = False
                for col in range(self.cols):
                    cell = self.cells[row][col]
                    if cell['min'][0] <= x < cell['max'][0] and cell['min'][1] <= z < cell['max'][1]:
                        # Append the camera to the appropriate cell (use image_id as key)
                        cell_cameras[(row, col)][image_id] = camera

                        # Find points that are seen by the camera using image_id
                        for point_id, point in points.items():
                            if any(pt_image_id == image_id for pt_image_id, _ in point['track']):
                                cell_points[(row, col)][point_id] = point

                        # Found the cell, no need to check other cells
                        found_cell = True
                        break

                if found_cell:
                    break

        # Convert the cell data to the same format as the scene
        split_scenes = []
        for row in range(self.rows):
            for col in range(self.cols):
                cell_scene = {
                    'points': cell_points[(row, col)],
                    'cameras': cell_cameras[(row, col)]
                }
                split_scenes.append(((row, col), cell_scene))

        return split_scenes
