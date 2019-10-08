# speed is proportional to framerate.
# It's 1.0 if we're achieving 60 fps
speed = 1.0
class Plane:
    def move(self):
        if self.falling:
            self.position.move(0, 8/speed)

class Game:
    def __init__(self):
        self.lastframe = time()
        
    def checkspeed(self):
	global speed
        now = time()
        elapsed = now - self.lastframe
	speed = 0.0166/elapsed
        self.lastframe = now
