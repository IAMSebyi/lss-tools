import matplotlib.pyplot as plt


class SceneVisualizer:
    def __init__(self, projected_scene):
        """
        Initializes the Scene Visualizer with the projected 2D scene data.

        :param projected_scene: dict
            A dictionary containing:
            - "points": A numpy array of projected 3D points (2D coordinates)
            - "cameras": A numpy array of projected camera positions (2D coordinates)
        """
        self.projected_scene = projected_scene

    def plot_scene(self, filename='projected_scene.png'):
        """
        Plots the 2D projection of the scene, including points and cameras,
        and saves the plot to a file.

        :param filename: str
            The name of the file to save the plot to.
        """
        # Extract points and cameras
        points = self.projected_scene["points"]
        cameras = self.projected_scene["cameras"]

        # Create a new figure
        plt.figure(figsize=(10, 8))

        # Plot points
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
        plt.close()  # Close the figure to free up memory
