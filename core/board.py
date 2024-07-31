import numpy as np
import os
from math import sqrt
from scipy.spatial import KDTree
from core.building import Building
from core.graph import Graph
from core.model import ModelInference
from core.imageTransform import ImageTransformer

def initialize_board(base_image_path):
    """ Initializes the board with buildings and returns the board and graph.
    :param str base_image_path: path to the base image
    :type str
    :rtype 2D array, Graph, dict
    :return 44x44 string array, graph of buildings, json output from the model"""
    board = create_board()
    api_key = os.getenv("ROBOFLOW_API_KEY")
    model = ModelInference(api_key)

    output = model.get_inference_output(base_image_path)
    transformer = ImageTransformer()
    transformer.create_building_list(output)

    for building in Building.building_list:
        insert_building(board, building)

    graph = create_graph(board, Building.building_list)

    return board, graph, output

def create_board():
    """ Returns a new Clash of Clans board in form of 44x44 array.
    :param void
    :type None
    :rtype 2D array
    :return board: 44x44 string array
    """

    board = np.full((44, 44), ".", dtype=str) # For better alignment, print board only shows the 1st character as opposed to 'U3'
    return board

def create_graph(board, buildings):
    """ Builds a graph of buildings and their adjacencies.
    :param 2D array board: 44x44 array of Building objects or None
    :param list buildings: list of Building objects
    :rtype Graph
    :return graph: graph of buildings
    """
    graph = Graph()
    for building in buildings:
        graph.add_node(building)
    coordinates = [building.top_left_coordinates for building in buildings]
    kd_tree = KDTree(coordinates)

    for i, building in enumerate(buildings):
        coords = building.top_left_coordinates
        indices = kd_tree.query_ball_point(coords, sqrt(72), return_sorted=True)
        for index in indices:
            if index != i:
                if(are_buildings_adjacent(building, buildings[index])):
                    if (buildings[index], 0) not in graph.get_neighbors(building):
                        distance = find_distance(building, buildings[index])
                        graph.add_edge(building, buildings[index], distance)
    return graph

def print_board(board):
    """ Prints the current Clash of Clans board.
    :param 2D array board: 44x44 string array
    :type 2D array
    :rtype void
    :return None
    """
    for row in board:
        print(" ".join(row))

def insert_building(board, building):
    """ Inserts a building into the board.
    :param 2D array board: 44x44 string array
    :param Building building: building to insert
    :type 2D array, Building
    :rtype void
    :return None
    """
    row, col = building.top_left_coordinates
    length = int(sqrt(building.size))
    for i in range(row, row + length):
        for j in range(col, col + length):
            board[i][j] = str(building)

def find_building(board, building):
    """ Returns a list of all buildings in the board.
    :param 2D array board: 44x44 string array
    :param Building building: building to find
    :type 2D array, Building
    :rtype Building
    :return buildings: Building object if found, None otherwise
    """
    for b in Building.building_list:
        if building == b:
            return b
    return None

def find_distance(building1, building2):
    """ Returns the distance between two buildings.
    :param Building building1: first building
    :param Building building2: second building
    :type Building, Building
    :rtype float
    :return distance: distance between two buildings. If the two are direct neighbors (have touching tiles), return # of tiles touching, else return the Euclidean distance between the two buildings
    """
    row1, col1 = building1.top_left_coordinates
    length1 = int(sqrt(building1.size))
    row2, col2 = building2.top_left_coordinates
    length2 = int(sqrt(building2.size))

    horizontal_distance = col1 - col2
    vertical_distance = row1 - row2
    actual_horizontal_distance, actual_vertical_distance = None, None

    if(horizontal_distance < 0):
        actual_horizontal_distance = col2 - (col1 + length1)
    else:
        actual_horizontal_distance = col1 - (col2 + length2)
    if(vertical_distance < 0):
        actual_vertical_distance = row2 - (row1 + length1)
    else:
        actual_vertical_distance = row1 - (row2 + length2)
    
    if actual_horizontal_distance < 0 and actual_vertical_distance <= 0 or actual_vertical_distance < 0 and actual_horizontal_distance <= 0:
        return actual_vertical_distance + actual_horizontal_distance
    else:
        if actual_horizontal_distance < 0:
            actual_horizontal_distance = 0
        if actual_vertical_distance < 0:
            actual_vertical_distance = 0
        return sqrt(actual_horizontal_distance ** 2 + actual_vertical_distance ** 2)

