gnuradio reciver

 Implements a "spectrometer" using a Sofware Defined Receiver (SDR). It can receive
from any receiver supported by gnuradio via the --args argument although support 
for  rtl, airspy, uhd, & funcube receivers is slightly more streamlined. The program 
spectrum_log.py  is the front end to the actual data acquisition program spectrum.py. 
The program has as  a companion program, showdata.py which is made to display the 
data format (text array) used to store the acquired spectra. 

Features: optional background subtraction (using a 
background spectrum measured previously), optional line removal/reduction, optional 
smoothing of the spectrum acquired by low order polynomial fits over several adjacent
points. Choice of averaging method.

Tested on Ubuntu16.04, `8.04 and MacOS. User should have installed: python 2.7, 
gnuradio, astropy, uhd, astropy, matplotlib==2.02 .

Credits: 
1. Initial version (data acquisiion, spectrum generation, zmq-based data handling, and 
file output, etc.) written by Danny Jacobs and his students at ASU. Summer/Fall 2018.
2. Additional features (command-line interface, improved plotting, additional receiver types, 
background subtraction, data conditioning) added by Andri Gretarsson. Fall/Winter 2018.
