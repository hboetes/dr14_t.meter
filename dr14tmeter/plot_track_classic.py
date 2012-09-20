# dr14_t.meter: compute the DR14 value of the given audiofiles
# Copyright (C) 2011  Simone Riva
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from dr14tmeter.audio_math import *
from dr14tmeter.out_messages import *
from dr14tmeter.my_time_formatter import *

import math
import time
import datetime

try:
    import matplotlib.pyplot as pyplot
    import matplotlib.mlab as mlab
    from matplotlib import dates
except:
    ____foo = None

    
class PltTrackStruct:
    def __init__( self , plot_mode='fill' , t = [] , sz=0 , ch=0 ):
        self.ch = ch
        self.t = t
        self.start_time = 0 
        self.end_time = 0
        if plot_mode == 'fill' :
            self.mp = zeros( ( sz , ch ) )
            self.mn = zeros( ( sz , ch ) )
        else :
            self.mp = []
            self.mn = []
            
        self.Y = []
        self.plot_mode = plot_mode # or "curve"


def plot_track_str( plot_str , ax=None ):
    for j in range( plot_str.ch ):
        ax = pyplot.subplot( 210+j+1 )
        
        if plot_str.plot_mode == 'fill' :
            ax.fill( plot_str.t ,  plot_str.mp[:,j], 'b', plot_str.t ,  plot_str.mn[:,j], 'b')
        else:
            ax.plot( plot_str.t , plot_str.Y[:,j] , 'b' )
        
        pyplot.axis( [ plot_str.start_time , plot_str.end_time , -1.0 , 1.0 ] )
        
        ax.xaxis.set_major_formatter( MyTimeFormatter() )
        
        pyplot.grid(1)
        
        pyplot.title( "Channel %d" % (j+1) )
        pyplot.xlabel('Time [min:sec]')
        pyplot.ylabel('Amplitude')
        
    pyplot.show()
    

def plot_track_classic( Y , Fs , Plot=True , time_range=None , utime=0.02 , title=None , time_lim=4 , start_time=0.0 , end_time=-1.0 ):
    
    time_a = time.time()
        
    s = Y.shape
    
    if len( Y.shape ) > 1 :
        ch = s[1]
    else :
        ch = 1
        
    plot_str = PltTrackStruct( ch=ch )
 
    sz_section = s[0]
    first_sample = 0
    
    if start_time >= 0 and end_time > start_time :
        sz_section = int( ( end_time - start_time ) * Fs )
        first_sample = int( start_time * Fs )
        plot_str.start_time = start_time
        plot_str.end_time = end_time
    else :
        plot_str.start_time = 0.0
        plot_str.end_time = sz_section * 1.0/Fs
            
    
    block_len = utime
    
    samples_block = block_len * Fs
    sz = int( sz_section / samples_block )
    
    curr_sample = first_sample
    
    if sz_section > time_lim*Fs:
        plot_str.mp = zeros( ( sz , ch ) )
        plot_str.mn = zeros( ( sz , ch ) )
        plot_str.t = start_time + np.arange( 0 , sz ) * block_len
        for i in range( sz ):
            plot_str.mp[i,:] = np.max( Y[curr_sample:curr_sample+samples_block,:] , 0 )
            plot_str.mn[i,:] = np.min( Y[curr_sample:curr_sample+samples_block,:] , 0 )
            curr_sample = curr_sample + samples_block
    else:
        plot_str.plot_mode = "curve"
        plot_str.t = start_time + np.arange( sz_section ) * 1/Fs
        plot_str.Y = Y[ first_sample:first_sample+sz_section , : ]
    
    
        
    if Plot :
        plot_track_str( plot_str )
        
    return plot_str
    
    
    
    
    