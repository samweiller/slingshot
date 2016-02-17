# python version of the slingshot!
import os

# this line lists all directories nested beneath the first argument and
# can handle spaces (which is rare).
# os.system("find ~/Documents/RipsToMove/HOLDING_CELL -d 1 -type d -name '*'")

# this is the better, pythony way to do it!
# next(os.walk('/'))[1]
TVDIR = "/Users/samweiller/Documents/RipsToMove/TVSHOWS"

# List remote TV dirs:
# ssh -q pi@raspberrypi.local find /mnt/usbstorage/Mainframe/TV\\ Shows/ -maxdepth 1 -mindepth 1 -type d

# localTVShows = []
# for showName in next(os.walk(TVDIR))[1]:
#     # shortenedShow = os.path.basename(showName)
#     localTVShows.append(os.path.basename(showName))
#     print(localTVShows)
import subprocess
TVLISTCMD = "ssh -q pi@raspberrypi.local find '/mnt/usbstorage/Mainframe/TV\\ Shows/' -maxdepth 1 -mindepth 1 -type d"
p = subprocess.Popen([TVLISTCMD], stdout=subprocess.PIPE, shell=True)
out = p.stdout.readlines()
# out.splitlines()
print out[0].strip()
