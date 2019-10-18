from tkinter import *
from tkinter import font
from math import sqrt
from random import *
from time import time

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
SPACING = 100
speed = 0.0

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    '''create a new object from this one.  we use this when we want to
       create a modified copy of a point without modifying the original object'''
    def copy(self):
        return Point(self.X, self.Y)

    ''' vector addition of points '''
    def add(self, other):
        self.X = self.X + other.X
        self.Y = self.Y + other.Y

    def move(self, dx, dy):
        self.X = self.X + dx
        self.Y = self.Y + dy

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y) 

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.sqrt(dx**2 + dy**2)

''' update_position takes a list of x and y coordinates and a Point.
    It creates a new list of x and y coordintes by adding the Point to all
    the coordintes from the original list '''    

def update_position(position_list, position, scale):
    newlist = []
    is_x = True;
    for val in position_list:
        if is_x:
            newlist.append(int(scale*(val + position.getX())))
        else:
            newlist.append(int(scale*(val + position.getY())))
        is_x = not is_x
    return newlist

''' The BuildingView class has the task of displaying one building '''
class BuildingView():
    def __init__(self, canvas, building, scale):
        self.canvas = canvas
        self.building = building
        self.height = scale*building.get_height()
        xpos = scale*building.get_xpos()
        width = scale*building.get_width()
        canvas_height = scale*CANVAS_HEIGHT
        self.main_rect = canvas.create_rectangle(xpos, canvas_height, xpos + width, canvas_height - self.height, fill="brown")

    def redraw(self, scale):
        if self.building.get_height() != self.height:
            #the building has changed; need to redraw it
            self.canvas.delete(self.main_rect)
            self.height = scale*self.building.get_height()
            xpos = scale*self.building.get_xpos()
            width = scale*self.building.get_width()
            canvas_height = scale*CANVAS_HEIGHT
            self.main_rect = self.canvas.create_rectangle(xpos, canvas_height, xpos + width, canvas_height-self.height, fill="brown")
            
    def cleanup(self):
        self.canvas.delete(self.main_rect)

''' The Building class holds all the state associated with the model of one building '''
class Building():
    def __init__(self, building_num, height, width):
        self.height = height
        self.x = building_num*SPACING
        self.width = width

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_xpos(self):
        return self.x

    ''' is_inside tests if a point is inside the building '''
    def is_inside(self, point):
        if point.X < self.x or point.X > self.x + self.width or point.Y < CANVAS_HEIGHT-self.height:
            return False
        return True

    ''' shrink the building when a bomb drops on it '''
    def shrink(self):
        self.height = self.height - 50

''' BombView is responsible for displaying the bomb '''
class BombView():
    def __init__(self, canvas, bomb_model, scale):
        self.bomb_model = bomb_model
        self.canvas = canvas
        self.points = [0,0, 10,0, 5,5, 10,10, 10,20, 5,22, 0,20, 0,10, 5,5]
        self.draw(scale)

    ''' draw the bomb at its current position '''
    def draw(self, scale):
        current_points = update_position(self.points, self.bomb_model.get_position(), scale)
        self.polygon = self.canvas.create_polygon(*current_points, fill="black")
        self.drawn = True

    ''' erase the old bomb, and redraw it '''
    def redraw(self, scale):
        if self.drawn:
            self.canvas.delete(self.polygon)
        if self.bomb_model.is_drawable():
            self.draw(scale)

''' The Bomb class maintains the model of the bomb.  There's                           
    only one bomb.  Once it explodes it can be reused again '''
class Bomb():
    def __init__(self):
        self.falling = False
        self.position = Point(0,0)

    def get_position(self):
        return self.position

    def is_drawable(self):
        return self.falling

    def move(self):
        if self.falling:
            self.position.move(0, 8*speed)

    ''' drop the bomb from the plane '''
    def drop(self, point):
        if self.falling:
            # don't drop again while bomb is still falling
            return
        self.falling = True
        # copy the plane's position, rather that taking a reference to it
        # (if we instead do self.position = point, we'll end up changing the plane's position as the bomb falls)
        self.position = point.copy()

    def explode(self):
        self.falling = False

