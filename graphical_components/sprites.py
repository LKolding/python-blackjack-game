from ressources.graphics.graphics import *

ImageURLS = {
    "Clubs" : "ressources/images/clubs.svg",
    "Spades" : "ressources/images/spades.svg",
    "Hearts": "ressources/images/hearts.svg",
    "Hiamonds" : "ressources/images/diamonds.svg"
}
class RoomValues:
    tableColor = color_rgb(95, 0, 0),
    tableLegColor = "Grey",
    floorColor = color_rgb(0, 100, 5),
    wallColor = color_rgb(145, 145, 145)
    
def getCardText(p: Point, text: str, color: str):
    rtxt = Text(p, text)
    rtxt.setTextColor(color)
    return rtxt

class CardSprite:
    '''CardSprite class. Has a predefined size tuple of 40x56.
    flipped is for only drawing backside of the card'''
    def __init__(self, no, suit, xpos, ypos, size=(40, 56), flipped=False):
        self.components = []
        self.suit = suit
        self.no = no
        self.flipped = flipped

        self.ypos = ypos
        self.xpos = xpos

        self.width = size[0]
        self.height = size[1]
        self._create_components()

    def _create_components(self):
        if self.flipped:
            card_background = Rectangle(
            Point(self.xpos, self.ypos), 
            Point(self.xpos+self.width, self.ypos+self.height)
            )
            card_background.setFill("black")
            self.components.append(card_background)

        else:
            card_background = Rectangle(
                Point(self.xpos, self.ypos), 
                Point(self.xpos+self.width, self.ypos+self.height)
                )
            card_background.setFill("white")
            if self.suit == "Spades" or self.suit == "Clubs": text_color = "Black"
            elif self.suit == "Diamonds" or self.suit == "Hearts": text_color = "Red"

            if self.no == 1 or self.no == 11:
                top_no_text = getCardText(Point(self.xpos+(0.16*self.width), self.ypos+(0.16*self.height)), "A", text_color)
                bot_no_text = getCardText(Point(self.xpos+(0.84*self.width), self.ypos+(0.84*self.height)), "A", text_color)
            else:
                top_no_text = getCardText(Point(self.xpos+(0.16*self.width), self.ypos+(0.16*self.height)), self.no, text_color)
                bot_no_text = getCardText(Point(self.xpos+(0.84*self.width), self.ypos+(0.84*self.height)), self.no, text_color)
                

            suit_text = getCardText(Point(self.xpos+0.5*self.width, self.ypos+0.5*self.height), self.suit, text_color)
            #suit_image = Image(Point(self.xpos+0.5*self.width, self.ypos+0.5*self.height), ImageURLS[self.suit])

            self.components.append(card_background)
            self.components.append(suit_text)
            #self.components.append(suit_image)
            self.components.append(top_no_text)
            self.components.append(bot_no_text)


    def draw(self, graphwin):
        for comp in self.components:
            comp.draw(graphwin)

class Table:
    # takes four points as an argument
    def __init__(self, points: tuple):
        self.components = []
        if len(points) != 4: raise Exception("Table must recieve 4, and only 4, points")
        self.points = points
        self.color = RoomValues.tableColor

        self._create_components()

    def _create_components(self):
        table_polygon = Polygon(*self.points)
        table_polygon.config = {"fill" : self.color, "outline":"black"}
        self.components.append(table_polygon)
        # TODO: maybe add an outline around the table?

    def draw(self, graphwin):
        for comp in self.components: comp.draw(graphwin)
        
class Floor:
    def __init__(self,x, y):
        self.components = []
        self.xpos = x
        self.ypos = y
        self.color = RoomValues.floorColor
        self._create_components()

    def _create_components(self):
        floor_rectangle = Rectangle(self.xpos, self.ypos)
        floor_rectangle.config = {"fill" : self.color}
        self.components.append(floor_rectangle)

    def draw(self, graphwin):
        for comp in self.components: comp.draw(graphwin)

class Wall:
    def __init__(self,x, y):
        self.components = []
        self.xpos = x
        self.ypos = y
        self.color = RoomValues.wallColor
        self._create_components()

    def _create_components(self):
        wall_rectangle = Rectangle(self.xpos, self.ypos)

        wall_rectangle.config = {"fill":self.color}
        self.components.append(wall_rectangle)

    def draw(self, graphwin):
        for comp in self.components: comp.draw(graphwin)

class Dealer:
    def __init__(self): pass

    def draw(self, graphwin): pass

class Room:
    def __init__(self, frame_width, frame_height, frame_x, frame_y):
        self.components = []
        self.frame_xpos = frame_x
        self.frame_ypos = frame_y

        ## INIT TABLE OBJ
        table_points = {
            "top_left_point" : Point(0.14*frame_width, 0.3*frame_height),
            "top_right_point": Point(0.86*frame_width, 0.3*frame_height),

            "bottom_right_point" : Point(0.92*frame_width, 0.84*frame_height),
            "bottom_left_point" : Point(0.08*frame_width, 0.84*frame_height)
        }
        table = Table((
            table_points["top_left_point"],
            table_points["top_right_point"],
            table_points["bottom_right_point"],
            table_points["bottom_left_point"]
        ))
    
        ## INIT FLOOR OBJ
        floor_points = {
            "top_left_point" : Point(0, 0.4*frame_height),
            "bottom_right_point" : Point(frame_width, frame_height),
        }
        floor = Floor(floor_points["top_left_point"], floor_points["bottom_right_point"])
        
        ## INIT WALL OBJ
        wall_points = {
            "top_left_point":Point(0,0),
            "bottom_right_point":Point(frame_width, 0.4*frame_height)
        }
        wall = Wall(wall_points["top_left_point"], wall_points["bottom_right_point"])
        
        self.components.append(wall)
        self.components.append(floor)
        self.components.append(table)

    def draw(self, graphwin):
        for comp in self.components:
            comp.draw(graphwin)