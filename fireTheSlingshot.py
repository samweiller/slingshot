# fireTheSlingshot.py

# STAGES
# For TV:
# Compare home dirs to remote dirs (searching for existing shows)
# If show exists, do same for subfolder (search for existing seasons)
# if Season exists, check FILES for existing episodes
# Copy only new files to appropriate directories on server
# move copied files to ROCKET folder

# For Movies:
# Compare home files to remote files (search for existing movies)
# Copy only new files to appropriate directories on server
# Move copied files to ROCKET folder

# At End:
# Ask if user wants to fire the rocket (delete copied files)


# REQUIREMENTS
# Feedback for user throughout
# NO login each time (known SSH key)
# Error handling

# import statements
import os
# this is the better, pythony way to list the TV shows
# next(os.walk('/'))[1]
TVDIR = "/Users/samweiller/Documents/RipsToMove/TVSHOWS"
dirsToCopy = []

import subprocess
TVLISTCMD = "ssh -q pi@raspberrypi.local find '/mnt/usbstorage/Mainframe/TV\\ Shows/' -maxdepth 1 -mindepth 1 -type d"
p = subprocess.Popen([TVLISTCMD], stdout=subprocess.PIPE, shell=True)
longTVList = p.stdout.readlines()

remoteShows = []
for TVshow in longTVList:
    remoteShows.append(os.path.basename(TVshow.strip()))

remoteShows.sort()

print('****** REMOTE TV SHOW LIST ******')
for i in remoteShows:
    print(i)

print('\n')

print('Scanning local files...')

localTVShows = []
for shortenedShow in next(os.walk(TVDIR))[1]:
    # # shortenedShow = os.path.basename(showName)
    # localTVShows.append(os.path.basename(showName))
    # print(localTVShows)
    # print(showName)
    # shortenedShow = os.path.basename(showName)
    if shortenedShow in remoteShows:
        print('{} already exists remotely. I will do my best to only add new files.').format(shortenedShow.upper())

        print('Scanning {} for existing seasons...').format(shortenedShow)
        SEASONCMD = "ssh -q pi@raspberrypi.local find '/mnt/usbstorage/Mainframe/TV\\ Shows/{}/' -maxdepth 1 -mindepth 1 -type d".format(shortenedShow.replace(" ", "\\ "))
        p2 = subprocess.Popen([SEASONCMD], stdout=subprocess.PIPE, shell=True)
        longSeasonList = p2.stdout.readlines()

        remoteSeasons = []
        for season in longSeasonList:
            remoteSeasons.append(os.path.basename(season.strip()))

        print("Existing Seasons:")
        for i in remoteSeasons:
            print(i)

        tempTVdir = os.path.join(TVDIR, shortenedShow)
        # print(tempTVdir)

    localSeasonList = []
    for localSeason in next(os.walk(tempTVdir))[1]:
        if localSeason in remoteSeasons:
            print("!! WARNING: {} of {} already exists remotely. If I copy these files, any identically named files on the server will be overwritten.").format(localSeason, shortenedShow)
            print("Do you want me to go ahead and copy (a)ll files, (n)ew files, or (s)kip this season completely?")

            valid = 0
            while valid == 0:
                choice = raw_input('? ')
                if choice == 'a':
                    dirsToCopy.append(os.path.join(tempTVdir, localSeason))
                    valid = 1
                elif choice == 'n':
                    #figure this out later
                    valid = 1
                elif choice == 's':
                    # do nothing
                    valid = 1
                else:
                    valid = 0
        else:
            dirsToCopy.append(os.path.join(tempTVdir, localSeason))

print("Great! These are the folders I am going to copy. Is that correct?")
for j in dirsToCopy:
    print(j)





















## end of script
