import vdm
#I enable logging
vdm.dolog = True
#I set the directory to search in and pass a file (you should probably always pass vdm.HasEvents, I don't know why I don't do it automatically.)
#(If you want to filter after initalizing, call d.filter(func)
d = vdm.Directory("tf/demos", vdm.HasEvents)
#I set the EventFilter I intend to use - This can be overwritten when you initialize an EventList, but if you intend to use a filter at all you must start here so that you can avoid "dead branches" in your VDMs.
vdm.EventFilter = vdm.IsBookmark
#I make sure each file that passed the file filter could also have events remaining after using the event filter (<IMPORTANT>) PassesEventFilter relies on vdm.EventFilter
d.filter(vdm.PassesEventFilter)
for fI, file in d:  #for index, file path in filtered directory
        #Create an EventList object, passing the filepath, the next file if available, and passing EventFilter (I set it to vdm.EventFilter, which the __init__ does anyway)
        L = vdm.EventList(file, d[fI+1], Filter=vdm.EventFilter)
        #For index, event (json) in my event list: (Index is relative to filtered events, not all events in the file
        for eI, event in L:
                #I se my default margin
                margin = 500
                if event['value'] == '5-seconds':
                    margin = 500 #Note: 500 ticks is not 5 seconds.
                elif event['value'] == '10-seconds':
                    margin = 1000 #nor is 1000 ticks 10 seconds
                #Call RecordEvent, passing the event, the index, the EventList object, and recording margins. (Defaults are 500, 0 and 1 respectively)
                vdm.RecordEvent(event, eI, L, START_MARGIN=margin, END_MARGIN=0, SKIP_MARGIN=1)
        L.write()   #Create a VDM file from the bookmarks given
