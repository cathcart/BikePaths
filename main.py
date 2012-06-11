import multiprocessing as mp
import numpy as np
import random
import functools
import actors
import bikes
import sys
try:
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	import matplotlib.pyplot as plt
except ImportError:
	pass
	print "matplotlib error"
	#raise NameError("I'm not going to plot anything for you")

def print_frame(time, palette, bike_agents):

	#setup plot object
#	print "printing frame %d" % time
	fig = Figure()
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.set_frame_on(False)
	ax.set_axis_off()
	ax.axis([-700000, -694000, 7.044*pow(10,6), 6000 + 7.044*pow(10,6)])
	ax.set_autoscale_on(False)
	canvas.resize(3510, 2490)

	for bike in bike_agents:
		bike.call(ax, time)

	actors.plot_stations(palette, ax)

	#plot output
	#canvas.print_figure('alt_%05d'%int(100*time))
	canvas.print_figure('alt_%05d'%int(time))

def load_and_print(time, time_delta, journies, total_time, palette):
	active_j = filter(lambda x: x[0] <= time + time_delta and x[1] > time + time_delta, journies) 
	print "printing frame %d / %d (%d)" % (time, total_time, len(active_j))
	print_frame(time, palette, [actors.Actor(j, palette) for j in active_j])

def func2(here):
	print here

if __name__ == "__main__":

	data_file = "data.dat"
	pop = bikes.load_data(data_file)
	journies = bikes.get_journies(data_file)
	pool = mp.Pool(processes=2)

	#set palette
	palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
	new_palette = actors.Palette(palette)

	#temp_journies = journies[:1000]
	print "journies", len(journies)
	temp_journies = random.sample(journies, 100)

	total_time = len(pop)
	time_step = 1

	func = functools.partial(load_and_print, time_delta=time_step, journies=temp_journies, total_time=total_time, palette=new_palette)
	pool.map(func, range(0,total_time, time_step)) 
	#pool.map(func, np.arange(0,total_time, time_step)) 
