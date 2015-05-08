import multiprocessing as mp
import numpy as np
import random
import functools
import actors
import bikes
import sys
import datetime
try:
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	import matplotlib.pyplot as plt
except ImportError, e:
	pass
	print "matplotlib error"
	raise NameError("I'm not going to plot anything for you", e)

def print_frame(time, time_delta, sim_duration, sim_start, palette, bike_agents):

	#setup plot object
	fig = Figure()
	fig.subplots_adjust(left=None, bottom=None, right=None, wspace=0, hspace=0)
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.set_frame_on(False)
	ax.set_axis_off()
	ax.axis([-700000, -694000, 7.044*pow(10,6), 6000 + 7.044*pow(10,6)])
	ax.set_autoscale_on(False)
	frame_time = sim_start + (time/time_delta)*(sim_duration)/(239.0/time_delta)
	ax.text(-699900, 100+7.044e6, datetime.datetime.fromtimestamp(int(frame_time)).strftime('%Y-%m-%d %H:%M:%S'), bbox=dict(facecolor='white', alpha=1.0))

	for bike in bike_agents:
		bike.call(ax, time)

	actors.plot_stations(palette, ax)

	#plot output
	print 'frame_%05d'%int(100*time)
	canvas.print_figure('frame_%05d'%int(10*time), dpi=240, facecolor=(1, 1, 1, 0))

def load_and_print(time, time_delta, sim_duration, sim_start, journies, total_time, palette):
	active_j = filter(lambda x: x[0] <= time + time_delta and x[1] > time + time_delta, journies) 
	print "printing frame %d / %d (%d)" % (time, total_time, len(active_j))
	print_frame(time, time_delta, sim_duration, sim_start, palette, [actors.Actor(j, palette) for j in active_j])

if __name__ == "__main__":

	data_file = "data.dat" #data file listing the number of bikes at each station
	pop, time_delta, time0 = bikes.load_data(data_file)
	journies = bikes.get_journies(data_file)

	#set palette
	palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
	new_palette = actors.Palette(palette)

	total_time = len(pop)
	time_step = 0.25
	func = functools.partial(load_and_print, time_delta=time_step, sim_duration=time_delta, sim_start=time0, journies=journies, total_time=total_time, palette=new_palette)
	pool = mp.Pool(processes=3)
	pool.map(func, np.arange(0,total_time, time_step)) 
