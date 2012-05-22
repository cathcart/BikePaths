import multiprocessing as mp
import numpy as np
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
	canvas.print_figure('alt_%05d'%int(100*time))


if __name__ == "__main__":



#	[T, s, m, j] = [100, 44, 10, 90]
#	[real_journies, pop] = bikes.random_pop(T, s, m, j)
#	journies = bikes.pop_to_journies(pop)
	data_file = "feb8good.dat"
	journies = bikes.get_journies(data_file)
	pool = mp.Pool(processes=3)

	#set palette
	palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
	new_palette = actors.Palette(palette)

	#setup_bike_agents
        agents = []
        for j in journies:
                if j[2] != j[-1]:
                        agents.append(actors.Actor(j, new_palette))

	total_time = len(pop)
	func = functools.partial(print_frame, palette=new_palette, bike_agents=agents)
	pool.map(func, np.arange(2,total_time, 1)) 