''' PlaneView class is responsibe for displaying the plane '''
class PlaneView():
    def __init__(self, canvas, plane_model, scale):
        self.canvas = canvas
        self.plane_model = plane_model
        self.body_points = [0,28, 20,16, 120,16, 94,32, 12,32]
        self.wing1_points = [40,28, 76,28, 94,48, 80,48]
        self.wing2_points = [52,16, 78,8, 94,8, 81,16]
        self.tail_points = [90,16, 110,0, 124,0, 116,16]
        self.draw(scale)

    def draw(self, scale):
        pos = self.plane_model.get_position()
        current_body_points = update_position(self.body_points, pos, scale)
        current_wing1_points = update_position(self.wing1_points, pos, scale)
        current_wing2_points = update_position(self.wing2_points, pos, scale)
        current_tail_points = update_position(self.tail_points, pos, scale)
        self.body = self.canvas.create_polygon(*current_body_points, fill="red")
        self.wing1 = self.canvas.create_polygon(*current_wing1_points, fill="grey")
        self.wing2 = self.canvas.create_polygon(*current_wing2_points, fill="grey")
        self.tail = self.canvas.create_polygon(*current_tail_points, fill="grey")

    def redraw(self, scale):
        self.canvas.delete(self.body)
        self.canvas.delete(self.wing1)
        self.canvas.delete(self.wing2)
        self.canvas.delete(self.tail)
        self.draw(scale)

#the plane model, independent of its view
class Plane():
    def __init__(self, x, y):
        self.start_position = Point(x, y)
        self.position = Point(x, y)
        self.width = 124 # plane width  

    def get_position(self):
        return self.position

    ''' reset the plane to its starting position at the start of a new level '''
    def reset_position(self):
        self.position = self.start_position.copy()

    ''' move the plane however much it moves during one frame '''
    def move(self):
        self.position.move(-4 * speed, 0)
        if self.position.getX() < -self.width:
            self.position.move(CANVAS_WIDTH + self.width, 40)
            #ensure we don't go off the bottom of the screen                                    
            if self.position.getY() > CANVAS_HEIGHT - 32:
                self.position.Y = CANVAS_HEIGHT - 32
            #we get 10 points each row the plane moves down                                     
            return 10
        else:
            return 0

