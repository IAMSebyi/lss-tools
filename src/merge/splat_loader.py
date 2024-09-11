import struct
import os


class SplatLoader:
    def __init__(self, dir_path: str):
        """
        Initializes the SplatLoader with the path to the scene directory.

        :param dir_path: Path to the directory containing GS results of the split scenes.
        """
        self.dir_path = dir_path

    def load_splats(self):
        """
        Loads the Gaussian Splatting results from all .ply files in the directory.

        :return: dict
            A dictionary containing the GS results of the split scenes, where the keys are the respective row and column
            computed during splitting and the values are a list of splats
        """
        splats = {}

        # Iterate over all the .ply files in the directory
        for file_name in os.listdir(self.dir_path):
            # Check if the file is a .ply file
            if file_name.endswith('.ply'):
                file_path = os.path.join(self.dir_path, file_name)
                print(f"Found {file_name}")

                # Extract the row and column information from the filename (e.g., "1_2.ply")
                row, col = map(int, file_name.split('.')[0].split('_'))
                print(f"Loading splats for cell: {row, col}...")

                # Open the .ply file and read its contents
                with open(file_path, 'rb') as ply_file:
                    # Skip the header part
                    while True:
                        line = ply_file.readline().decode('utf-8').strip()
                        if line == "end_header":
                            break

                    splat_data = []

                    # Read until end of file
                    while True:
                        # Read the binary content for each vertex (assuming vertex data is 248 bytes per vertex)
                        vertex_data = ply_file.read(248)
                        if not vertex_data:
                            break  # End of file

                        # Unpack the binary data
                        try:
                            data = struct.unpack('<fff fff 48f f fff ffff', vertex_data)
                            splat = {
                                'position': data[:3],
                                'normal': data[3:6],
                                'features_dc': data[6:9],
                                'features_rest': data[9:57],
                                'opacity': data[57],
                                'scale': data[58:61],
                                'rotation': data[61:65]
                            }
                            splat_data.append(splat)
                        except struct.error:
                            print(f"Error unpacking vertex data from {file_name}")
                            break

                # Store the splat data in the dictionary using the (row, col) as keys
                splats[(row, col)] = splat_data

        print(f"Total cells loaded: {len(splats)}")
        return splats

    @staticmethod
    def load_cells(filepath: str):
        """
        Loads cell boundaries from the cell_boundaries.txt file.

        :param filepath: Path to the cell_boundaries.txt file.
        :return: dict
            A dictionary where the keys are (row, col) tuples and the values are dictionaries with 'min' and 'max' keys
            containing the boundary points.
        """
        cell_boundaries = {}

        with open(filepath, 'r') as file:
            while True:
                line = file.readline().strip()
                if not line:
                    break

                # Parse the row and column
                row, col = map(int, line.split())

                # Parse the boundary points (min and max)
                min_line = file.readline().strip()
                max_line = file.readline().strip()

                min_x, min_z = map(float, min_line.split())
                max_x, max_z = map(float, max_line.split())

                # Store the boundary information in the dictionary
                cell_boundaries[(row, col)] = {
                    'min': [min_x, min_z],
                    'max': [max_x, max_z]
                }

        return cell_boundaries
