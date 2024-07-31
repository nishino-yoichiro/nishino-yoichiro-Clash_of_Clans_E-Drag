from core.board import print_board, initialize_board, process_dragons
from core.building import Building

def process_image(base_image_path, output_image_path):
    board, graph, output = initialize_board(base_image_path)
    process_dragons(board, graph, output, Building.building_list, base_image_path, output_image_path)

def main():
    base_image_path = "assets/COC_24.webp"
    output_image_path = "assets/output.jpg"
    process_image(base_image_path, output_image_path)

if __name__ == "__main__":
    main()