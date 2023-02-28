import turtle


TITLE = "Home Simulator"

FONT = ("Arial", 14, "bold")

room1 = None
room2 = None
room3 = None

door1_closed = False
door2_closed = False
door3_closed = False

Window_Width  = 0           # window size, set by 'make_window'
Window_Height = 0
Window_LL = 0               # lower left corner of the window

Room_Width = 0              # room size, set by 'make_window'
Room_Height = 0


# Calls for window creation
# All collected here, so window creation can be controlled explicitly

def make_window():
    global Window_Width, Window_Height
    global Room_Width, Room_Height

    turtle.title(TITLE)
    Window_Width = turtle.window_width()    # window size
    Window_Height = turtle.window_height()
    Room_Width = Window_Width / 2
    Room_Height = Window_Height / 2
    turtle.setworldcoordinates(Window_LL, Window_LL, Window_Width, Window_Height)



# ---------- Index classes ----------
#
#   class SimMap:
#       __init__()
#       draw_map()

#   class Room:
#       __init__(room_name, llx, lly, w, h)
#       draw_room()
#           - draw_doors(door_name)
#               - draw_markers()
#       draw_furniture()

#   class Robot:
#       __init__()
#       at_home()
#       move_to(p_name)
#       perceive()
#       open_door(door_name)
#       change_door_status(door_name)

#   class Label:
#       __init__(self, x, y, quadrant, edge, text)

#   class Square:
#       __init__()
#       draw_square(self, x, y, w, h)
#
# ----------  end index ----------


# ----------------------------------------
# Draws the perimeter of the map in the window
# and set the background color: light gray
# ----------------------------------------

class SimMap:
    def __init__(self):
        global room1
        global room2
        global room3

        turtle.bgcolor("light gray")
        self.draw_map()

        room1 = Room("room1", Window_LL, Room_Height, Room_Width, Room_Height)
        room2 = Room("room2", Window_LL, Window_LL, Room_Width, Room_Height)
        room3 = Room("room3", Room_Width, Window_LL, Room_Width, 2 * Room_Height)

        robot = Robot()

        if door1_closed:
            robot.open_door("close", "door1")
        else:
            robot.open_door("open", "door1")
        if door2_closed:
            robot.open_door("close", "door2")
        else:
            robot.open_door("open", "door2")
        if door3_closed:
            robot.open_door("close", "door3")
        else:
            robot.open_door("open", "door3")

    def draw_map(self):
        perimeter = Square("blue")
        perimeter.draw_square(Window_LL, Window_LL, Window_Width, Window_Height)