''' The View class handles everything to do with displaying the user interface to the user'''
class View(Frame):
    def __init__(self, root, controller, scale):
        self.controller = controller
        root.wm_title("Bomber")
        self.windowsystem = root.call('tk', 'windowingsystem')
        self.frame = root
        self.scale = scale
        self.canvas = Canvas(self.frame, width=int(CANVAS_WIDTH*scale), height=int(CANVAS_HEIGHT*scale), bg="white")
        self.canvas.pack(side = LEFT, fill=BOTH, expand=TRUE)
        self.init_fonts()
        self.init_score()
        self.building_views = []
        self.messages_displayed = False

    def init_fonts(self):
        self.bigfont = font.nametofont("TkDefaultFont")
        self.bigfont.configure(size=int(48*self.scale))
        self.scorefont = font.nametofont("TkDefaultFont")
        self.scorefont.configure(size=int(20*self.scale))

    def init_score(self):
        self.score_text = self.canvas.create_text(int(5*self.scale), int(5*self.scale), anchor="nw")
        self.canvas.itemconfig(self.score_text, text="Score:", font=self.scorefont)

    def register_plane(self, plane_model):
        self.plane_view = PlaneView(self.canvas, plane_model, self.scale)

    def register_bomb(self, bomb_model):
        self.bomb_view = BombView(self.canvas, bomb_model, self.scale)

    def register_building(self, building_model):
        building_view = BuildingView(self.canvas, building_model, self.scale)
        self.building_views.append(building_view)

    def unregister_buildings(self):
        for building_view in self.building_views:
            building_view.cleanup()
        self.building_views.clear()

    def display_score(self):
        self.canvas.itemconfig(self.score_text, text="Level: " + str(self.controller.get_level())
                               + "  Score: " + str(self.controller.get_score()), font=self.scorefont)

    def game_over(self):
        self.text = self.canvas.create_text(self.scale*CANVAS_WIDTH/2, self.scale*CANVAS_HEIGHT/2, anchor="c")
        self.canvas.itemconfig(self.text, text="GAME OVER!", font=self.bigfont)
        self.text2 = self.canvas.create_text(self.scale*CANVAS_WIDTH/2, self.scale*CANVAS_HEIGHT/2 + 100, anchor="c")
        self.canvas.itemconfig(self.text2, text="Press r to play again.", font=self.scorefont)
        self.messages_displayed = True

    def plane_landed(self):
        self.text = self.canvas.create_text(self.scale*CANVAS_WIDTH/2, self.scale*CANVAS_HEIGHT/2, anchor="c")
        self.canvas.itemconfig(self.text, text="SUCCESS!", font=self.bigfont)
        self.text2 = self.canvas.create_text(self.scale*CANVAS_WIDTH/2, self.scale*CANVAS_HEIGHT/2 + 100, anchor="c")
        self.canvas.itemconfig(self.text2, text="Press n for next level.", font=self.scorefont)
        self.messages_displayed = True

    def clear_messages(self):
        if self.messages_displayed:
            self.canvas.delete(self.text)
            self.canvas.delete(self.text2)

    def update(self):
        self.plane_view.redraw(self.scale)
        self.bomb_view.redraw(self.scale)
        for building_view in self.building_views:
            building_view.redraw(self.scale)
        self.display_score()

