class SplatMerger:
    def __init__(self, splats, cells):
        """
        Initializes the SplatMerger with the splats and cells dictionaries

        :param splats: dict
            A dictionary containing the GS results of the split scenes
        :param cells: dict
            A dictionary containing the cell boundaries of the split scenes
        """
        self.splats = splats
        self.cells = cells

    def cull_gaussians(self):
        """
        Removes the Gaussians that fall outside the cell boundaries for each scene

        :return: dict
            A dictionary containing the GS results of the split scenes after boundary-based culling,
            where the keys are the respective row and column computed during splitting and the values are a list of splats
        """
        new_splats = {}
        for pos, splat in self.splats.items():
            cell = self.cells.get((pos[0], pos[1]))
            if cell is None:
                print(f"Warning: Cell boundaries for position {pos} not found.")
                continue

            min_point = cell['min']
            max_point = cell['max']

            # Get Gaussians that fall inside the cell bounding box region
            remaining_splat_data = [
                gauss for gauss in splat
                if min_point[0] <= gauss['position'][0] < max_point[0]
                and min_point[1] <= gauss['position'][1] < max_point[1]
            ]

            print(f"Cell {pos}: {len(splat)} splats before culling, {len(remaining_splat_data)} splats after culling")
            new_splats[pos] = remaining_splat_data

        return new_splats

    def merge_splats(self):
        """
        Merges all culled Gaussians into a single list representing the complete scene

        :return: list
            A list containing all the remaining Gaussians after culling
        """
        # First, cull the Gaussians based on cell boundaries
        culled_splats = self.cull_gaussians()

        # Initialize an empty list to hold all merged splats
        complete_splat = []

        # Log the number of cells being merged
        print(f"Merging splats from {len(culled_splats)} cells")

        # Efficiently merge all splats from each cell
        for pos, splat_list in culled_splats.items():
            print(f"Merging cell {pos} with {len(splat_list)} splats")
            complete_splat.extend(splat_list)

        return complete_splat