# ----------------------------------------
# Draws the walls (perimeter),
# puts room labels (at distance <edge> from walls),
# draws the doors between rooms (door1,door2,door3),
# assign and draws the markers (p1, ..., p9),
# puts the furniture in the rooms (stove,bed,table)
# ----------------------------------------
class Room:

    def __init__(self, room_name, llx, lly, w, h):
    # calculates the centers of the rooms
    # calls: draw_room/draw_furniture

        self.room_name = room_name      # name of the room
        self.llx = llx                  # lower left corner for the door drawing
        self.lly = lly
        self.w = w                      # w = width of the room
        self.h = h                      # h = height (the length in (x,y))

        self.cx = llx + w/2             # (cx,cy) center of the room (p1, p5, p9)
        self.cy = lly + h/2

        self.draw_room()
        self.draw_furniture()

    def draw_room(self):
    # draws the wall (perimeter) for each room and puts a label on it

        wall = Square("blue")
        wall.draw_square(self.llx, self.lly, self.w, self.h)

        distance = self.w/8         # distance from the edges of the room
        Label(self.llx, self.lly + self.h, "SE", distance, self.room_name)

        if self.room_name == "room1":
            self.draw_doors_and_markers_near("door3")   # draws p3
            self.draw_doors_and_markers_near("door1")   # draws p2
        elif self.room_name == "room2":
            self.draw_doors_and_markers_near("door3")   # draws p4
            self.draw_doors_and_markers_near("door2")   # draws p6
        elif self.room_name == "room3":
            self.draw_doors_and_markers_near("door2")   # draws p7
            self.draw_doors_and_markers_near("door1")   # draws p8

    def draw_doors_and_markers_near(self, door_name):
    # draws a door between two rooms
        self.door_name = door_name
        door_amplitude = 60             # size of the door along x
        door_thickness = 20             # size of the door along y
        edge = 10                       # distance for markers labelling

        door = Square("blue")

        # drawing of the doors (door1, door2, door3) according to the room
        # door3: room1 <-> room2
        if self.door_name == "door3":                               # door3: side of room1
            if self.room_name == "room1":
                self.door3_x = self.cx                              # position of the door3
                self.door3_y = self.cy - Room_Height / 2
                self.ll3x_door = self.door3_x - door_amplitude/2    # lower_left corner of door3
                self.ll3y_door = self.door3_y - door_thickness/2
                door.draw_square(self.ll3x_door, self.ll3y_door, door_amplitude, door_thickness)
                self.draw_markers()
            elif self.room_name == "room2":                         # door3: the same by the other side in room2
                self.door3_x = self.cx
                self.door3_y = self.cy + Room_Height / 2
                self.ll3x_d = self.door3_x - door_amplitude/2
                self.ll3y_d = self.door3_y - door_thickness/2
                door.draw_square(self.ll3x_d, self.ll3y_d, door_amplitude, door_thickness)
                self.draw_markers()
        # door2: room2 <-> room3
        elif self.door_name == "door2":                             # door2: side of room2
            if self.room_name == "room2":
                self.door2_x = self.cx + Room_Width / 2                        # position of door2
                self.door2_y = self.cy
                self.ll2x_door = self.door2_x - door_thickness/2    # lower_left corner of door2
                self.ll2y_door = self.door2_y - door_amplitude/2
                door.draw_square(self.ll2x_door, self.ll2y_door, door_thickness, door_amplitude)
                self.draw_markers()
            elif self.room_name == "room3":                         # door2: the same by the other side
                self.door2_x = self.cx - Room_Width / 2
                self.door2_y = self.cy - Room_Height / 2
                self.ll2x_door = self.door2_x - door_thickness/2
                self.ll2y_door = self.door2_y - door_amplitude/2
                door.draw_square(self.ll2x_door, self.ll2y_door, door_thickness, door_amplitude)
                self.draw_markers()
        # door1: room1 <-> room3
        elif self.door_name == "door1":                             # door1: side of room1
            if self.room_name == "room1":
                self.door1_x = self.cx + Room_Width / 2                        # position of door1
                self.door1_y = self.cy
                self.ll1x_door = self.door1_x - door_thickness/2    # lower_left corner of door1
                self.ll1y_door = self.door1_y - door_amplitude/2
                door.draw_square(self.ll1x_door, self.ll1y_door, door_thickness, door_amplitude)
                self.draw_markers()
            elif self.room_name == "room3":                         # door1: the same by the other side
                self.door1_x = self.cx - Room_Width / 2
                self.door1_y = self.cy + Room_Height / 2
                self.ll1x_door = self.door1_x - door_thickness/2
                self.ll1y_door = self.door1_y - door_amplitude/2
                door.draw_square(self.ll1x_door, self.ll1y_door, door_thickness, door_amplitude)
                self.draw_markers()
        else:
            return

    def draw_markers(self):
    # places and draws the markers in the room
        door_step = 30              # distance of each markers from the door
        edge = 10                   # distance for markers labelling

        turtle.pen(pencolor="blue", pensize=2, speed=0)
        turtle.shape("circle")      # markers shape

        if self.room_name == "room1":
        # p1: center (room1)
            turtle.goto(self.cx, self.cy)
            turtle.color("green")
            turtle.stamp()
            Label(self.cx, self.cy, "NW", edge, "p1")

            if self.door_name == "door3":
            # p3 -> door 3 (room1)
                self.p3_x = self.door3_x
                self.p3_y = self.door3_y + door_step
                turtle.goto(self.p3_x, self.p3_y)
                turtle.color("green")
                turtle.stamp()
                Label(self.p3_x, self.p3_y, "NW", edge,"p3")

            elif self.door_name == "door1":
            # p2 -> door1 (room1)
                self.p2_x = self.door1_x - door_step
                self.p2_y = self.door1_y
                turtle.goto(self.p2_x, self.p2_y)
                turtle.color("green")
                turtle.stamp()
                Label(self.p2_x, self.p2_y, "NW", edge,"p2")

        elif self.room_name == "room2":
        # p5: center (room2)
            turtle.goto(self.cx, self.cy)
            turtle.color("green")
            turtle.stamp()
            Label(self.cx, self.cy, "SW", edge, "p5")

            if self.door_name == "door3":
            # p4 -> door3 (room2)
                self.p4_x = self.door3_x
                self.p4_y = self.door3_y - door_step
                turtle.goto(self.p4_x, self.p4_y)
                turtle.color("green")
                turtle.stamp()
                Label(self.p4_x, self.p4_y, "SW", edge,"p4")

            elif self.door_name == "door2":
            # p6 -> door2 (room2)
                self.p6_x = self.door2_x - door_step
                self.p6_y = self.door2_y
                turtle.goto(self.p6_x, self.p6_y)
                turtle.color("green")
                turtle.stamp()
                Label(self.p6_x, self.p6_y, "SW", edge,"p6")

        elif self.room_name == "room3":
            # p9: center (room3)
            turtle.goto(self.cx, self.cy)
            turtle.color("green")
            turtle.stamp()
            Label(self.cx, self.cy, "NE", edge, "p9")

            if self.door_name == "door2":
            # p7 -> door2 (room3)
                self.p7_x = self.door2_x + door_step
                self.p7_y = self.door2_y
                turtle.goto(self.p7_x, self.p7_y)
                turtle.color("green")
                turtle.stamp()
                Label(self.p7_x, self.p7_y, "NE", edge,"p7")

            elif self.door_name == "door1":
            # p8 -> door1 (room3)
                self.p8_x = self.door1_x + door_step
                self.p8_y = self.door1_y
                turtle.goto(self.p8_x, self.p8_y)
                turtle.color("green")
                turtle.stamp()
                Label(self.p8_x, self.p8_y, "NE", edge,"p8")
        else:
            return

    def draw_furniture(self):
    # draws and labels the furniture in each room
        f_name = ""
        f_width = 0
        f_height = 0

        if self.room_name == "room1":           # room1 -> the bed
            f_name = "Bed"
            f_width = 70
            f_height = 150
            self.f_x = self.cx - Room_Width / 2
            self.f_y = self.cy - Room_Height / 2
        elif self.room_name == "room2":         # room2 -> the stove
            f_name = "Stove"
            f_width = 150
            f_height = 60
            self.f_x = Window_LL + Room_Width / 4
            self.f_y = Window_LL
        elif self.room_name == "room3":         # room3 -> the table
            f_name = "Table"
            f_width = 80
            f_height = 120
            self.f_x = self.cx + Room_Width / 6
            self.f_y = Room_Height / 6

        furniture = Square("blue")                                  # drawing
        furniture.draw_square(self.f_x, self.f_y, f_width, f_height)
        Label(self.f_x + 40, self.f_y + 30, "SW", 0, f_name)        # labelling


