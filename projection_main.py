from src.common.colmap_loader import COLMAPLoader
from src.common.visualization import SceneVisualizer

from src.projection.ground_plane_projection import GroundPlaneProjector


def main():
    # Large Scale Datasets
    datasets = {'building', 'matrix_city_aerial', 'residence', 'rubble', 'sciart'}

    for ds in datasets:
        # Define path
        path = 'data/input/' + ds + '/train/sparse/0'

        # Load COLMAP scene
        cl = COLMAPLoader(path_to_scene=path)
        scene = cl.load_scene()

        # Project scene in 2D
        gpp = GroundPlaneProjector(scene=scene)
        projected_scene = gpp.project_to_2d()

        # Visualize 2D scene
        sv = SceneVisualizer(projected_scene=projected_scene)
        sv.plot_scene(ds + '.png')


if __name__ == '__main__':
    main()
