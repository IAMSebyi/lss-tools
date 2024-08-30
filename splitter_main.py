from src.common.colmap_loader import COLMAPLoader
from src.common.visualization import SceneVisualizer

from src.splitter.scene_splitter import SceneSplitter

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

    # Project split scenes in 2D and visualize them
    for grid_pos, cell_scene in split_scenes:
        gpp = GroundPlaneProjector(cell_scene)
        projected_scene = gpp.project_to_2d()

        sv = SceneVisualizer(projected_scene)
        sv.plot_scene2D('rubble2d_' + str(grid_pos[0]) + '_' + str(grid_pos[1]) + '.png')


if __name__ == '__main__':
    main()
