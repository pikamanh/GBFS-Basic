import sys
from PIL import Image, ImageDraw

class Node:
    def __init__(self, cost, state, parent):
        self.cost = cost
        self.state = state
        self.parent = parent

class Queue:
    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

    def not_empty(self):
        if self.queue:
            return True
        
    def pop(self):
        if self.not_empty():
            list_cost = []
            for node in self.queue:
                list_cost.append(node.cost)
            return self.queue.pop(list_cost.index(min(list_cost)))
        
    def node_inside(self):
        return self.queue

class Maze:
    def __init__(self):
        with open(sys.argv[1]) as f:
            self.src = f.read()

        self.src = self.src.splitlines()

        self.height = len(self.src)
        self.width = max(len(line) for line in self.src)

        for i, line in enumerate(self.src):
            for j, element in enumerate(line):
                if element =="A":
                    self.start = (i, j)
                elif element =="B":
                    self.end = (i, j)

    def action(self, row, col):
        actions = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1)
        }

        return actions

    def solve(self):
        queue = Queue()
        self.explored = set()
        path = []
        list_node = []
        self.numPath = 0

        start_node = Node(0, self.start, None)
        queue.add(start_node)

        while queue.not_empty():
            curr_node = queue.pop()

            if curr_node.state == self.end:
                while curr_node:
                    path.append(curr_node.state)
                    curr_node = curr_node.parent
                path.reverse()
                return path, self.explored
            
            self.explored.add(curr_node.state)
            self.numPath += 1

            for action, (row, col) in self.action(*curr_node.state).items():
                if 0 <= row < self.height and 0 <= col < self.width and "#" not in self.src[row][col] and (row, col) not in self.explored:
                    cost = abs(row - self.end[0]) + abs(col - self.end[1])
                    next_node = Node(cost, (row, col), curr_node)
                    queue.add(next_node)

    def stored(self):
        maze = []

        for i, row in enumerate(self.src):
            rows = ""
            for j, col in enumerate(row):
                if col == "A":
                    rows += "A"
                elif col == "B":
                    rows += "B"
                elif col == "#":
                    rows += "█"
                elif col == " " and (i, j) in self.solve()[0]:
                    rows += "*"
                else:
                    rows += " "
            maze.append(rows)
        
        return maze
    
    def print(self):
        for line in self.stored():
            print(line)

    def output_image(self, maze, show_explored = None, show_result = None):
        cell_size = 50
        cell_border = 2
        
        img = Image.new(
            "RGBA",
            [self.width * cell_size, self.height * cell_size],
            "grey"
        )

        draw = ImageDraw.Draw(img)

        for i, row in enumerate(maze):
            for j, col in enumerate(row):
                x0 = j * cell_size + cell_border - 0.5
                y0 = i * cell_size + cell_border - 0.5
                x1 = (j + 1) * cell_size - cell_border
                y1 = (i + 1) * cell_size - cell_border

                if (i, j) == self.start:
                    #Yellow
                    fill = (250, 238, 2)
                elif (i, j) == self.end:
                    #Blue
                    fill = (66, 99, 245)
                elif col == "█":
                    #Black
                    fill = (5, 5, 5)
                elif (i, j) in self.solve()[0] and show_result:
                    #Green
                    fill = (19, 250, 2)
                elif (i, j) in self.solve()[1] and show_explored:
                    #Red
                    fill = (252, 3, 3)
                else:
                    #White
                    fill = (255, 255, 255)

                draw.rectangle(
                    [x0, y0, x1, y1],
                    fill
                )

        img.save("GBFS.png")
        # img.show()

m = Maze()
m.output_image(m.stored(), True, True)
print("Number of distance had gone:", m.numPath)