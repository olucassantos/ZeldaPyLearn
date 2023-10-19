from csv import reader

# Recebe o caminho do arquivo CSV e retorna uma lista com o mapa
def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        layout = reader(level_map, delimiter= ',')
        for row in layout:
            terrain_map.append(list(row))        
        
        return terrain_map