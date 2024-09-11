from src.merge.splat_loader import SplatLoader
from src.merge.splat_merger import SplatMerger
from src.merge.splat_exporter import SplatExporter


def main():
    # Define path
    splats_dir = 'splats/rubble/split'
    cells_path = 'data/output/rubble/cell_boundaries.txt'
    output_path = 'splats/rubble/full/rubble.ply'

    # Load split scenes' GS results
    sl = SplatLoader(splats_dir)
    splats = sl.load_splats()

    # Load cell boundaries information
    cells = sl.load_cells(cells_path)

    # Merge split splats
    sm = SplatMerger(splats, cells)
    merged_splat = sm.merge_splats()

    # Export merged splat
    se = SplatExporter(merged_splat, output_path)
    se.export_splat()


if __name__ == '__main__':
    main()
