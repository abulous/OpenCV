sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-opencv libatlas-base-dev gfortran libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libgtk2.0-dev
pip3 install matplotlib
pip3 install numpy
pip3 install opencv-python
echo will likely need to restart terminal, and likely need to edit config files - turn on camera Interfacing Options - Camera
echo change raspi-config now? Y/N: 
read resp
case $resp in
	y|Y|yes|Yes)
		sudo raspi-config
		;;
	n|N|no|No)
		echo install complete. Please reboot
		;;
esac
