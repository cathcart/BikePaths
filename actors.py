import path
import math
try:
	import matplotlib.pyplot as plt
	IsPlotting = True
except ImportError:
	print "No plotting available"
	IsPlotting = False

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
	
def convert_long_lat(value):

	if value == None:
		return None

	#start = [float(x) for x in value.strip("W").split("N")]	
	origin = [53.33080, -6.27527]
	start = value

	theta = path.bearing(origin, start)
	d = path.distance(origin, start)

	return [d * math.cos(theta), d * math.sin(theta)]

def mercator_projection(value):

	if value == None:
		return None

	radius = 6371 # km	
	#origin = [53.33110, -6.28575]
	#origin = [180, 85]
	origin = [53.34418, -6.26478]

	[lat0, lng0] = [math.radians(x) for x in origin]
	[lat1, lng1] = [math.radians(x) for x in value]

	x = radius * (lng1 - lng0)

	y = radius * math.log((1 + math.sin(lat1))/(math.cos(lat1)))

	return [x, y]
	
if __name__ == "__main__":
	x = []
	y = []

	#plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
	#plt.scatter(x, y, 'ro')

	locations = path.get_station_locations()
	for t in locations.values():
		#[a, b] = convert_long_lat(t)
		[a, b] = mercator_projection(t)
		x.append(a)
		y.append(b)

	min_x = min([t for t in x])
	max_x = max([t for t in x])
	min_y = min([t for t in y])
	max_y = max([t for t in y])

	for p in zip(x,y):
		print p[0], p[1]
		#print 640*(p[0] - min_x)/(max_x-min_x), 640*(p[1] - min_y)/(max_y-min_y)
		

	journey = [2, 5, 25, 26]
	one = Actor(journey)
	journey = [4, 9, 26, 25]
	two = Actor(journey)

	agents = [one, two]
	
	#trial_path = path.Path(journey[2], journey[3])

	#plt.plot(x, y, 'ro')
	#plt.savefig("test.png")

	for t in range(11):
		#print t, [convert_long_lat(x.call(t)) for x in agents]
		#print t, [mercator_projection(x.call(t)) for x in agents]
		print t, [x.call(t) for x in agents]

#		if t >= journey[0] and t < journey[1]:	
#			a = trial_path.position(t)
#			bike = str(a[0])+"N"+str(abs(a[1]))+"W"
#			[x, y] = convert_long_lat(bike)
#
#			if IsPlotting:	
#				plt.plot(x, y, 'bo')
#				plt.savefig("test%d.png" % t)
#			else:
#				print x,y
#	
