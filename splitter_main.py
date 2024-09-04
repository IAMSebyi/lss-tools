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
    ss = SceneSplitter(scene, 25, 25, num_of_points)
    split_scenes = ss.split_scene()

    for grid_pos, cell_scene in split_scenes:
        # Convert row and column to string
        str_row = str(grid_pos[0])
        str_col = str(grid_pos[1])

        # Export the cell scene in COLMAP format
        output_dir = 'data/output/rubble2/' + str_row + '_' + str_col + '/colmap/sparse/0'
        se = SceneExporter(cell_scene, output_dir)
        se.export_scene()

        # Project the cell scene in 2D
        gpp = GroundPlaneProjector(cell_scene)
        projected_scene = gpp.project_to_2d()

        # Visualize the cell scene in 2D
        sv = SceneVisualizer(projected_scene)
        sv.plot_scene2D('rubble2d_' + str_row + '_' + str_col + '.png')


if __name__ == '__main__':
    main()