''' The Model class holds the game model, and manages the interactions
between the elements of the game, namely the Plane, Bomb and
Buildings.  It doesn't display anything. '''
class Model(Frame):
    def __init__(self, controller):
        self.controller = controller
        self.init_score()
        self.rand = Random()

        #create game objects
        self.plane = Plane(CANVAS_WIDTH - 100, 0)
        controller.register_plane(self.plane)
        self.bomb = Bomb()
        controller.register_bomb(self.bomb)
        self.buildings = []
        self.building_width = SPACING * 0.8
        self.create_buildings()
        self.game_running = True
        self.won = False

    def init_score(self):
        self.score = 0
        self.level = 1
        self.controller.update_score(0)
        self.controller.update_level(0)

    def create_buildings(self):
        #remove any old buildings
        self.controller.unregister_buildings()
        self.buildings.clear()

        #create the new ones
        for building_num in range(0, 1000//SPACING):
            height = self.rand.randint(10,500) #random number between 10 and 500
            building = Building(building_num, height, self.building_width)
            self.buildings.append(building);
            self.controller.register_building(building)

    def drop_bomb(self):
        self.bomb.drop(self.plane.position)

    def check_bomb(self):
        if not self.bomb.falling:
            return
        for building in self.buildings:
            if building.is_inside(self.bomb.position):
                self.bomb.explode()
                building.shrink()
        if self.bomb.position.getY() > CANVAS_HEIGHT:
            self.bomb.explode()

    def check_plane(self):
        # we'll check if the plane nose hits a building, or if the
        # base of the fuselage hits.  Won't worry if the wing hits though.
        plane_nose = self.plane.position.copy()
        plane_nose.move(0, 28)
        plane_body_bottom = self.plane.position.copy()
        plane_body_bottom.move(12, 32)
        for building in self.buildings:
            if building.is_inside(plane_nose) or building.is_inside(plane_body_bottom) :
                self.game_over()
        if plane_body_bottom.getY() == CANVAS_HEIGHT and plane_body_bottom.getX() < 20:
            self.plane_landed()

    def game_over(self):
        self.game_running = False
        self.won = False
        self.controller.game_over()

    def plane_landed(self):
        self.game_running = False
        self.won = True
        self.score = self.score + 1000
        self.controller.update_score(self.score)
        self.controller.plane_landed()

    def restart(self):
        self.level = 1
        self.controller.update_level(self.level)
        self.score = 0
        self.controller.update_score(self.score)
        self.plane.reset_position()
        self.building_width = SPACING * 0.8
        self.create_buildings()
        self.won = False
        self.game_running = True

    def next_level(self):
        #don't move to next level unless we've actually won!
        if self.won == False:
            return
        self.level = self.level + 1
        self.controller.update_level(self.level)
        self.plane.reset_position()
        self.building_width = self.building_width * 0.9
        self.create_buildings()
        self.won = False
        self.game_running = True
        
    def update(self):
        if self.game_running:
            self.score = self.score + self.plane.move()
            self.controller.update_score(self.score)
            self.check_plane()
            self.bomb.move()
            self.check_bomb()

''' The Controller class handles input from the user, registering and
updating new views, and also serves to route updates from the Model to
the Views '''
class Controller():
    def __init__(self):
        self.root = Tk();
        self.windowsystem = self.root.call('tk', 'windowingsystem')
        self.views = []
        self.root.bind_all('<Key>', self.key)
        self.running = True
        self.score = -1
        self.level = -1
        self.buildings = []
        self.model = Model(self);
        self.add_view(View(self.root, self, 0.7))

        #do one round of display before we seed the speed measurement,
        #or we get a bad first value because it takes time to draw the
        #window the first time
        self.model.update()
        for view in self.views:
            view.update()
        self.root.update()

        self.lastframe = time()
        self.framecount = 0

    # called by the Model to inform everyone that a new building exists 
    def register_building(self, building):
        self.buildings.append(building)
        for view in self.views:
            view.register_building(building)

    # called by the Model to inform everyone to erase all the old buildings
    def unregister_buildings(self):
        self.buildings.clear()
        for view in self.views:
            view.unregister_buildings()

    # called by the Model to inform everyone that a plane exists
    def register_plane(self, plane):
        self.plane = plane
        for view in self.views:
            view.register_plane(plane)

    # called by the Model to inform everyone that a bomb exists
    def register_bomb(self, bomb):
        self.bomb = bomb
        for view in self.views:
            view.register_bomb(bomb)

    # called when a new view needs to be initialized
    def add_view(self, view):
        self.views.append(view)
        view.register_plane(self.plane)
        view.register_bomb(self.bomb)
        for building in self.buildings:
            view.register_building(building)

    #some helper functions to hide the controller implementation from
    #the model and the controller
    def update_score(self, score):
        self.score = score

    def get_score(self):
        return self.score
        
    def update_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    def game_over(self):
        for view in self.views:
            view.game_over()
        
    def plane_landed(self):
        for view in self.views:
            view.plane_landed()
        
    def key(self, event):
        if event.char == ' ':
            self.model.drop_bomb()
        elif event.char == 'q':
            self.running = False
        elif event.char == 'n':
            for view in self.views:
                view.clear_messages()
            self.model.next_level()
        elif event.char == 'r':
            for view in self.views:
                view.clear_messages()
            self.model.restart()
        elif event.char == 'v':
            self.add_view(View(self.root, self, 0.35))

    ''' adjust game speed so it's more or less the same on different machines '''
    def checkspeed(self):
        global speed
        self.framecount = self.framecount + 1
        # only check every ten frames                                                           
        if self.framecount == 10:
            now = time()
            elapsed = now - self.lastframe
            # speed will be 1.0 if we're achieving 60 fps                                       
            if speed == 0:
                #initial speed value                                                            
		# At 60fps, 10 frames take 1/6 of a second.                                     
                speed = 6 * elapsed
            else:
                # use an EWMA to damp speed changes and avoid excessive jitter                  
                speed = speed * 0.9 + 0.1 * 6 * elapsed
            self.lastframe = now
            self.framecount = 0
            
    def run(self):
        while self.running:
            self.model.update()
            for view in self.views:
                view.update()
            self.root.update()
            self.checkspeed()
        self.root.destroy()

game = Controller();
game.run()
