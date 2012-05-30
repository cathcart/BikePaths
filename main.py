import multiprocessing as mp
import numpy as np
import random
import functools
import actors
import bikes
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


if __name__ == "__main__":



#	[T, s, m, j] = [100, 44, 10, 90]
#	[real_journies, pop] = bikes.random_pop(T, s, m, j)
#	journies = bikes.pop_to_journies(pop)
	data_file = "feb8good.dat"
	pop = bikes.load_data(data_file)
	journies = bikes.get_journies(data_file)
	pool = mp.Pool(processes=2)

	#set palette
	palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
	new_palette = actors.Palette(palette)

	#temp_journies = journies[:1000]
	print "journies", len(journies)
	temp_journies = random.sample(journies, 1000)

	total_time = len(pop)
	time_step = 1

	func = functools.partial(load_and_print, time_delta=time_step, journies=temp_journies, total_time=total_time, palette=new_palette)
	pool.map(func, np.arange(0,total_time, time_step)) 

#	for t in np.arange(0,total_time,time_step):
#		load_and_print(t, time_step, temp_journies, total_time, new_palette)

#	#setup_bike_agents
#	print len(journies)
#        agents = []
#        for j in journies[:1000]:
#                if j[2] != j[-1]:
#			print j
#                        agents.append(actors.Actor(j, new_palette))
#
#	print "agents setup"
#	total_time = len(pop)
#	func = functools.partial(print_frame, palette=new_palette, bike_agents=agents)
#	pool.map(func, np.arange(0,total_time, 1)) 
#
