#####################
#######README########
#####################

SimTraffic

By: Tommy McLeroy

Software Engineering 2

St. Edward's University

www.github.com/foxhoundnull




How to run:

The following configurations will work, other configurations may work as well.

Windows:
1. Install python 3.2
http://www.python.org/ftp/python/3.2/python-3.2.amd64.msi
2. Install pygame 1.9.2a0
http://pygame.org/ftp/pygame-1.9.2a0.win32-py3.2.msi
3. Run Main.py


Linux:
1. Install dependencies
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev
2. Download and install pygame
svn co svn://seul.org/svn/pygame/trunk pygame
cd pygame
python setup.py build
sudo python setup.py install
3.Run Main.py





SimTraffic Description:

Real time traffic system simulator

Dynamically timed network of lights

Adaptive learning

Models real road systems




Eventual Features:

Customizable simulation settings such as speed limits, traffic levels, wait times.

Statistical reports to measure the effectiveness of timing policies

Load custom road systems via text file



Elevator Pitch:

For: local governments

Who: need to improve traffic conditions

The: SimTraffic program

Is a: traffic solution toolkit

That: offers a universally optimized solution to
traffic problems

Unlike: human error prone manual timing

This project: acts as an expert system for traffic
management