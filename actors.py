import path
import bikes
import math
import random
import numpy as np
import xml.etree.cElementTree as etree
import urllib2
import pickle
import os
try:
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	import matplotlib.pyplot as plt
	IsPlotting = True
except ImportError:
	pass
	#raise NameError("I'm not going to plot anything for you")

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
		#self.color = new_palette[self.start -1]

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


	def call(self, plt_obj, time, palette):
		if time >= self.start_time and time < self.end_time:
			color = palette[(self.start, time)]
			run_time = time - self.start_time
			try:
				time_fraction = float(run_time)/self.time_delta
			except ZeroDivisionError:
				print time, self.start_time, self.end_time
				print self.time_delta
				os.exit()
			#return super(Actor, self).position(time_fraction)
			self.plot_lines(plt_obj, time_fraction, color)
			self.plot_points(plt_obj, time_fraction, color)
		else:
			return None
	
	def plot_lines(self, plt_obj, time, color):

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
			plt_obj.plot(x0, y0, color, alpha = my_alpha, linewidth=4)

	def plot_points(self, plt_obj, time, color):
		[x, y] = mercator_projection(self.position(time))[:]
		plt_obj.plot(x, y, c=color, marker="o", markeredgecolor=color)
		#plt_obj.plot(x, y, "ko")

def mercator_projection(value):

	if value == None:
		return None

	[lat, lng] = value

	radius =  6378137 # m	epsg:3857 std
	x = math.radians(lng) * radius
	y = radius * math.log(math.tan(math.radians((90 + lat)/2)))

	return (x, y)

class Palette(object):
	def __init__(self, default_palette):
		self.default = default_palette
		self.__setup()

	def __setup(self):
	        lat_lng_locations = path.get_station_locations().values()
	        locations = [mercator_projection(v) for v in lat_lng_locations]
	
		splits = self.__kmeans(locations,len(palette))
	
		self.palette = {}
		for v in range(len(self.default)):
			for x in splits.values()[v]:
				self.palette[(locations.index(x), 0)] = self.default[v]

	def __getitem__(self, key):

		station, time = key
		time = int(time)
		try:
			color = self.palette[(station, time)]
		except KeyError:
			#raise NameError("time error")
			color = self.__getitem__((station, time-1))
			
		return color

	def mix(self, journey):
		st, et, ss, es = journey
		color1 = self.__getitem__((es,et))
		color2 = self.__getitem__((ss,st))
		new_color = self.__color_mix(color1, color2, pop[et][es])#weight is simply the number of bikes in the es at et
		self.palette[(es, et)] = new_color

	def __color_mix(self, color1, color2, weight):

		if weight < 0:
			weight = 0
		#average of color1*weight and color2
		r1, g1, b1 = color1[1:3], color1[3:5], color1[5:]
		r2, g2, b2 = color2[1:3], color2[3:5], color2[5:]

		nr = (1.0/(weight+1))*(weight*int(r1, 16) + int(r2, 16))
		ng = (1.0/(weight+1))*(weight*int(g1, 16) + int(g2, 16))
		nb = (1.0/(weight+1))*(weight*int(b1, 16) + int(b2, 16))

		return "#" + hex(int(nr))[2:] + hex(int(ng))[2:] + hex(int(nb))[2:]
	
	def __kmeans(self, data, n):
		#note: this only works with points that are 2D tuples. annoying but simple
		#data is the list of data points to be split
		# n is the number of splits
	
		def distance(a, b):
	        	return math.sqrt(pow(a[0]-b[0],2) + pow(a[1]-b[1],2))
	
		mean_points = []#[random.choice(data) for x in range(n)]
		for i in range(n):
			x = random.uniform(min(data)[0], max(data)[0])
			y = random.uniform(min(data)[1], max(data)[1])
	
			mean_points.append((x, y))
	
	
		for i in range(10):
			split_points = [[] for x in mean_points]
		
			for point in data:
				distances = [distance(point, x) for x in mean_points]
				split_points[distances.index(min(distances))].append(point)
	
	
			for v in range(n):
				mean_points[v] = tuple([(1.0/len(split_points[v]))*t for t in reduce(lambda x,y: (x[0]+y[0], x[1]+y[1]), split_points[v])])
			
		return dict(zip(mean_points, split_points))
	
if __name__ == "__main__":

		
	[T, s, m, j] = [1000, 44, 10, 900]
	#[T, s, m, j] = [10, 44, 100, 1]
	[real_journies, pop] = bikes.random_pop(T, s, m, j)
	journies = bikes.pop_to_journies(pop)

	#set palette
	palette = ["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"]		
	#palette = ["#556270", "#4ECDC4", "#C7F464", "#FF6B6B", "#C44D58"]

	new_palette = Palette(palette)
	#palette = set_random_palette()

	#sort journies by arrival time
	for journey in sorted(journies, key=lambda x: x[1]):
		new_palette.mix(journey)

	#get locations
      	lat_lng_locations = path.get_station_locations().values()
        locations = [mercator_projection(v) for v in lat_lng_locations]

	
	#setup_bike_agents
        agents = []
        for j in journies:
                if j[2] != j[-1]:
                        agents.append(Actor(j))

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
			bike.call(ax, t, new_palette)

		#plot output
		for pos in locations:
			colour = new_palette[(locations.index(pos), t)]
			#ax.plot(pos[0], pos[1], c=colour, marker="o", markeredgecolor="k", markersize=10.0)
			ax.plot(pos[0], pos[1], c=colour, marker="o", markeredgecolor=colour, markersize=8.0)
		canvas.print_figure('new_%03d'%t)
#	canvas.print_figure('new', dpi=600)
