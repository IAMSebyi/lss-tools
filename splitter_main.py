from src.common.colmap_loader import COLMAPLoader
from src.splitter.scene_splitter import SceneSplitter


def main():
    # Define path
    path = 'data/input/rubble/train/sparse/0'

    # Load COLMAP scene
    cl = COLMAPLoader(path_to_scene=path)
    scene = cl.load_scene()

    ss = SceneSplitter(scene, 2, 2)
    split_scenes = ss.split_scene()


if __name__ == '__main__':
    main()
