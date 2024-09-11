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
        num_of_points, num_of_cameras, scene = cl.load_scene()

        # Project scene in 2D
        gpp = GroundPlaneProjector(scene=scene)
        projected_scene = gpp.project_to_2d()

        # Visualize 2D scene
        sv2d = SceneVisualizer(scene=projected_scene)
        sv2d.plot_scene2D(ds + '2d.png', False)

        # Visualize 3D scene
        sv3d = SceneVisualizer(scene=scene)
        sv3d.plot_scene3D(ds + '3d.png', False)


if __name__ == '__main__':
    main()
