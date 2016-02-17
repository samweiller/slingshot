echo "Prepping the slingshot..."
echo "Firing!"

echo "Transferring TV Shows..."
scp -r ~/Documents/RipsToMove/TVSHOWS/* pi@raspberrypi.local:"/mnt/usbstorage/Mainframe/TV\\ Shows/"

echo "Transferring Movies..."
scp -r ~/Documents/RipsToMove/MOVIES/* pi@raspberrypi.local:/mnt/usbstorage/Mainframe/Movies/