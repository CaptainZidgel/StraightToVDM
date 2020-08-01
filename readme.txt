"Straight-to-VDM"
Take a directory of json bookmarks, create VDMs automatically. Tada!
Simply open the executable or run cli.py
You must provide the program an absolute path to your directory, which should by nested some level inside of tf/
(You can get an absolute path by double clicking the path in windows explorer and copying)

Devs: 
Tested and works with >= Python 3.8

modules (reference for forks):
vdf - Simple parser for extremely simple cases of writing Valve Developer Format (just my case)
vdm - Create VDMs (written using vdf)
cli - Command Line Interface

scripting:
You can use vdm as a module for a script to very finely process each demo! example:
Set specific recording lengths based on bookmark name!
Exclude specific bookmark names!
Tutorial:

vdm.ProcessAll(dir, START_MARGIN=500, END_MARGIN=0, SKIP_MARGIN=1):
# dir - Directory to search for JSONs and output VDMs
# START_MARGIN 	- How many ticks before the bookmark to start recording (tick - START_MARGIN)
# END_MARGIN 		- How many ticks after bookmark to end recording (tick + END_MARGIN)
# SKIP_MARGIN 	- How many ticks before a recording starts to end the skip (tick - START_MARGIN - SKIP_MARGIN)
This is what CLI calls.

You can control more details by writing your own loops to collect jsons and filter their events.

vdm.Process(file, collection, fI, START_MARGIN, END_MARGIN, SKIP_MARGIN):'''
# file - the path to file
# collection - the list of paths to jsons - this is used to access jsons that follow another json
# fI - the index of the file, in a loop
# START_MARGIN - How many ticks before the bookmark to start recording (tick - START_MARGIN)
# END_MARGIN - How many ticks after bookmark to end recording (tick + END_MARGIN)
# SKIP_MARGIN - How many ticks before a recording starts to end the skip (tick - START_MARGIN - SKIP_MARGIN)
Each parameter is positional and extremely NECESSARY! You are basically just reimplementing ProcessAll!

This function is just my own and you'll probably write your own, but it is here if you want it :)
Use Prefix=True so when you operate on things in this list, you can actually get the file path instead of filename.
vdm.searchdir(dir, ext=".json", Prefix=False):
# dir - The directory to collect jsons from
# ext - File extensions to look for
# Prefix - Whether or not to include filepath
Returns a list

(Things you can change that will take effect during the default Process)
vdm.EventFilter = my_func
Set this to any bool-returning function you want, 
def my_func(event):
	if event['tick'] > 5:
		return True
will choose which events can be recorded
vdm.JSONFilter
Chooses which jsons get picked when using ProcessAll.
ProcessAll also implements a filter that only processes jsons with events.