# ----------------------------------------
# Places the robot at home (on marker p1)
# Moves the robot among the markers (and draws the path)
# Returns the kind of furniture in each room (bed, stove, table)
# ----------------------------------------
class Robot:
    def __init__(self):
    # robot starts in <p1>
        self.laststamp = 0      # ID of last stamp left, to be reset at next move
        self.at_home()
        # self.drawbox('p8')

    def at_home(self):
    # set speed, shape, color and size of the robot and places it in <p1>
        turtle.penup()
        turtle.pen(pencolor="blue", pensize=4, speed=1)
        turtle.turtlesize(1)
        turtle.color("blue")
        turtle.shape("circle")

        home_pos = (room1.cx, room1.cy)     # starts in <p1> center of room1
        turtle.goto(home_pos)
        turtle.pendown()
        turtle.stamp()                      # the robot leaves the first trace
        turtle.penup()

    def open_door(self, action, door_name):
        # action can be "open" or "close"
        if door_name is "door3":
            self.change_door_status(action, room1.ll3x_door, room1.ll3y_door, "NS")
        if door_name is "door2":
            self.change_door_status(action, room2.ll2x_door, room2.ll2y_door, "WE")
        if door_name is "door1":
            self.change_door_status(action, room3.ll1x_door, room3.ll1y_door, "WE")
        else:
            return

    def change_door_status(self, action, x, y, orient):
    # open or close the door according its orientation
        self.amplitude = 60
        self.thickness = self.amplitude/3
        edge = 2

        old_x, old_y = turtle.pos()             # the status before action
        old_color = turtle.pencolor()
        old_fill = turtle.fillcolor()
        old_size = turtle.pensize()
        old_speed = turtle.speed()

        if orient == "NS":
            self.amplitude = self.thickness
            self.thickness = self.amplitude * 3

        new_door = Square("")

        turtle.goto(x, y)

        if action == "open":                    # open -> empty drawing
            turtle.color("gray", "light gray")
        else:                                   # close -> fill the door
            turtle.color("blue", "blue")

        turtle.pendown()                        # re-draw the empty/full door
        turtle.pensize(1)
        turtle.begin_fill()
        new_door.draw_square(x, y, self.thickness, self.amplitude)
        turtle.end_fill()
        turtle.penup()

        turtle.goto(old_x, old_y)           # back to the old status
        turtle.pencolor(old_color)
        turtle.fillcolor(old_fill)
        turtle.pensize(old_size)
        turtle.speed(old_speed)

    def move_to(self, pname):
    # moves leaving a trace and stores the room
        global room1
        global room2
        global room3
        self.arrival_room = ""              # latest room of the path

        turtle.pendown()

        if pname == "p1":
            room_name = "room1"
            turtle.goto(room1.cx, room1.cy)
        elif pname == "p2":
            room_name = "room1"
            turtle.goto(room1.p2_x, room1.p2_y)
        elif pname == "p3":
            room_name = "room1"
            turtle.goto(room1.p3_x, room1.p3_y)
        elif pname == "p4":
            room_name = "room2"
            turtle.goto(room2.p4_x, room2.p4_y)
        elif pname == "p5":
            room_name = "room2"
            turtle.goto(room2.cx, room2.cy)
        elif pname == "p6":
            room_name = "room2"
            turtle.goto(room2.p6_x, room2.p6_y)
        elif pname == "p7":
            room_name = "room3"
            turtle.goto(room3.p7_x, room3.p7_y)
        elif pname == "p8":
            room_name = "room3"
            turtle.goto(room3.p8_x, room3.p8_y)
        elif pname == "p9":
            room_name = "room3"
            turtle.goto(room3.cx, room3.cy)
        else:
            return
        if self.laststamp != 0:
            turtle.clearstamp(self.laststamp)
        self.laststamp = turtle.stamp()
        self.arrival_room = room_name

    def perceive(self):
    # prints and returns the furniture when in the arrival_room
        if self.arrival_room == "room1":
            print("I am in room1... I see the BED")
            return ["Bed"]

        elif self.arrival_room == "room2":
            print("I am in room2... I see the STOVE")
            return ["Stove"]

        elif self.arrival_room == "room3":
            print("I am in room3... I see the TABLE")
            return ["Table"]

        else:
            return[]

    def drawbox(self, p):
    # draws a box at point p
        oldshape = turtle.shape()
        oldwid, oldlen, oldout = turtle.shapesize()
        oldfill = turtle.fillcolor()
        oldpos = turtle.pos()
        turtle.shape("square")
        turtle.shapesize(5, 5, 1)
        turtle.fillcolor("white")
        turtle.setpos(room3.p8_x, room3.p8_y)
        turtle.stamp()
        turtle.setpos(oldpos)
        turtle.shape(oldshape)
        turtle.shapesize(oldwid, oldlen, oldout)
        turtle.fillcolor(oldfill)

