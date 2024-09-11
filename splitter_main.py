from src.common.colmap_loader import COLMAPLoader
from src.common.visualization import SceneVisualizer

from src.splitter.scene_splitter import SceneSplitter
from src.splitter.scene_exporter import SceneExporter

from src.projection.ground_plane_projection import GroundPlaneProjector


def main():
    # Define path
    path = 'data/input/rubble/train/sparse/0'

    # Load COLMAP scene
    cl = COLMAPLoader(path_to_scene=path)
    num_of_points, num_of_cameras, scene = cl.load_scene()

    # Split complete scene
    rows, cols = 16, 16
    ss = SceneSplitter(scene, rows, cols, num_of_points)
    cells, split_scenes = ss.split_scene()

    # Open a file to write cell boundaries
    output_dir = 'data/output/rubble/'
    with open(output_dir + 'cell_boundaries.txt', 'w') as boundary_file:
        for grid_pos, cell_scene in split_scenes:
            # Convert row and column to string
            str_row = str(grid_pos[0])
            str_col = str(grid_pos[1])

            # Get the cell's min and max points
            cell = cells[grid_pos[0]][grid_pos[1]]
            min_point = cell['min']
            max_point = cell['max']

            # Write the cell boundaries to the file
            boundary_file.write(f"{str_row} {str_col}\n")
            boundary_file.write(f"{min_point[0]} {min_point[1]}\n")
            boundary_file.write(f"{max_point[0]} {max_point[1]}\n")

            # Export the cell scene in COLMAP format
            cell_dir = output_dir + str_row + '_' + str_col + '/colmap/sparse/0'
            se = SceneExporter(cell_scene, cell_dir)
            se.export_scene()

            # Project the cell scene in 2D
            gpp = GroundPlaneProjector(cell_scene)
            projected_scene = gpp.project_to_2d()

            # Visualize the cell scene in 2D
            sv = SceneVisualizer(projected_scene)
            sv.plot_scene2D('rubble2d_' + str_row + '_' + str_col + '.png')


if __name__ == '__main__':
    main()
