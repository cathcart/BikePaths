import path
import bikes
import math
import random
import numpy as np
import xml.etree.cElementTree as etree
import urllib2
try:
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	import matplotlib.pyplot as plt
	IsPlotting = True
except ImportError:
	print "No plotting available"
	IsPlotting = False
	raise NameError("I'm not going to plot anything for you")

#palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
palette = ["#556270", "#4ECDC4", "#C7F464", "#FF6B6B", "#C44D58"]

def set_random_palette():

	req = urllib2.Request("http://www.colourlovers.com/api/palettes/random", headers={'User-Agent' : "Chrome"})
	web_palette = urllib2.urlopen(req).read()

	tree = etree.fromstring(web_palette)
	p = tree.find("palette/colors")

	rand_palette = ["#" + x.text for x in p.getiterator("hex")]

	open("web_palettes.dat", "a").write(reduce(lambda x,y: "\"" + x + "\" " + y,rand_palette) + "\n")
	return rand_palette

class Actor(path.Path):
	def __init__(self, journey):
		self.start_time = journey[0]
		self.end_time = journey[1]
		self.time_delta = self.end_time - self.start_time -1

		super(Actor, self).__init__(journey[2], journey[3])

		#self.color = palette[self.start_time%len(palette)]#time
		self.color = palette[self.start%len(palette)]#start_station

	def call(self, time):
		if time >= self.start_time and time < self.end_time:
			run_time = time - self.start_time
			time_fraction = run_time/self.time_delta
			return super(Actor, self).position(time_fraction)
		else:
			return None
	
	def plot_lines(self, plt_obj, position):

		for cut in np.arange(0,1,0.05):
			x0 = []
			y0 = []
			#plot tail
			my_alpha = 0.1
			for p in [x for x in self.points_to_here(position) if x not in self.points_to_here(cut*position)]:
				[a, b] = mercator_projection(p)[:]
				x0.append(a)
				y0.append(b)
				if cut != 0:
					my_alpha = cut
			plt_obj.plot(x0, y0, self.color, alpha = my_alpha, linewidth=4)

	def plot_points(self, plt_obj, time):
		[x, y] = mercator_projection(self.position(time))[:]
		plt_obj.plot(x, y, c=self.color, marker="o", markeredgecolor=self.color)
		#plt_obj.plot(x, y, "ko")


	
def mercator_projection(value):

	if value == None:
		return None

	[lat, lng] = value

	radius =  6378137 # m	epsg:3857 std
	x = math.radians(lng) * radius
	y = radius * math.log(math.tan(math.radians((90 + lat)/2)))

	return (x, y)

	
if __name__ == "__main__":

	palette = set_random_palette()
		
	[T, s, m, j] = [200, 44, 100, 190]
	[real_journies, pop] = bikes.random_pop(T, s, m, j)
	journies = bikes.pop_to_journies(pop)

	agents = []
	for j in journies:
		if j[2] != j[-1]:
			agents.append(Actor(j))

	#setup plot object	
	fig = Figure()
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.set_frame_on(False)
	ax.set_axis_off()
	canvas.resize(3510, 2490)
	end = 0.7

	for bike in agents:
		end = random.random()
		bike.plot_lines(ax, end)
		bike.plot_points(ax, end)
	
	#plot output
	#canvas.print_figure('new', dpi=300)
	canvas.print_figure('new', dpi=600)
