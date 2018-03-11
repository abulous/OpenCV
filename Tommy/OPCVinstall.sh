sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-opencv gfortran
pip3 install matplotlib
pip3 install numpy
pip3 install opencv-python
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install libgdk2.0-pixbuf2.0-dev libpango1.0-dev libcairo2-dev
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libgtk2.0-dev

echo will likely need to restart terminal, and likely need to edit config files - turn on camera, expand file system, and might as well enable SSH and VNC while youre at it
echo change raspi-config now? Y/N: 
read resp
case $resp in
	y|Y|yes|Yes)
		sudo raspi-config
		;;
	n|N|no|No)
		echo install complete.
		;;
esac
echo restart now? y/n
read rest
case $rest in
	y|Y|yes|Yes)
		reboot
		;;
	n|N|no|No)
		echo you may need to restart for changes to work.
		;;
esac
