import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = last_score = best_score =  0
lives = 3

time = 0.5
rocks_spawned = paused = mute = False

TOTAL_ROCKS = 10
started = False
rocks_spawn_counter = 1.0

ROCK_DIM = 64

# global time for animation
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
# debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
image_url="http://www.nyewall.com/images/2013/05/stellar-space-art-wallpapers-for-download-presidia-creative.jpg"
image_size=[1247,641]

nebula_info = ImageInfo([image_size[0]/2, image_size[1]/2], image_size)
nebula_image = simplegui.load_image(image_url)



# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 75)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

mute_info = ImageInfo([64, 64], [128, 128], 17)
mute_image = simplegui.load_image("https://cdn1.iconfinder.com/data/icons/sphericalcons/128/mute%202.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self): 
        self.angle += self.angle_vel
        if self.thrust == True:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * 0.2
            self.vel[1] += forward[1] * 0.2

        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
            
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT  
                    
            
    def keydown(self, key):
        angle_vel = 0.1
        if key == simplegui.KEY_MAP['left']:
            self.angle_vel = -angle_vel
        if key == simplegui.KEY_MAP['right']:
            self.angle_vel = angle_vel
        if key == simplegui.KEY_MAP['up']:
            self.thrust = True
            ship_thrust_sound.play()
            self.image_center = [130, 45]
        if key == simplegui.KEY_MAP['space']:
            if not paused:
                self.shoot()
            
    def keyup(self, key):
        global paused, started, mute

        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['left']:
            self.angle_vel = 0
        if key == simplegui.KEY_MAP['up']:
            self.thrust = False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()        
            self.image_center = ship_info.get_center()
        if key == simplegui.KEY_MAP['space']:
            if not paused:
                self.shoot()
        if key == simplegui.KEY_MAP['p']:
            paused = False if paused else True
            
        if key == simplegui.KEY_MAP['r']:
            started = False

        if key == simplegui.KEY_MAP['m']:
            mute = False if mute else True
            if mute:
                explosion_sound.set_volume(0)
                ship_thrust_sound.set_volume(0)
                missile_sound.set_volume(0)
                soundtrack.set_volume(0)
            else:
                explosion_sound.set_volume(1)
                ship_thrust_sound.set_volume(1)
                missile_sound.set_volume(0.5)
                soundtrack.set_volume(1)
                
    def shoot(self):
        missile_spawner(self)
 
def missile_spawner(ship):
    global missile_group
    forward = angle_to_vector(ship.angle)
    vel = [ship.vel[0] + forward[0] * 5, ship.vel[1] + forward[1] * 5]        
    pos = [ship.pos[0] + (forward[0] * ship.radius),ship.pos[1]+(forward[1] * ship.radius)]
    a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
    missile_group.append(a_missile)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        current_rock_index = (self.age % ROCK_DIM) // 1
        current_rock_center = [self.image_center[0] +  current_rock_index * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, current_rock_center, self.image_size, self.pos, [self.image_size[0] * 0.8,self.image_size[1] * 0.8]) 

        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT        
    
        self.age += 1
           
    def collide(self, other_object):
        self_pos = self.pos
        obj_pos = other_object.pos
        
        if (dist(self_pos,obj_pos) < (self.radius + other_object.radius)):
            return True

        return False
        
def draw(canvas):
    global time
    
    # animiate background
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [nebula_info.get_size()[0]*1.6,nebula_info.get_size()[1]*1.6], wtime / 1000.0)
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if mute:
        canvas.draw_image(mute_image, mute_info.get_center(), mute_info.get_size(), [50, HEIGHT - 50], [mute_info.get_size()[0] * 0.5,mute_info.get_size()[1] * 0.5])

    if not paused:
        # draw ship and sprites
        my_ship.draw(canvas)
        
        # draw splash screen if not started
        if not started:
            canvas.draw_image(splash_image, splash_info.get_center(), 
                              splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                              splash_info.get_size())
            reset_game()
        # update ship and sprites
        else:
            time += 1

            my_ship.update()
            
            process_sprite_group(rock_group,canvas,rocks_spawned)
            process_sprite_group(missile_group,canvas,True)
            process_sprite_group(explosion_group,canvas,True)
        
            group_collide(rock_group,my_ship)
            group_group_collide(rock_group, missile_group)
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                              splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                              splash_info.get_size())
        
    draw_lives_and_scores(canvas)

