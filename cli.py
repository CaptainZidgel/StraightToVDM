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
        * PREC                 | SAVED AS: killstreaks.txt
    Please note this will overwrite VDMs currently written in your directory.

    Will you be processing prec or in-game bookmarks? (enter PREC or IG)
"""
print(help)
support = input("PREC or IG > ")
if support.lower()[0] == "p":
    support = "prec"
elif support.lower()[0] == "i":
    support = "ds"
else:
    print("Unknown option: {}. Please type prec or ig".format(support))
print("Proceeding with {} support".format(support))
print("Write the path to your {}. Ideally, an absolute path (begins with drive). This is where VDMs will be saved.".format("directory" if support == "ds" else "killstreaks.txt"))
src = input("> ")
src = os.path.abspath(src)
d = vdm.Directory(src, JSONFilter=vdm.HasEvents, Type=support)
print("I am about to ask you to fill some parameters - each has a default and you can choose to enter nothing or a non-number value to use the default.")
startm = getNumVal("1. How many ticks before a bookmark do you wish to start your recording? (Default 500)\n>", 500) 
endm = getNumVal("2. How many ticks after a bookmark do you wish to end your recording? (Default 0: End on bookmark)\n>", 0)
skipm = getNumVal("3. (Advanced) How many ticks before recording starts do you wish to stop fast-forwarding? (Default 1)\n>", 1)
onlybmarks = input("4. (Advanced) Skip automatically generated Killstreak bookmarks and only process manually made bookmarks? y/n\n>")
if onlybmarks.lower() == "y":
    vdm.EventFilter = vdm.IsBookmark
    d.filter(vdm.PassesEventFilter)
    print("Proceeding by only processing manual bookmarks")
else:
    print("Proceeding by processing all events")
for fI, file in d:
        L = vdm.EventList(file, d)
        for eI, event in L:
                vdm.RecordEvent(event, eI, L, START_MARGIN=startm, END_MARGIN=endm, SKIP_MARGIN=skipm)
        L.write()
print("Finished.")

_ = input("Press any key to exit.")
