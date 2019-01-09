NOTE: At the moment most users will need to downgrade matplotlib to version 2.02 in order
to use this program.

 Implements a "spectrometer" using a Sofware Defined Receiver (SDR). It can receive
from any receiver supported by gnuradio via the --args argument although support 
for  rtl, airspy, uhd, & funcube receivers is slightly more streamlined. The program
spectrum_log.py  is the front end to the actual data acquisition program spectrum.py. 
The program has as  a companion program, showdata.py which is made to display the 
data format (text array) used to store the acquired spectra. 

Features: optional background subtraction (using a background spectrum measured previously),
optional line removal/reduction, optional smoothing of the spectrum acquired by low 
order polynomial fits over several adjacent points. Choice of averaging method.

Tested on Ubuntu 16.04, 18.04 and MacOS. User should have installed: python 2.7, 
gnuradio, astropy, uhd, astropy, matplotlib. Some users will need to install the specific
version 2.0.2 due to bugs in matplotlib 2.1.x . To install this specific version of
matplotlib, use: sudo pip install matplotlib==2.02. (The latest version of matplotlib
seems to have trouble working in this context.)

Credits: 
1. Initial version (data acquisiion, spectrum generation, zmq-based data handling, and 
file output, etc.) written by Danny Jacobs and his students at ASU. Summer/Fall 2018.
2. Additional features (command-line interface, improved plotting, additional receiver types, 
background subtraction, data conditioning) added by Andri Gretarsson. Fall/Winter 2018.
