# "Stopwatch: The Game"
import simplegui

# define global variables
counter = 0
total_stop_count = 0
successful_stop_count = 0 
lap = 0
lapList = []

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(current_time):
    milli = current_time % 10
    current_time = int(current_time / 10)
    
    mins = int(current_time / 60)
    secs = current_time - mins * 60
    
    if (secs<10):
        secs = "0" + str(secs)
    
    return str(mins)+":"+str(secs)+"."+str(milli)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_counter():
    global timer
    timer.start()
    
def lap_counter():
    global lap,lapList
    if counter > lap:
        laptime = counter
        lapList.append(format(laptime - lap))
        lap = laptime
    
def stop_counter():
    global timer
    global total_stop_count
    global successful_stop_count
    
    if timer.is_running():
        total_stop_count +=1
        if(counter % 10 == 0):
            successful_stop_count += 1
        timer.stop()
        
def reset_counter():
    global counter, lapList, lap
    global total_stop_count
    global successful_stop_count

    stop_counter()
    counter = 0
    total_stop_count = 0
    successful_stop_count = 0
    lap = 0
    lapList = []
    

# define event handler for timer with 0.1 sec interval
def run_counter():
    global counter
    counter += 1
    

def key_handler(key):
    if key == simplegui.KEY_MAP["right"]:
        start_counter()
    elif key == simplegui.KEY_MAP["left"]:
        stop_counter()
    elif key == simplegui.KEY_MAP["space"]:
        lap_counter()
    elif key == simplegui.KEY_MAP["r"]:
        reset_counter() 
    else:
        print """Usage:
                 Right - Start
                 Left - Stop
                 Space - Lap
                 R - Reset"""
    

# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter),[35,160],100,"Red")
    canvas.draw_text("Score: "+str(successful_stop_count)+"/"+str(total_stop_count),[0,30],30,"Blue")
    canvas.draw_text("Stopwatch: The Game",[0,293],33,"Blue")
    canvas.draw_text("Start-[right], Stop-[left], Lap-[space], Reset-[r]",[4,260],16,"White")
    canvas.draw_line([300,0],[300,300],2,"Yellow")
    canvas.draw_text("Laps",[350,25],30,"Blue")

    i=1
    to_display = 0 if (len(lapList) - 12) < 0 else (len(lapList) - 12)
    
    for lapId in range(to_display,len(lapList)):
        canvas.draw_text("Lap "+str(lapId+1)+": "+lapList[lapId],[310,30+i*20],20,"White")
        i += 1
        
# create frame
myframe = simplegui.create_frame("Stopwatch: The Game",450,300)
myframe.set_draw_handler(draw)
myframe.set_keydown_handler(key_handler)

# register event handlers
myframe.add_button("Start",start_counter,100)
myframe.add_button("Lap",lap_counter,100)
myframe.add_button("Stop",stop_counter,100)
myframe.add_button("Reset",reset_counter,100)
timer = simplegui.create_timer(100, run_counter)

# start frame
myframe.start()

