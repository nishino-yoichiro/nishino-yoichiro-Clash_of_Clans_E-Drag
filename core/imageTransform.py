import math
import json
import os
from PIL import Image, ImageDraw
from core.building import Building


class ImageTransformer:
    conversion_dict = {
        "BOMB" : "Bomb",
        "HUT" : "Hut",
        "CANNON" : "Cannon",
        "LAB" : "Labratory",
        "TOWER" : "ArcherTower",
        "MORTAR" : "Mortar",
        "CC" : "ClanCastle",
        "GS" : "GoldStorage",
        "ES" : "ElixirStorage",
        "GM" : "GoldMine",
        "EM" : "ElixirMine",
        "BARRACKS" : "Barracks",
        "CAMP" : "ArmyCamp",
        "TH" : "TownHall"
    }
    @staticmethod
    def rotate_coordinates(x, y, cx, cy, angle):
        """ Rotate a point around a center point by a given angle in degrees. The angle is measured in degrees, counter-clockwise.
        :param x: x-coordinate of the point to rotate
        :param y: y-coordinate of the point to rotate
        :param cx: x-coordinate of the center point
        :param cy: y-coordinate of the center point
        :param angle: angle in degrees
        :type int, int, int, int, int
        :rtype int, int
        :return: x, y coordinates of the rotated point
        """
        x_prime = x - cx
        y_prime = y - cy
        angle_rad = math.radians(angle)
        x_double_prime = x_prime * math.cos(angle_rad) + y_prime * math.sin(angle_rad)
        y_double_prime = -x_prime * math.sin(angle_rad) + y_prime * math.cos(angle_rad)
        x_final = x_double_prime + cx
        y_final = y_double_prime + cy
        return x_final, y_final
    
    def find_edges(self, data):
        """ Find the edges of the image based on the outermost buildings
        :param data: json data containing the image and predictions
        :type dict
        :rtype: Tuple
        :return: Tuple containing the minimum x, minimum y, maximum x, and maximum y coordinates
        """
        min_x = 100000
        min_y = 100000
        max_x = -100000
        max_y = -100000

        for prediction in data["predictions"]:
            x, y = prediction["x"], prediction["y"]
            width, height = prediction["width"], prediction["height"]
            min_x = min(min_x, x - width / 2)
            min_y = min(min_y, y - height / 2)
            max_x = max(max_x, x + width / 2)
            max_y = max(max_y, y + height / 2)

        return min_x, min_y, max_x, max_y

    def create_building_list(self, data):
        """ Create a list of Building objects from the json data, converting coordinates to a 44x44 grid
        :param data: json data containing the image and predictions
        :type dict
        :rtype list
        :return: List of Building objects
        """
        building_list = []

        diamond_length = math.sqrt(44**2 + 44**2)
        scale_x = data["image"]["width"] / diamond_length
        scale_y = data["image"]["height"] / diamond_length

        center_x = self.find_edges(data)[0] + (self.find_edges(data)[2] - self.find_edges(data)[0]) / 2
        center_y = self.find_edges(data)[1] + (self.find_edges(data)[3] - self.find_edges(data)[1]) / 2
        center_x /= scale_x
        center_y /= scale_y

        for prediction in data["predictions"]:
            name = self.conversion_dict[prediction["class"]]
            cx, cy = prediction["x"], prediction["y"]
            cx /= scale_x
            cy /= scale_y
            width, height = prediction["width"], prediction["height"]
            width /= scale_x
            height /= scale_y
            x = cx - width
            y = cy

            rotated_coordinates = self.rotate_coordinates(y, x, center_y, center_x, 45)
            rotated_coordinates = (rotated_coordinates[0] / diamond_length * 44, rotated_coordinates[1] / diamond_length * 44)
            rotated_coordinates = (round(rotated_coordinates[0]), round(rotated_coordinates[1]))
            Building.from_type(name, rotated_coordinates)

        return building_list
    
    def unrotate_coordinates(self, data, dragon_data):
        """ Unrotate the coordinates of the dragons to match the original image
        :param data: json data containing the image and predictions
        :param dragon_data: List of dragon coordinates
        :type dict, list
        :rtype list
        :return: List of unrotated dragon coordinates
        """
        unrotated_coordinates = []
        diamond_length = math.sqrt(44**2 + 44**2)
        height = data["image"]["height"]
        width = data["image"]["width"]
        for dragon in dragon_data:
            x, y = dragon[0], dragon[1]
            rotated_coordinates = self.rotate_coordinates(x, y, 22, 22, -45)
            rotated_coordinates = (rotated_coordinates[0] / 44 * height, rotated_coordinates[1] / 44 * width)
            unrotated_coordinates.append((rotated_coordinates[1], rotated_coordinates[0]))
        return unrotated_coordinates

    def overlay_dragons_on_image(self, base_image, dragon_coordinates, output_image):
        """ Overlay the dragon icons on the base image
        :param base_image: Path to the base image
        :param dragon_coordinates: List of dragon coordinates
        :param output_image: Path to the output image
        :type str, list, str
        :rtype void
        :return None
        """
        base_image = Image.open(base_image)
        draw = ImageDraw.Draw(base_image)

        image_width, image_height = base_image.size
        image_width /= 44
        image_height /= 44
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "../assets/electro_dragon_icon.webp")
        icon = Image.open(icon_path)
        icon_size = (round(image_width), round(image_width))
        icon = icon.resize(icon_size, Image.LANCZOS)

        for (row, col) in dragon_coordinates:
            x, y = row, col
            radius = 5
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='blue', outline='blue')
            base_image.paste(icon, (round(x), round(y - image_width)), icon)

        base_image.save(output_image)





