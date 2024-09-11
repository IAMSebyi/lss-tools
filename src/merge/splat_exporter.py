import struct


class SplatExporter:
    def __init__(self, splat, output_path: str):
        """
        Initializes the SplatExporter with the splat list and the output path

        :param splat: list
            A list containing all the Gaussian primitives of the complete large scale scene
        :param output_path: str
            A string containing the output directory path to save the mesh of the complete scene
        """
        self.splat = splat
        self.output_path = output_path

    def export_splat(self):
        """
        Exports the Gaussian splat list into a .ply file following the specified format.
        """
        print(f"Exporting {len(self.splat)} splats to {self.output_path}")
        # Create and open the file in binary write mode
        with open(self.output_path, 'wb') as ply_file:
            # Write the header
            ply_file.write(b'ply\n')
            ply_file.write(b'format binary_little_endian 1.0\n')
            ply_file.write(f'element vertex {len(self.splat)}\n'.encode('utf-8'))
            ply_file.write(b'property float x\n')
            ply_file.write(b'property float y\n')
            ply_file.write(b'property float z\n')
            ply_file.write(b'property float nx\n')
            ply_file.write(b'property float ny\n')
            ply_file.write(b'property float nz\n')
            ply_file.write(b'property float f_dc_0\n')
            ply_file.write(b'property float f_dc_1\n')
            ply_file.write(b'property float f_dc_2\n')
            for i in range(45):  # Writing f_rest properties
                ply_file.write(f'property float f_rest_{i}\n'.encode('utf-8'))
            ply_file.write(b'property float opacity\n')
            ply_file.write(b'property float scale_0\n')
            ply_file.write(b'property float scale_1\n')
            ply_file.write(b'property float scale_2\n')
            ply_file.write(b'property float rot_0\n')
            ply_file.write(b'property float rot_1\n')
            ply_file.write(b'property float rot_2\n')
            ply_file.write(b'property float rot_3\n')
            ply_file.write(b'end_header\n')

            # Write the binary content for each Gaussian splat
            for splat in self.splat:
                # Define the format string to match the loaded data
                format_str = '<fff fff 48f f fff ffff'

                # Pack the splat data into binary format
                packed_data = struct.pack(
                    format_str,
                    *splat['position'],  # x, y, z
                    *splat['normal'],  # nx, ny, nz
                    *splat['features_dc'],  # f_dc_0, f_dc_1, f_dc_2
                    *splat['features_rest'],  # f_rest_0 to f_rest_47
                    splat['opacity'],  # opacity
                    *splat['scale'],  # scale_0, scale_1, scale_2
                    *splat['rotation']  # rot_0, rot_1, rot_2, rot_3
                )

                # Write the packed binary data
                ply_file.write(packed_data)