def draw_lives_and_scores(canvas):
    init_pos = [40, 80]
    ship_size = [my_ship.image_size[0]*0.5, my_ship.image_size[1]*0.5]
    for i in range(lives):
        pos = [init_pos[0] + 35 * i, init_pos[1]]
        canvas.draw_image(my_ship.image, my_ship.image_center, my_ship.image_size, pos, ship_size, 4.7)

    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score  ", [585, 50], 22, "White")
    canvas.draw_text("Last  ", [665, 50], 22, "Cyan")
    canvas.draw_text("Best", [730, 50], 22, "LightGreen")
    canvas.draw_text("||          ||", [647, 50], 22, "Red")
    canvas.draw_text(str(score), [585, 80], 22, "White")
    canvas.draw_text(str(last_score), [665, 80], 22, "Cyan")
    canvas.draw_text(str(best_score), [730, 80], 22, "LightGreen")
    
    
def reset_game():
    global missile_group, rock_group, explosion_group
    global score, lives, my_ship

    missile_group = []
    rock_group = []
    explosion_group = []

    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

    
def group_collide(sprite_set,space_object):
    global lives, score, started
    
    sprite_set_copy = list(sprite_set)
    if rocks_spawned:
        for i in range(len(sprite_set_copy)):
            if sprite_set_copy[i].collide(space_object):
                explosion_sound.rewind()
                explosion_sound.play()
                if type( space_object ) == Ship:
                   lives -= 1
                   explosive_object = Sprite(space_object.pos, space_object.vel, 0, space_object.angle_vel, explosion_image, explosion_info)
                   explosion_group.append(explosive_object)
                   #remove_nearby_space_objects(sprite_set, space_object)
                   if lives <= 0:
                        started = False
                else:
                    score += 10
                    space_object.age = space_object.lifespan
                try:
                    explosive_object = Sprite(sprite_set[i].pos, sprite_set[i].vel, 0, sprite_set[i].angle_vel, explosion_image, explosion_info)
                    explosion_group.append(explosive_object)
                    sprite_set.remove(sprite_set[i])
                except:
                    pass
 
def remove_nearby_space_objects(sprite_set, space_object):
    sprite_set_copy1 = list(sprite_set)
    for i in range(len(sprite_set_copy1)-1):
        if (dist(space_object.pos,sprite_set_copy1[i].pos) <  (space_object.radius + sprite_set_copy1[i].radius)):
            sprite_set.remove(sprite_set_copy1[i])
            explosive_object = Sprite(sprite_set_copy1[i].pos, space_object.vel, 0, space_object.angle_vel, explosion_image, explosion_info)
            explosion_group.append(explosive_object)

def group_group_collide(sprite_set1, sprite_set2):    
    for obj in sprite_set2:
        group_collide(sprite_set1,obj)
    
def process_sprite_group(sprite_set,canvas,ready_to_draw):    
    sprite_set_copy = list(sprite_set)

    if ready_to_draw:
        for i in range(len(sprite_set_copy)):
            if sprite_set_copy[i].age <= sprite_set_copy[i].lifespan :
                sprite_set_copy[i].draw(canvas)
                sprite_set_copy[i].update() 
            else:
                try:
                    sprite_set.remove(sprite_set[i])
                except:
                    pass


# timer handler that spawns a rock    
def rock_spawner():
    global rock_group,rocks_spawned, rocks_spawn_counter

    rocks_spawned = False

    rocks_spawn_counter += time / 1500
    
    if len(rock_group) < TOTAL_ROCKS and not paused:    
        rock_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        while (dist(my_ship.pos,rock_pos) < (2.5 * (my_ship.radius + asteroid_info.radius))):
            rock_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
            
        velocity = [(random.random() * .6 - .3) * rocks_spawn_counter, (random.random() * .6 - .3) * rocks_spawn_counter] 
        angel = random.random() * .2 - .1
        rock_group.append(Sprite(rock_pos, velocity, 0, angel, asteroid_image, asteroid_info))
                    
    rocks_spawned = True

    
def keydown_handler(key):
    my_ship.keydown(key)    

    
def keyup_handler(key):
    my_ship.keyup(key)        
    

def click(pos):
    global started, score, last_score,best_score, lives, time, rocks_spawn_counter, paused
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    paused = False
    if (not started) and inwidth and inheight:
        started = True
        last_score = score
        if score > best_score:
            best_score = score
        score = 0 
        lives = 3
        time = 0
        rocks_spawn_counter = 1.0
        soundtrack.rewind()
        soundtrack.play()

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)


rock_group = []
rock_spawner()

missile_group = []
explosion_group = []

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(click)
frame.add_label('~~~~CONTROLS~~~~')
frame.add_label('')

frame.add_label('P......Pause/Play')
frame.add_label('R.....Restart')
frame.add_label('M....Mute/UnMute')
frame.add_label('')
frame.add_label('Right.....Turn Clockwise')
frame.add_label('Left.......Turn AntiClockwise')
frame.add_label('Space....Fire Missile')

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
soundtrack.play()