def find_nearest_neighbor(building, graph):
    """ Returns the nearest neighbor of a building.
    :param Building building: building to find the nearest neighbor of
    :param Graph graph: graph of buildings
    :type Building, Graph
    :rtype Building
    :return nearest_neighbor: nearest neighbor of the building
    """
    neighbors = graph.get_neighbors(building)
    nearest_neighbor = None
    min_distance = sqrt(44**2 + 44**2)
    for neighbor in neighbors:
        if neighbor[1] < min_distance:
            min_distance = neighbor[1]
            nearest_neighbor = neighbor[0]
        elif neighbor[1] == min_distance:
            if nearest_neighbor != None and (neighbor[0]).health > nearest_neighbor.health:
                nearest_neighbor = neighbor[0]
            if nearest_neighbor == None:
                nearest_neighbor = neighbor[0]
    print(building, nearest_neighbor)
    return nearest_neighbor

def find_nearest_neighbor_not_visited(building, graph, visited):
    """ Returns the nearest neighbor of a building that has not been visited.
    :param Building building: building to find the nearest neighbor of
    :param Graph graph: graph of buildings
    :param set visited: set of visited buildings
    :type Building, Graph, set
    :rtype Building
    :return nearest_neighbor: nearest neighbor of the building that has not been visited
    """
    neighbors = graph.get_neighbors(building)
    nearest_neighbor = None
    min_distance = sqrt(44**2 + 44**2)
    for neighbor in neighbors:
        if neighbor[0] not in visited and neighbor[1] < min_distance:
            min_distance = neighbor[1]
            nearest_neighbor = neighbor[0]
        elif neighbor[0] not in visited and neighbor[1] == min_distance:
            if nearest_neighbor != None and (neighbor[0]).health > nearest_neighbor.health and neighbor[0] not in visited:
                nearest_neighbor = neighbor[0]
            if nearest_neighbor == None and neighbor[0] not in visited:
                nearest_neighbor = neighbor[0]
    return nearest_neighbor

def are_buildings_adjacent(building1, building2):
    """ Returns True if two buildings are adjacent, False otherwise.
    :param Building building1: first building
    :param Building building2: second building
    :type Building, Building
    :rtype bool
    :return True if buildings are adjacent, False otherwise
    """
    row1, col1 = building1.top_left_coordinates
    length1 = int(sqrt(building1.size))
    row2, col2 = building2.top_left_coordinates
    length2 = int(sqrt(building2.size))

    horizontal_distance = col1 - col2
    vertical_distance = row1 - row2
    horizontal_check, vertical_check = False, False

    if(horizontal_distance < 0):
        horizontal_check = col1 + length1 + 1 >= col2
    else:
        horizontal_check = col2 + length2 + 1 >= col1
    if(vertical_distance < 0):
        vertical_check = row1 + length1 + 1>= row2
    else:
        vertical_check = row2 + length2 + 1>= row1

    return horizontal_check and vertical_check

def group_buildings(graph, buildings):
    chains = []

    def dfs(visited, node, chain, counter):
        next = find_nearest_neighbor_not_visited(node, graph, visited)
        if next is not None and next not in visited:
            visited.add(next)
            counter[0] += 1
            chain.append(next)
            dfs(visited, next, chain, counter)
    
    for building in buildings:
        chain = [building]
        counter = [1]
        visited = set()
        visited.add(building)
        dfs(visited, building, chain, counter)
        chains.append((chain, counter[0]))

    sorted_chains = sorted(chains, key=lambda x: x[1], reverse=True)
    return sorted_chains

def find_adjacent_buildings(board, buildings):
    """ Builds a graph of buildings and their adjacencies.
    :param 2D array board: 44x44 array of Building objects or None
    :param list buildings: list of Building objects
    :rtype Graph
    :return graph: graph of buildings
    """
    graph = Graph()
    for building in buildings:
        graph.add_node(building)
        row, col = building.center_coordinates
        if row > 0 and board[row - 1][col] is not None:
            graph.add_edge(building, board[row - 1][col])
        if row < 43 and board[row + 1][col] is not None:
            graph.add_edge(building, board[row + 1][col])
        if col > 0 and board[row][col - 1] is not None:
            graph.add_edge(building, board[row][col - 1])
        if col < 43 and board[row][col + 1] is not None:
            graph.add_edge(building, board[row][col + 1])
    return graph