# ----------------------------------------
# Labelling markers (p1..p9)
# Write the text of label in p(x,y) aligning it
# according to the quadrant: NW-NE-SW-SE
# ----------------------------------------
class Label:
    def __init__(self, x, y, quadrant, edge, text):
        self.text = text
        if quadrant == "NW":
            self.x = x - edge
            self.y = y + edge
        elif quadrant == "NE":
            self.x = x + edge
            self.y = y + edge
        elif quadrant == "SW":
            self.x = x - edge *2
            self.y = y - edge *3
        elif quadrant == "SE":
            self.x = x + edge
            self.y = y - edge

        turtle.goto(self.x, self.y)
        turtle.write(self.text, move=False, align="center", font=FONT)


# ----------------------------------------
# Draws the squares used for:
# map, rooms, doors, furniture
# with: width = w and height = h
# ----------------------------------------
class Square:
    def __init__(self, color):
        turtle.pencolor(color)
        turtle.pensize(8)
        turtle.speed(0)
        turtle.turtlesize(1)

    def draw_square(self, x, y, w, h):
        turtle.penup()
        turtle.goto(x, y)

        turtle.pendown()
        turtle.hideturtle()
        for i in range(1,3):
            turtle.forward(w)
            turtle.left(90)
            turtle.forward(h)
            turtle.left(90)
        turtle.penup()


class Box(turtle.Turtle):
    def __init__(self):
        return


# ---------- Driver code ----------

# ---------- Driver code ----------
# Standalone test:
# Create a map and a robot
# Make robot move to a sequence of points
# and perceive <furniture> at the end

if __name__ == "__main__":

    make_window()
    map1 = SimMap()
    robot = Robot()

    robot.move_to("p3")
    robot.open_door("open", "door3")
    robot.move_to("p2")
    robot.open_door("open", "door1")
    robot.move_to("p8")
    robot.move_to("p9")
    robot.move_to("p7")
    robot.open_door("open", "door2")
    robot.move_to("p6")
    robot.open_door("close", "door2")
    robot.move_to("p4")
    robot.open_door("close", "door3")
    robot.move_to("p5")

    robot.perceive()


# ----------------------------------------
# Exit the program by
# clicking anywhere in the window
# ----------------------------------------

# turtle.exitonclick()

# ----------------------------------------
# Exit the program
# by clicking on the window close button
# ----------------------------------------

# turtle.done()
