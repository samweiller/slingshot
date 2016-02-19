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
import subprocess

os.system('clear')
print('Preparing the slingshot.')

# this is the better, pythony way to list the TV shows
# next(os.walk('/'))[1]
TVDIR = "/Users/samweiller/Documents/RipsToMove/TVSHOWS"
dirsToCopy = []

MOVDIR = "/Users/samweiller/Documents/RipsToMove/MOVIES"
moviesToCopy = []

TVLISTCMD = "ssh -q pi@raspberrypi.local find '/mnt/usbstorage/Mainframe/TV\\ Shows/' -maxdepth 1 -mindepth 1 -type d"
p = subprocess.Popen([TVLISTCMD], stdout=subprocess.PIPE, shell=True)
longTVList = p.stdout.readlines()

remoteShows = []
for TVshow in longTVList:
    remoteShows.append(os.path.basename(TVshow.strip()))

remoteShows.sort()

# print('****** REMOTE TV SHOW LIST ******')
# for i in remoteShows:
#     print(i)
#
# print('\n')

print('Scanning local files...')

localTVShows = []
for shortenedShow in next(os.walk(TVDIR))[1]:
    if shortenedShow in remoteShows:
        print('\n')
        print('{} already exists remotely. I will do my best to only add new files.').format(shortenedShow.upper())

        print('Scanning {} for existing seasons...').format(shortenedShow)
        SEASONCMD = "ssh -q pi@raspberrypi.local find '/mnt/usbstorage/Mainframe/TV\\ Shows/{}/' -maxdepth 1 -mindepth 1 -type d".format(shortenedShow.replace(" ", "\\ "))
        p2 = subprocess.Popen([SEASONCMD], stdout=subprocess.PIPE, shell=True)
        longSeasonList = p2.stdout.readlines()

        remoteSeasons = []
        for season in longSeasonList:
            remoteSeasons.append(os.path.basename(season.strip()))

        # print("Existing Seasons:")
        # for i in remoteSeasons:
        #     print(i)

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
            # This adds requested and new folders to the copy list
            dirsToCopy.append(os.path.join(tempTVdir, localSeason))

print('\n')
print("Great! These are the shows I am going to copy.")
for j in dirsToCopy:
    print("{}, {}").format(os.path.split(os.path.split(j)[0])[1], os.path.split(j)[1])
proceed  = raw_input('If this looks right, hit enter and we are good to go. If not, type n and run the program again. ')

if proceed == 'n':
    quit()

print('The TV slingshot is ready.')
print('\n')

##### MOVIES #####
print('Moving on to Movies...')
print('This process is much easier. I will only copy over new movies. Nothing extra for you to do!')

MOVLISTCMD = "ssh -q pi@raspberrypi.local find '/mnt/usbstorage/Mainframe/Movies/' -maxdepth 1 -mindepth 1"
p = subprocess.Popen([MOVLISTCMD], stdout=subprocess.PIPE, shell=True)
longMOVList = p.stdout.readlines()

remoteMovies = []
for movie in longMOVList:
    remoteMovies.append(os.path.basename(movie.strip()))

localMovies = []
for shortenedMovie in os.listdir(MOVDIR):
    # print(shortenedMovie)
    if shortenedMovie not in remoteMovies:
        # do nothing
        moviesToCopy.append(os.path.join(MOVDIR, shortenedMovie))


print('\n')
print("Okay. Looks like these are the files I am going to copy.")
print("Plex will take care of all the renaming.")
for j in moviesToCopy:
    print(os.path.split(j)[1])

proceed  = raw_input('If this looks right, hit enter and we are good to go. If not, type n and run the program again. ')

if proceed == 'n':
    quit()

print('The Movies slingshot is ready.')
print('\n')


##### FIRE THE SLINGSHOT #####
print('Firing the TV slingshot.')

for d in dirsToCopy:
    MKDIRCMD = 'ssh -q pi@raspberrypi.local mkdir -p "/mnt/usbstorage/Mainframe/TV\\ Shows/{}/{}"'.format(os.path.split(os.path.split(d)[0])[1].replace(" ", "\\ "), os.path.split(d)[1].replace(" ", "\\ "))
    COPYCMD = 'scp -r {}/* pi@raspberrypi.local:"/mnt/usbstorage/Mainframe/TV\\ Shows/{}/{}/"'.format(d.replace(" ", "\\ "), os.path.split(os.path.split(d)[0])[1].replace(" ", "\\ "), os.path.split(d)[1].replace(" ", "\\ "))
    # print(MKDIRCMD)
    # print(COPYCMD)
    os.system(MKDIRCMD)
    os.system(COPYCMD)
    os.system('mv {} /Users/samweiller/Documents/RipsToMove/ROCKET/'.format(d.replace(" ", "\\ ")))

print('\n')
print('Firing the Movies slingshot.')
for m in moviesToCopy:
    os.system('scp -r {} pi@raspberrypi.local:"/mnt/usbstorage/Mainframe/Movies/'.format(m.replace(" ", "\\ ")))
    os.system('mv {} /Users/samweiller/Documents/RipsToMove/ROCKET/'.format(m.replace(" ", "\\ ")))
    print('foo')

print('\n')
LAUNCH = raw_input('Both slingshots have been fired and copied files have been moved to ROCKET. Would you like to launch the rocket as well (y/n)? ')

if LAUNCH == 'y':
    os.system('trash /Users/samweiller/Documents/RipsToMove/ROCKET/*')
else:
    print('Copied files will remain in ROCKET.')