def eliminate_building(graph, board, building):
    """ Eliminates a building from the board.
    :param 2D array board: 44x44 string array
    :param Building building: building to eliminate
    :type 2D array, Building
    :rtype void
    :return None
    """
    row, col = building.top_left_coordinates
    length = int(sqrt(building.size))
    for i in range(row, row + length):
        for j in range(col, col + length):
            board[i][j] = "X"
    Building.delete(building)
    graph.delete_node(building)

def find_surrounding_tiles(board, building):
    """ Returns a list of all surrounding tiles of a building.
    :param 2D array board: 44x44 string array
    :param Building building: building to find the surrounding tiles of
    :type 2D array, Building
    :rtype list
    :return surrounding_tiles: list of all surrounding tiles of the building
    """

    row, col = building.top_left_coordinates
    length = int(sqrt(building.size))
    surrounding_tiles = []
    for i in range(row - 3, row + length + 3):
        for j in range(col - 3, col + length + 3):
            if i >= 0 and i < 44 and j >= 0 and j < 44 and (i < row - 1 or i >= row + length + 1 or j < col - 1 or j >= col + length + 1):
                surrounding_tiles.append((i, j))
    return surrounding_tiles

def valid_tile(board, row, col):
    """ Returns True if the eight surrounding pixels are empty, False otherwise.
    :param 2D array board: 44x44 string array
    :param int row: row index
    :param int col: column index
    :type 2D array, int, int
    :rtype bool
    :return True if the tile is at least one tile away from a building, False otherwise
    """
    if row > 0 and board[row - 2][col] != "." and board[row - 2][col] != "X":
        return False
    if row < 43 and board[row + 2][col] != "." and board[row + 2][col] != "X":
        return False
    if col > 0 and board[row][col - 2] != "." and board[row][col - 2] != "X":
        return False
    if col < 43 and board[row][col + 2] != "." and board[row][col + 2] != "X":
        return False
    if row > 0 and col > 0 and board[row - 2][col - 2] != "." and board[row - 2][col - 2] != "X":
        return False
    if row > 0 and col < 43 and board[row - 2][col + 2] != "." and board[row - 2][col + 2] != "X":
        return False
    if row < 43 and col > 0 and board[row + 2][col - 2] != "." and board[row + 2][col - 2] != "X":
        return False
    if row < 43 and col < 43 and board[row + 2][col + 2] != "." and board[row + 2][col + 2] != "X":
        return False
    if board[row][col] != "." and board[row][col] != "X":
        return False
    return True  

def place_electro_dragons(board, chains, num_dragons):
    """ Places Electro Dragons on non-overlapping valid tiles with highest chain rate.
    :param 2D array board: 44x44 string array
    :param list chains: list of chains of buildings
    :param int num_dragons: number of Electro Dragons to place
    :type 2D array, list, int
    :rtype list
    :return list of Electro Dragons placed on the board
    """
    visited = set()
    dragons = []
    while num_dragons > 0:
        if(len(Building.building_list) == len(visited)):
            visited = set()
        for chain in chains:
            starting_building = chain[0][0]
            if(starting_building not in visited):
                if len(chain[0]) == 1:
                    next_building = starting_building   
                else:
                    next_building = chain[0][1]
                surrounding_tiles = find_surrounding_tiles(board, starting_building)
                best_tile = None
                best_distance = None
                for i, j in surrounding_tiles:
                    if valid_tile(board, i, j):
                        distance = sqrt((i - next_building.top_left_coordinates[0])**2 + (j - next_building.top_left_coordinates[1])**2)
                        if best_tile is None or distance < best_distance:
                            best_tile = (i,j)
                            best_distance = distance
                if best_tile is not None:
                    board[best_tile[0]][best_tile[1]] = "Z"
                    dragons.append((best_tile[0], best_tile[1]))
                    num_dragons -= 1
            for building in chain[0]:
                if building not in visited:
                    visited.add(building)
            if num_dragons == 0:
                return dragons

def process_dragons(board, graph, output, buildings, base_image_path, output_image_path):
    """ Processes the Electro Dragons and overlays them on the base image.
    :param 2D array board: 44x44 string array
    :param Graph graph: graph of buildings
    :param dict output: json output from the model
    :param list buildings: list of Building objects
    :param str base_image_path: path to the base image
    :param str output_image_path: path to the output image
    :type 2D array, Graph, dict, list, str, str
    :rtype void
    :return None
    """
    transformer = ImageTransformer()
    chains = group_buildings(graph, buildings)
    dragons = place_electro_dragons(board, chains, 6)
    dragons = transformer.unrotate_coordinates(output, dragons)
    transformer.overlay_dragons_on_image(base_image_path, dragons, output_image_path)

