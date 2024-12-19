crystals_data = {"red": "images/crystals/Dark_red_ crystal2.png",
                 "blue": "images/crystals/Blue_crystal2.png",
                 "gold": "images/crystals/Yellow_crystal2.png",
                 "purple": "images/crystals/Violet_crystal2.png",
                 "white": "images/crystals/White_crystal2.png"}
class Crystal:
    def __init__(self, rectangle, color, crystals_data):
        self.rectangle = rectangle
        self.color = color
        self.image = crystals_data[color]