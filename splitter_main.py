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
    scene = cl.load_scene()

    # Split complete scene
    ss = SceneSplitter(scene, 2, 2)
    split_scenes = ss.split_scene()

    for grid_pos, cell_scene in split_scenes:
        # Project the cell scene in 2D
        gpp = GroundPlaneProjector(cell_scene)
        projected_scene = gpp.project_to_2d()

        # Convert row and column to string
        str_row = str(grid_pos[0])
        str_col = str(grid_pos[1])

        # Visualize the cell scene in 2D
        sv = SceneVisualizer(projected_scene)
        sv.plot_scene2D('rubble2d_' + str_row + '_' + str_col + '.png')

        # Export the cell scene in COLMAP format
        output_dir = 'data/output/rubble/' + str_row + '_' + str_col
        se = SceneExporter(cell_scene, output_dir)
        se.export_scene()


if __name__ == '__main__':
    main()
