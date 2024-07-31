class Building:
    id_counter = 0
    instance_counts = {}
    building_list = []
    BUILDING_TYPES = {
        "Bomb" : 1,
        "Hut" : 4,
        "Cannon" : 9,
        "Labratory" : 9,
        "ArcherTower" : 9,
        "Mortar" : 9,
        "ClanCastle" : 9,
        "GoldStorage" : 9,
        "ElixirStorage" : 9,
        "GoldMine" : 9,
        "ElixirMine" : 9,
        "Barracks" : 9,
        "ArmyCamp" : 16,
        "TownHall" : 16
    }
    NAME_SHORTCUTS = {
        "Bomb" : "BO",
        "Hut" : "HU",
        "Cannon" : "CA",
        "Labratory" : "LA",
        "ArcherTower" : "AT",
        "Mortar" : "MO",
        "ClanCastle" : "CC",
        "GoldStorage" : "GS",
        "ElixirStorage" : "ES",
        "GoldMine" : "GM",
        "ElixirMine" : "EM",
        "Barracks" : "BA",
        "ArmyCamp" : "AC",
        "TownHall" : "TH"
        
    }
    BUILDING_HEALTH = {
        "Bomb": 73,
        "Hut": 250,
        "Cannon": 420,
        "Laboratory": 500,
        "ArcherTower": 380,
        "Mortar": 400,
        "ClanCastle": 1200,
        "GoldStorage": 400,
        "ElixirStorage": 400,
        "GoldMine": 400,
        "ElixirMine": 400,
        "Barracks": 250,
        "ArmyCamp": 150,
        "TownHall": 1600
    }
    def __init__(self, size, name, top_left_coordinates):
        """
        Initializes a new Building instance.
        
        :param int size: The size of the building (e.g., 4, 9, 16)
        :param str name: The name of the building
        :param tuple top_left_coordinates: The (x, y) coordinates of the building's top-left corner
        """
        self.size = size
        self.name = name
        self.top_left_coordinates = top_left_coordinates
        self.health = self.BUILDING_HEALTH.get(name, 0)
        Building.building_list.append(self)

        if name in Building.instance_counts:
            Building.instance_counts[name] += 1
            self.id = Building.instance_counts[name]
        else:
            Building.instance_counts[name] = 1
            self.id = 1


    @classmethod
    def from_type(cls, building_type, top_left_coordinates):
        """
        Alternative constructor to initialize a Building instance using a building type.
        
        :param str building_type: The type of the building (e.g., "small", "medium", "large")
        :param str name: The name of the building
        :param tuple top_left_coordinates: The (x, y) coordinates of the building's top-left corner
        :return: A new Building instance
        :rtype: Building
        """
        size = cls.BUILDING_TYPES.get(building_type)
        if size is None:
            raise ValueError(f"Unknown building type: {building_type}")
        return cls(size, building_type, top_left_coordinates)

    def delete(self):
        """ Deletes the building from the game
        """
        Building.building_list.remove(self)
        Building.instance_counts[self.name] -= 1

    def __repr__(self):
        short_name = self.NAME_SHORTCUTS.get(self.name, self.name[0:2])
        if Building.instance_counts[self.name] > 1:
            return f"{short_name}_{self.id}" # for example, "TH_0", help for debugging
        return f"{short_name}"