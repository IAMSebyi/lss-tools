import matplotlib.pyplot as plt
import numpy as np


class SceneVisualizer:
    def __init__(self, scene):
        """
        Initializes the Scene Visualizer with the projected 2D scene data.

        :param scene: dict
            A dictionary containing:
            - "points": A numpy array of projected 3D points (2D coordinates)
            - "cameras": A numpy array of projected camera positions (2D coordinates)
        """
        self.scene = scene

    def plot_scene2D(self, filename='scene_plot_2D.png', plt_points=True):
        """
        Plots the 2D projection of the scene, including points and cameras,
        and saves the plot to a file.

        :param filename: str
            The name of the file to save the plot to.
        """
        # Extract points and cameras
        if plt_points:
            points = self.scene["points"]
        cameras = self.scene["cameras"]

        # Create a new figure
        plt.figure(figsize=(10, 8))

        # Plot points
        if plt_points:
            plt.scatter(points[:, 0], points[:, 1], color='blue', label='Points', s=1)

        # Plot cameras
        plt.scatter(cameras[:, 0], cameras[:, 1], color='red', label='Cameras', marker='x', s=2)

        # Add labels and legend
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('2D Projection of COLMAP Scene')
        plt.legend()
        plt.grid(True)

        # Remove axis
        plt.axis('off')

        # Save the plot to a file
        plt.savefig(filename)
        print(f"2D scene was plotted to {filename}")

        plt.close()  # Close the figure to free up memory

    def plot_scene3D(self, filename='projected', plt_points=True):
        """
        Plots the 3D projection of the scene, including points and cameras,
        and saves the plot to a file.

        :param filename: str
            The name of the file to save the plot to.
        """
        # Extract points and cameras
        if plt_points:
            points = self.scene["points"]
        cameras = self.scene["cameras"]

        # Convert points and cameras to numpy arrays if they are not already
        if plt_points:
            points_xyz = np.array([point['xyz'] for point in points.values()])
        cameras_tvec = np.array([camera['tvec'] for camera in cameras.values()])

        # Create a new figure
        fig = plt.figure(figsize=(20, 20))
        ax = fig.add_subplot(projection='3d')

        # Plot points
        if plt_points:
            ax.scatter(points_xyz[:, 0], points_xyz[:, 2], points_xyz[:, 1], color='blue', label='Points', s=1)

        # Plot cameras
        ax.scatter(cameras_tvec[:, 0], cameras_tvec[:, 2], cameras_tvec[:, 1], color='red', label='Cameras', s=2)

        # Add labels and legend
        ax.set_xlabel('X Label')
        ax.set_ylabel('Z Label')
        ax.set_zlabel('Y Label')
        ax.set_title('3D Projection of COLMAP Scene')
        ax.legend()
        ax.grid(True)

        # Keep axis
        ax.axis('on')

        # Save the plot to a file
        fig.savefig(filename)
        print(f"3D scene was plotted to {filename}")

        plt.close(fig)  # Close the figure to free up memory
