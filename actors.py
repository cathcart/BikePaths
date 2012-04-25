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
	raise NameError("I'm not going to plot anything for you")

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
		#self.time_delta = self.end_time - self.start_time -1
		self.time_delta = self.end_time - self.start_time 

		super(Actor, self).__init__(journey[2], journey[3])

		#self.color = palette[self.start_time%len(palette)]#time
		#self.color = palette[self.start%len(palette)]#start_station
		self.color = new_palette[self.start -1]

	def Distance(self, start, end):

		#calculate the distance between two long lat points with the haversine formula
		lat1, lon1 = start.lat, start.lng
		lat2, lon2 = end.lat, end.lng
		radius = 6371 # km
	
		dlat = math.radians(lat2-lat1)
		dlon = math.radians(lon2-lon1)
		a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
		    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = radius * c
	
		return d*1000


	def call(self, plt_obj, time):
		if time >= self.start_time and time < self.end_time:
			run_time = time - self.start_time
			try:
				time_fraction = float(run_time)/self.time_delta
			except ZeroDivisionError:
				print time, self.start_time, self.end_time
				print self.time_delta
				os.exit()
			#return super(Actor, self).position(time_fraction)
			self.plot_lines(plt_obj, time_fraction)
			self.plot_points(plt_obj, time_fraction)
		else:
			return None
	
	def plot_lines(self, plt_obj, time):

		#for cut in np.arange(0,1,0.05):
		for cut in np.arange(0.5,1.2,0.5):
			x0 = []
			y0 = []
			#plot tail
			my_alpha = 0.2
			for p in [x for x in self.points_to_here(time) if x not in self.points_to_here(cut*time)]:
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

def distance(a, b):
        return math.sqrt(pow(a[0]-b[0],2) + pow(a[1]-b[1],2))

def kmeans(data, n):
	#note: this only works with points that are 2D tuples. annoying but simple
	#data is the list of data points to be split
	# n is the number of splits

	mean_points = []#[random.choice(data) for x in range(n)]
	for i in range(n):
		x = random.uniform(min(data)[0], max(data)[0])
		y = random.uniform(min(data)[1], max(data)[1])

		mean_points.append((x, y))


	for i in range(10):
		split_points = [[] for x in mean_points]
	
		for point in data:
			distances = [distance(point, x) for x in mean_points]
			print distances	
			split_points[distances.index(min(distances))].append(point)


		print [len(x) for x in split_points]	
		for v in range(n):
			print split_points[v]
			mean_points[v] = tuple([(1.0/len(split_points[v]))*t for t in reduce(lambda x,y: (x[0]+y[0], x[1]+y[1]), split_points[v])])
		
		print "#here", i, mean_points
	return dict(zip(mean_points, split_points))

def mercator_projection(value):

	if value == None:
		return None

	[lat, lng] = value

	radius =  6378137 # m	epsg:3857 std
	x = math.radians(lng) * radius
	y = radius * math.log(math.tan(math.radians((90 + lat)/2)))

	return (x, y)

	
if __name__ == "__main__":

	palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
	#palette = ["#556270", "#4ECDC4", "#C7F464", "#FF6B6B", "#C44D58"]

        lat_lng_locations = path.get_station_locations().values()
        locations = [mercator_projection(v) for v in lat_lng_locations]

	splits = kmeans(locations,len(palette))

	new_palette = {}
	for v in range(len(palette)):
		for x in splits.values()[v]:
			new_palette[locations.index(x)] = palette[v]

#	fig = Figure()
#	canvas = FigureCanvas(fig)
#	ax = fig.add_subplot(111)
#	#ax.set_frame_on(False)
#	#ax.set_axis_off()
#	canvas.resize(3510, 2490)
#
#	x=[];y=[]
#	[[x.append(t[0]), y.append(t[1])] for t in [mercator_projection(z) for z in path.get_station_locations().values()]]
#	ax.plot(x, y, "ko")
#
#	#plot output
#	canvas.print_figure('stations', dpi=300)


	#palette = set_random_palette()
		
	[T, s, m, j] = [200, 44, 100, 190]
	#[T, s, m, j] = [10, 44, 100, 1]
	[real_journies, pop] = bikes.random_pop(T, s, m, j)
	journies = bikes.pop_to_journies(pop)

	agents = []
	for j in journies:
		if j[2] != j[-1]:
			agents.append(Actor(j))

	for bike in agents:
		print "new", agents.index(bike)
		bike_dict = {}
		for t in np.arange(0.1,1.1,0.1):
			a = bike.position(t - 0.1) 
			b = bike.position(t)
			bike_dict[t] = bike.Distance(a,b)
		print bike_dict

	os.exit()
	total_time = len(pop)	
	for t in range(total_time):
		#setup plot object	
		fig = Figure()
		canvas = FigureCanvas(fig)
		ax = fig.add_subplot(111)
		ax.set_frame_on(False)
		ax.set_axis_off()
		ax.axis([-700000, -694000, 7.044*pow(10,6), 6000 + 7.044*pow(10,6)])
		ax.set_autoscale_on(False)
		canvas.resize(3510, 2490)
	
		for bike in agents:
			bike.call(ax, t)

		#plot output
		for pos in locations:
			colour = new_palette[locations.index(pos)]
			#ax.text(pos[0], pos[1], locations.index(pos))
			ax.plot(pos[0], pos[1], c=colour, marker="o", markeredgecolor="k")
		canvas.print_figure('new_%03d'%t)
#	canvas.print_figure('new', dpi=600)
