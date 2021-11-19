from ressources.graphics.graphics import *

class Graph:
    def __init__(self, w: int, h: int, x: int, y: int, values: tuple, label:str=None):
        self.width = w
        self.height = h

        self.xpos = x
        self.ypos = y

        if label: self.label = label
        else: self.label = "some_graph"

        self.background = Rectangle(Point(x, y), Point(x+w, y+h))
        self.background.config = {"fill":"lightblue"}

        self.frame = Rectangle(Point(x, y), Point(x+w, y+h))
        self.frame.config = {
            "outline":"black",
            "width":"5"
        }

        self.points = []
        self.lines = []
        self.components = []

        # gets the interval in which the lines/points shall be printed horizontically
        self.interval = self.width/(len(values)-1)

        last_point = Point(0,0)
        for no in range(len(values)):
            if no == 0:
                last_point = Point(self.xpos, self.ypos+values[0])

                # saving points for showing labels afterwards
                self.points.append(last_point)
            else:
                try:
                    new_point = Point(self.xpos+self.interval*no, self.ypos+values[no])
                    self.lines.append(Line(last_point, new_point))
                    last_point = new_point

                    # saving points for showing labels afterwards
                    self.points.append(last_point)
                except Exception as e: print("%s\n\noh no" % e)

    def show(self, graphwin, options: tuple):
        '''options: drawLines, showLabels'''
        self.background.draw(graphwin)

        for line in self.lines: line.draw(graphwin)

        self.frame.draw(graphwin)

        labels = []
        if "drawLabels" in options:
            for no, point in enumerate(self.points):
                labels.append(Text(point, f"p{no+1}"))

            for label in labels:
                label.setTextColor("black")
                #label.setStyle("bold")
                label.draw(graphwin)

        lines = []
        if "drawLines" in options:
            for no, point in enumerate(self.points):
                if no == 0: continue
                _line = Line(\
                    Point(self.xpos+self.interval*no, self.ypos),\
                    Point(self.xpos+self.interval*no, self.ypos+self.height)
                    )
                _line.config = {"fill":"darkgrey"}
                lines.append(_line)

        if "drawGraphLabel" in options:
            lbl = Text(Point(70, self.height-20), self.label)
            lbl.setSize(12)
            self.components.append(lbl)

        for line in lines: line.draw(graphwin)
        for comp in self.components: comp.draw(graphwin)