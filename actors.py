import path
import bikes
import math
import random
try:
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	import matplotlib.pyplot as plt
	IsPlotting = True
except ImportError:
	print "No plotting available"
	IsPlotting = False
	raise NameError("I'm not going to plot anything for you")

#i like this, it works
class Actor(path.Path):
	def __init__(self, journey):
		self.start_time = journey[0]
		self.end_time = journey[1]
		self.time_delta = self.end_time - self.start_time -1

		super(Actor, self).__init__(journey[2], journey[3])

	def call(self, time):
		if time >= self.start_time and time < self.end_time:
			run_time = time - self.start
			time_fraction = run_time/self.time_delta
			return super(Actor, self).position(time_fraction)
		else:
			return None
	
	def plot(self, plt_obj, position):
		color = random.choice(["#F1B2E1", "#B1DDF3", "#FFDE89", "#E3675C", "#C2D985"])
		x0 = []
		y0 = []
		#plot weak tail
		for p in bike.points_to_here(position):
			[a, b] = mercator_projection(p)[:]
			x0.append(a)
			y0.append(b)
		plt_obj.plot(x0, y0, color, alpha = 0.1, linewidth=4)

		x0 = []
		y0 = []
		#plot mid tail
		temp = [str(x[0])+"&"+str(x[1]) for x in bike.points_to_here(position)]
		temp2 = [str(x[0])+"&"+str(x[1]) for x in bike.points_to_here(0.5*position)]
		temp3 = [[float(y) for y in x.split("&")] for x in temp if x not in temp2]
		for p in temp3:
			(a, b) = mercator_projection(p)[:]
			x0.append(a)
			y0.append(b)
		plt_obj.plot(x0, y0, color, alpha = 0.3, linewidth=4)

		x0 = []
		y0 = []
		#plot near tail
		temp = [str(x[0])+"&"+str(x[1]) for x in bike.points_to_here(position)]
		temp2 = [str(x[0])+"&"+str(x[1]) for x in bike.points_to_here(0.75*position)]
		temp3 = [[float(y) for y in x.split("&")] for x in temp if x not in temp2]
		for p in temp3:
			(a, b) = mercator_projection(p)[:]
			x0.append(a)
			y0.append(b)
		plt_obj.plot(x0, y0, color, alpha = 0.7, linewidth=4)
	
#		#ax.plot(x0[-1], y0[-1], 'ko')

	
def mercator_projection(value):

	if value == None:
		return None

	[lat, lng] = value

	radius =  6378137 # m	epsg:3857 std
	x = math.radians(lng) * radius
	y = radius * math.log(math.tan(math.radians((90 + lat)/2)))

	return (x, y)

	
if __name__ == "__main__":
		
	#[T, s, m, j] = [200, 44, 100, 190]
	[T, s, m, j] = [20, 44, 100, 1]
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
	end = 0.7

	for bike in agents:
		bike.plot(ax, end)

	#plot output
	ax.set_frame_on(False)
	ax.set_axis_off()
	canvas.resize(3510, 2490)
	canvas.print_figure('new', dpi=300)

