
# Straight-to-VDM
Take a directory of json bookmarks, create VDMs automatically. Tada!  
Simply open the executable or run cli.py 

You must provide the program an absolute path to your directory, which should by nested some level inside of tf/  
(You can get an absolute path by double clicking the path in windows explorer and copying)

### Devs
Tested and works with >= Python 3.8  
modules (reference for forks):

vdf - Simple parser for extremely simple cases of writing Valve Developer Format (just my case)  
vdm - Create VDMs (written using vdf)  
cli - Command Line Interface  

##### scripting:
You can use vdm as a module for a script to very finely process each demo! example:  
Set specific recording lengths based on bookmark name!  
Exclude specific bookmark names!  
Using vdm as a module is very granular and if you intend on treating every event the same and with no filters, you might as well use cli.py  
Tutorial:  
(See example_script.py or cli.py for examples)  
Any time I mention a >**filter_func**<, a function you would use with filter(), a function that returns True or False. The defaults always return True.  
A Directory filter will filter .json files, an EventFilter will filter events IN a .json file. 

##### OK BUT HOW DO I ACTUALLY USE IT?

In essence, you must create a Directory object of files, loop on each of those files, creating an EventList object to loop through events.

```python
d = vdm.Directory(path, filter_func)
```
If you use EventFilters, you must first now `vdm.EventFilter` to your func, and then call   `Directory.filter(vdm.PassesEventFilter)`  
This is required to make sure you do not filter all the events out of a json, leaving the loop with no events to process (which is bad). 
```python
d = vdm.Directory(path, filter_func)
vdm.EventFilter = my_event_filter_func
d.filter(vdm.PassesEventFilter)
```

[ You can also call `d.filter(your_func)` to filter your directory as many times as you like before moving on. ]
```python
for file_index, file_path in d:
	L = vdm.EventList(file_path, d[file_index+1], filter_func)
```
	
[ file_path and file_index+1 must be passed exactly like that, as vdms usefulness relies on information from other files. filter is optional. ]
```python
for file_index, file_path in d:
	L = vdm.EventList(file_path, d[file_index+1], filter_func)
	for eventIndex, event in L:
		vdm.RecordEvent(event, eventIndex, L, START_MARGIN=500, END_MARGIN=0, SKIP_MARGIN=1)
	L.write()
```
	
[ event, eventIndex, and L must be passed exactly like that, as vdms usefulness relies on information from other events.  
Each event has a tick of the moment you pressed your bind. Here is how you can use that information:  
START_MARGIN is how many ticks to start recording before a bookmark (tick - START_MARGIN)  
END_MARGIN is how many ticks to stop recording after a bookmark (tick + END_MARGIN)  
SKIP_MARGIN is how many ticks to stop fast forwarding before a recording (tick - START_MARGIN - SKIP_MARGIN) ]  
L.write() will actually create the VDM file from your event information. Everything is handled within the L object.  

I am very bad at describing my code, something about trying to make this a module breaks my brain.  
If you have questions please ask!
