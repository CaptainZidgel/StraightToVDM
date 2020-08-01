"Straight-to-VDM"
Take a directory of json bookmarks, create VDMs automatically. Tada!
Simply open the executable or run cli.py
You must provide the program an absolute path to your directory, which should by nested some level inside of tf/
(You can get an absolute path by double clicking the path in windows explorer and copying)

Devs:
Tested and works with >= Python 3.8
modules:
vdf - Simple parser for extremely simple cases of writing Valve Developer Format (just my case)
vdm - Create VDMs (written using vdf)
cli - Command Line Interface

How to use vdm.py: 
Create(dir, START_MARGIN=500, END_MARGIN=0, SKIP_MARGIN=1):
# dir - Directory to search for JSONs and output VDMs
# START_MARGIN 	- How many ticks before the bookmark to start recording (tick - START_MARGIN)
# END_MARGIN 		- How many ticks after bookmark to end recording (tick + END_MARGIN)
# SKIP_MARGIN 	- How many ticks before a recording starts to end the skip (tick - START_MARGIN - SKIP_MARGIN)
