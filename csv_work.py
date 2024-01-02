import csv


def import_csv_layout(path):
    terrain_map = []
    with open(path) as layout_csv_file:
        level = csv.reader(layout_csv_file, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
