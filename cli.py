import os
import vdm

# Get a number value from input, or return a default.
def getNumVal(message, default):
	n = input(message)
	try:
		if int(n) < 0:
			print("Using default {}".format(default))
			return default
		return int(n)
	except ValueError:
		print("Using default {}".format(default))
		return default

help = """
	Welcome to STRAIGHT-TO-VDM, a program to
	create VDM files for all demos in a single directory.
	STRAIGHT-TO-VDM currently supports bookmarks created by:
		* In game demo support | SAVED AS: <demo_name>.json
	
	Please note this will overwrite VDMs currently written in your directory.
"""
print(help)
print("Write the path to your directory. Ideally, an absolute path (begins with drive). Path must be within tf/ directory.")
src = input("> ")
if "tf"+os.sep not in src:
	print("BAD DIRECTORY - IS IT A CHILD OF TF ?")
else:
	src = os.path.abspath(src)
	print("I am about to ask you to fill some parameters - each has a default and you can choose to enter nothing or a non-number value to use the default.")
	startm = getNumVal("How many ticks before a bookmark do you wish to start your recording? (Default 500)\n>", 500) 
	endm = getNumVal("How many ticks after a bookmark do you wish to end your recording? (Default 0: End on bookmark)\n>", 0)
	skipm = getNumVal("(Advanced) How many ticks before recording starts do you wish to stop fast-forwarding? (Default 1)\n>", 1)
	onlybmarks = input(" (Advanced) Skip automatically generated Killstreak bookmarks and only process manually made bookmarks? y/n\n>")
	if onlybmarks.lower() == "y":
		vdm.EventFilter = vdm.IsBookmark
	vdm.ProcessAll(src, startm, endm, skipm)
	print("Finished.")

_ = input("Press any key to exit.")
exit()
