import os
import json
import vdf

#Util###################################################################
#Logging
dolog = False   #vdm.dolog = True
def log(message, *argv):
    message = "STVDM:\t" + message
    if dolog:
        print(message.format(*argv))
        
#Search a directory (dir) for files that have extension (ext) (Returns a list of file names)
def searchdir(dir, ext=".json", Prefix=False):
    dir = os.path.abspath(dir)
    log("Converting to absolute path: {}", dir)
    prefix = dir+os.sep if Prefix else ''
    files = [prefix+f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) if os.path.splitext(f)[1].lower() == ext] #This is called list comprehension. I'm looping over a directory and using if statements to determine what goes inside the list.
    files.sort() #Alphabetically, the earliest demos should be processed first
    return files

#clamp to always above 0
def clamp(n):
    if n >= 0:
        return n
    else:
        return 0

#Class Definitions (for vdm commands)###################################

class Skip:
    def __init__(self, stick, skipto):
        self.factory = "SkipAhead"
        self.name = "skip"
        self.start = stick
        self.skipto = skipto

    def __call__(self):
        return dict(factory = self.factory, name = self.name, starttick = self.start, skiptotick = self.skipto)

class PlayCommands:
    def __init__(self, stick):
        self.factory = "PlayCommands"
        self.start = stick

    def __call__(self):
        return dict(factory = self.factory, name = self.name, starttick = self.start, commands = self.command)

class StartRecord(PlayCommands):    #classname(OtherClass) indicates inheritance
    def __init__(self, stick):
        super().__init__(stick)
        self.name = "startrec"
        self.command = "startrecording"

class StopRecord(PlayCommands):
    def __init__(self, stick):
        super().__init__(stick)
        self.name = "stoprec"
        self.command = "stoprecording"

class NextDem(PlayCommands):    #Plays the next demo
    def __init__(self, stick, next_path):
        super().__init__(stick)
        self.name = "nextdem"
        #playdemo cmd searches from tf directory (Using the try/except statement in case we're not actually operating out of tf dir, i.e. testing)
        prune = ''      
        try:
            prune = next_path.split("tf"+os.sep)[1]
        except IndexError: #Not in tf dir
            print("WARNING: NOT IN TF DIRECTORY", next_path, next_path.split("tf"+os.sep))
            prune = next_path
        self.command = "playdemo {}".format(prune.replace(".json", ".dem")) # we pass this class a json file, so quickly switch it for the actual demo

class StopDemo(PlayCommands): #Ceases playing a demo - should be called after all vdms have played through.
    def __init__(self, stick):
        super().__init__(stick)
        self.name = "stopdem"
        self.command = "stopdemo"

#Filters for jsons and events###########################################

def AlwaysPass(x):
    return True

#(J) Func to use with filter() to produce a list of jsons, but only those with events. Why is this in a func instead of simply a continue statement? Because some vdms need to know what the next eventful demo is.
def HasEvents(file_name): 
    with open(file_name, "r") as f:
            events = json.loads(f.read())['events']
            if len(events) == 0:
                return False
            else:
                return True
                
#(E) Only process events that are named Bookmarks (auto-bookmarked events are named 'Killstreak')
def IsBookmark(event):
    if event['name'] == "Bookmark":
        return True
    else:
        return False
        
#(J) This filter is run on JSONs, to prevent "stoppage" in the vdm flow, where it directs you to the next demo but the next demo has nothing to record, so it simply plays through and has no commands to pass you to a new demo.
def PassesEventFilter(file):
    with open(file, "r") as f:          #Open JSON for reading
        events = json.loads(f.read())['events']
        events = list(filter(EventFilter, events))
        if len(events) > 0:
            return True
        else:
            return False
        
#Scripters may write their own filter then set vdm.EventFilter to it
EventFilter = AlwaysPass
JSONFilter = AlwaysPass
############################CLASSES
class Directory:
    def __init__(self, path, JSONFilter=AlwaysPass):
        self.i = -1
        self.path = path
        self.data = searchdir(path, Prefix=True)
        self.data = list(filter(JSONFilter, self.data))

        '''This explanation goes for __next__ in EventList, as well
        self.i starts as -1 so that I can iterate it to be the index before returning
        however, we can't iterate until we've checked this is a valid index so
        we check is self.i (index - 1) is equal to the length of data (minus 1)
        This could also be evaluated with `self.i+1 == len(self.data)`
        Actually I'm not sure why we can't iterate before evaling if its a valid index
        but I'm sure I had a reason... probably a bad one
        '''
    def __next__(self):
        if self.i == len(self.data)-1:
                raise StopIteration
        self.i += 1
        return self.i, self.data[self.i]

    def __iter__(self):
        self.i = -1
        return self

    def __getitem__(self, key):
        try:
                return self.data[key]
        except IndexError:
                return None

    def filter(self, func):
        if func.__name__ != "AlwaysPass":
            prior = len(self.data)
            self.data = list(filter(func, self.data))
            now = len(self.data)
            log("Pruning files for {}: {}, {} - {} = {}", self.path, func.__name__, prior, prior-now, now)
        
class EventList:
        def __init__(self, path, nf, Filter=None):
                self.path = path
                self.i = -1
                self.nextFile = nf
                self.stack = []
                self.vdm = vdf.VDF(self.path.replace(".json", ".vdm"))
                with open(self.path) as f:
                        self.events = json.loads(f.read())['events']
                        self.filter(Filter or EventFilter)
                        #self.events = list(filter(EventFilter, self.events))
                
        def __next__(self):
            if self.i == len(self.events)-1:
                    raise StopIteration
            self.i += 1
            return self.i, self.events[self.i]
        
        def __iter__(self):
                self.i = -1
                return self

        def filter(self, func):
            if func.__name__ != "AlwaysPass":
                prior = len(self.events)
                self.events = list(filter(func, self.events))
                now = len(self.events)
                log("Pruning events for {}: {}, {} - {} = {}", self.path, func.__name__, prior, prior - now, now)

        def write(self):
                for a in self.stack:
                        self.vdm.commit(a)
                if self.vdm.elements > 0:
                    self.vdm.write()
                    log("Writing vdm")
                else:
                    log("Not writing vdm, no applicable events")

#VDM processing#########################################################
                    #NOTE: eventIndex (eI) is relative to filtered events, not the events in the JSON)
def RecordEvent(e, eI, L, START_MARGIN=500, END_MARGIN=0, SKIP_MARGIN=1):
        tick = e['tick']
        if eI == 0: #This is the first event in the demo
                action = Skip(1, clamp(tick - START_MARGIN - SKIP_MARGIN))
                L.stack.append(action())
        if dolog:
            print(e)
            log("Adding recording action for this event @ ticks {}-{}", tick-START_MARGIN, tick+END_MARGIN)
        action = StartRecord(tick - START_MARGIN)
        L.stack.append(action())
        action = StopRecord(tick + END_MARGIN)
        L.stack.append(action())
        if eI+1 == len(L.events): #This is the last event in the demo (Not using elif, so I can insert recordings between)
                if L.nextFile == None:  #If this is the last file
                        action = StopDemo(tick + 1)
                        L.stack.append(action())
                else:
                        action = NextDem(tick + 1, L.nextFile)
                        L.stack.append(action())
        else: #This is NOT the last event in the demo. (I could have put this skip creation block in an if/else statement with "if first event" but it felt more logical to include it here)
                action = Skip(tick + END_MARGIN + 1, L.events[eI+1]['tick'] - START_MARGIN - SKIP_MARGIN) 
                L.stack.append(action())
