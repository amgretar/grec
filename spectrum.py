#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Spectrum
# Generated: Fri Jun 29 09:30:58 2018

#Edited by Danny Jacobs
# June 2018
#Edited by Andri Gretarsson 
# November 2018
##################################################
from __future__ import print_function
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter as gr_filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import zmq
import time
import numpy as np
import osmosdr

def zmq_min_max_avg(socket_str,FFT_size,nreads=1):
    #input: URL and port (ex: "tcp://127.0.0.1:5555")
    #       /nreads number of times to read from the socket
    #       get data, make an array and do something with it
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.connect(socket_str)
    mean_accum = np.zeros(FFT_size)
    count_accum = np.zeros(FFT_size)
    for i in xrange(nreads):
        data_buffer = results_receiver.recv()
        data = np.frombuffer(data_buffer,dtype=np.complex64)
        data.shape = (data.size/FFT_size,FFT_size)
        data = np.abs(data)**2
        mean_accum += np.sum(data,axis=0)
        count_accum += data.shape[0]
    mean_accum = mean_accum[count_accum>0]/count_accum[count_accum>0]
    return mean_accum

class spectrum(gr.top_block):

    def __init__(self,freq,FFT_size,SDR_BW,receiver_type,gain,portnum,extraargs):
        gr.top_block.__init__(self, 'Spectrum')

        ##################################################
        # Variables
        ##################################################
        self.tuning = tuning = 0
        self.freq = freq
        self.samp_rate = samp_rate = SDR_BW     #needs to be <BW of radio. eg at 200e6 for the x300 U160 spectrum_log.py froze after ~20 O overflows ~30 integrations
        self.data_address = data_address = 'tcp://127.0.0.1:'+str(portnum)
        self.SDR_BW = SDR_BW
        self.FFT_size = FFT_size #take the FFT_size from the input
        self.receiver_type=receiver_type
        self.gain = gain

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_0 = fft.fft_vcc(FFT_size, True, (window.blackmanharris(FFT_size)), True, 1)
        self.dc_blocker_xx_0 = gr_filter.dc_blocker_cc(1024, True)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT_size)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_gr_complex, FFT_size, data_address, 100, False, -1)
 #       self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 512)
 #       self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, "fifo", True)
 #       self.blocks_file_sink_0.set_unbuffered(False)
        
        if receiver_type == 'rtl':
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "rtl=0" + extraargs )
            print('Reciever: RTL-SDR')
        elif receiver_type == 'airspy':
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "airspy" + extraargs )
            print('Reciever: Airspy')
        elif receiver_type == 'osmo':
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" + extraargs[1:])
            print('Receiver: osmo (first gr-osmocom compatible receiver found)')
        elif receiver_type == 'uhd':
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "uhd" + extraargs  )
            print('Receiver: UHD')            
        elif receiver_type == 'funcube':
            self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "fcd=0" + extraargs  )
            print('Receiver: Funcube Pro/Pro+')            

        if receiver_type in ['rtl','airspy','osmo','uhd','funcube']:
            self.osmosdr_source_0.set_sample_rate(SDR_BW)
            self.osmosdr_source_0.set_center_freq(freq, 0)                  # first tuning happens here. Later tunings use set_tuning below
            self.osmosdr_source_0.set_dc_offset_mode(2, 0)
            self.osmosdr_source_0.set_gain_mode(True, 0)
            self.osmosdr_source_0.set_gain(gain, 0)
            self.osmosdr_source_0.set_bandwidth(0, 0)             
            # Following args and others can be set by the "extraargs" command line option
#            self.osmosdr_source_0.set_freq_corr(0, 0)
#            self.osmosdr_source_0.set_if_gain(10, 0)
#            self.osmosdr_source_0.set_bb_gain(10, 0)
#            self.osmosdr_source_0.set_antenna("", 0)
            if receiver_type == 'uhd': self.osmosdr_source_0.set_bandwidth(1.5*SDR_BW, 0) 
            self.connect((self.osmosdr_source_0, 0), (self.dc_blocker_xx_0, 0))
        else:
            print('Receiver type not recognized. Trying gr_osmocom drivers...')               
            self.osmosdr_source_0.set_sample_rate(SDR_BW)
            self.osmosdr_source_0.set_center_freq(freq, 0)
            self.osmosdr_source_0.set_dc_offset_mode(2, 0)
            self.osmosdr_source_0.set_iq_balance_mode(0, 0)
            self.osmosdr_source_0.set_gain_mode(True, 0)
            self.osmosdr_source_0.set_gain(gain, 0)
            self.connect((self.osmosdr_source_0, 0), (self.dc_blocker_xx_0, 0))

        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.zeromq_push_sink_0, 0))

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        # self.uhd_usrp_source_0.set_center_freq(self.tuning, 0)
        if self.receiver_type in ['rtl','airspy','osmo','uhd','funcube']:
            self.osmosdr_source_0.set_center_freq(self.tuning, 0)
        else:
            self.osmosdr_source_0.set_center_freq(self.tuning, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        if self.receiver_type in ['rtl','airspy','osmo','uhd','funcube']:
            self.osmosdr_source_0.set_samp_rate(self.samp_rate)
        else:
            self.osmosdr_source_0.set_samp_rate(self.samp_rate)

    def get_integration_time(self):
        return self.integration_time

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time

    def get_data_address(self):
        return self.data_address

    def set_data_address(self, data_address):
        self.data_address = data_address

    def get_SDR_BW(self):
        return self.SDR_BW

    def set_SDR_BW(self, SDR_BW):
        self.SDR_BW = SDR_BW

    def get_FFT_size(self):
        return self.FFT_size

    def set_FFT_size(self, FFT_size):
        self.FFT_size = FFT_size

    def get_gain(self,gain):
        return self.gain

    def set_gain(self,gain):
        if self.receiver_type in ['rtl','airspy','osmo','uhd','funcube']:
            self.osmosdr_source_0.set_gain(gain,0)
        else:
            self.osmosdr_source_0.set_gain(gain,0)





def main(top_block_cls=spectrum, options=None):

    tb = top_block_cls()
    tb.start(1)
    tb.wait()


if __name__ == '__main__':
    main()
