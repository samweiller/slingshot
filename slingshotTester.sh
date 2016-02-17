# slingshotTester.sh
# This is the sandbox file for the slingshot.

# for tvDirectory in $(ssh pi@raspberrypi.local ls "/mnt/usbstorage/Mainframe/TV\\ Shows/*")
# do
# 	if tvD

# for directory in $(ls -1dp * | grep /)
# for directory in $(ls -1dp "${1:-.}"/*/)
OIFS="$IFS"
IFS=$'\n'
for directory in $(find ~/Documents/RipsToMove/HOLDING_CELL -type d -name '*')
do
	# echo "directory = $directory"
	echo $directory
done