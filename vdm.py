import os
import json
import vdf

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

class Record(PlayCommands):	#classname(OtherClass) indicates inheritance
	def __init__(self, stick):
		super().__init__(stick)
		self.name = "startrec"
		self.command = "startrecording"

class StopRecord(PlayCommands):
	def __init__(self, stick):
		super().__init__(stick)
		self.name = "stoprec"
		self.command = "stoprecording"

class NextDem(PlayCommands):	#Plays the next demo
	def __init__(self, stick, next_path):
		super().__init__(stick)
		self.name = "nextdem"
	 	#playdemo cmd searches from tf directory (Using the try/except statement in case we're not actually operating out of tf dir, i.e. testing)
		prune = ''		
		try:
			prune = next_path.split("tf"+os.sep)[1]
		except IndexError: #Not in tf dir
			print("WARNING: NOT IN TF DIRECTORY")
			prune = next_path
		self.command = "playdemo {}".format(prune.replace(".json", ".dem"))	# we pass this class a json file, so quickly switch it for the actual demo

class StopDemo(PlayCommands): #Ceases playing a demo - should be called after all vdms have played through.
	def __init__(self, stick):
		super().__init__(stick)
		self.name = "stopdem"
		self.command = "stopdemo"

#Func to use with filter() to produce a list of jsons, but only those with events. Why is this in a func instead of simply a continue statement? Because some vdms need to know what the next eventful demo is.
def HasEvents(file_name): 
	with open(file_name, "r") as f:
			events = json.loads(f.read())['events']
			if len(events) == 0:
				return False
			else:
				return True

#Search a directory (dir) for files that have extension (ext) (Returns a list of file names)
def searchdir(dir, ext, Prefix=False):
	prefix = dir+os.sep if Prefix else ''
	files = [prefix+f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) if os.path.splitext(f)[1] == ext] #This is called list comprehension. I'm looping over a directory and using if statements to determine what goes inside the list.
	files.sort() #Alphabetically, the earliest demos should be processed first
	return files

#clamp to always above 0
def clamp(n):
	if n >= 0:
		return n
	else:
		return 0

'''
 Create a vdm for every eventful json in a directory
 dir - Directory to search for JSONs
 START_MARGIN - How many ticks before the bookmark to start recording (tick - START_MARGIN)
 END_MARGIN - How many ticks after bookmark to end recording (tick + END_MARGIN)
 SKIP_MARGIN - How many ticks before a recording starts to end the skip (tick - START_MARGIN - SKIP_MARGIN)
'''
def Create(dir, START_MARGIN=500, END_MARGIN=0, SKIP_MARGIN=1):
	bmarks = searchdir(dir, ".json", Prefix=True)
	bmarks = list(filter(HasEvents, bmarks))
	for fI, file in enumerate(bmarks):	#Loop over each json
		with open(file, "r") as f:			#Open JSON for reading
			events = json.loads(f.read())['events']
			path = file.replace(".json", ".vdm")
			vdm = vdf.VDF(path)
			action_stack = [] #Some event loops may have multiple actions to add. I create a stack to push to
			for eI, e in enumerate(events):
				tick = e['tick']
				if eI == 0:	#This is the first event in the demo
					action = Skip(1, clamp(tick - START_MARGIN - SKIP_MARGIN))
					action_stack.append(action())
				action = Record(tick - START_MARGIN)
				action_stack.append(action())
				action = StopRecord(tick + END_MARGIN)
				action_stack.append(action())
				if eI+1 == len(events): #This is the last event in the demo (Not using elif, so I can insert recordings between)
					if fI+1 == len(bmarks):	#If this is the last file
						action = StopDemo(tick + 1)
						action_stack.append(action())
					else:
						action = NextDem(tick + 1, bmarks[fI+1])
						action_stack.append(action())
				else: #This is NOT the last event in the demo. (I could have put this skip creation block in an if/else statement with "if first event" but it felt more logical to include it here)
					action = Skip(tick + END_MARGIN + 1, events[eI+1]['tick'] - START_MARGIN - SKIP_MARGIN) 
					action_stack.append(action())

			#DONE DEFINING ACTIONS FOR THIS DEMO: WRITE THEM DOWN!!!
			for a in action_stack:
				vdm.commit(a)
			vdm.write()

