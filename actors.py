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
	#origin = [53.33080, -6.27527]
	#origin = [53.33110, -6.28575]
	origin = [180, 85]
	#origin = [53.34418, -6.26478]
	start = value

	theta = path.bearing(origin, start)
	d = path.distance(origin, start)

	return [d * math.cos(theta), d * math.sin(theta)]

def mercator_projection(value):

	if value == None:
		return None

	[lat, lng] = value

	radius =  6378137 # m	epsg:3857 std
	x = math.radians(lng) * radius
	y = radius * math.log(math.tan(math.radians((90 + lat)/2)))

	return (x, y)

	
if __name__ == "__main__":
	x = []
	y = []

#	#plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
#	#plt.scatter(x, y, 'ro')
#
	locations = path.get_station_locations()
		
	#mercator test
	print "should be (-626172.1357121646, 6887893.4928337997)"
	print mercator_projection((52.4827802220782, -5.625 ))

	#journey = [2, 5, 25, 26]
	journey = [2, 5, 1, 2]
	one = Actor(journey)
	journey = [4, 9, 26, 25]
	two = Actor(journey)

	#agents = [one, two]
	agents = [one]
	
	#plt.axis([0, 3.5, 0, 8000])
	plt.hold(b=True)

	start = (locations[one.start])[:]
	end = (locations[one.end])[:]
	print "Path gis: ", start, end
	print "path ", one.path_points


	x0 = []
	y0 = []
	for p in one.path_points:
		[a, b] = mercator_projection(p)[:]
		x0.append(a)
		y0.append(b)
	plt.plot(x0, y0, 'ro')
	plt.savefig("test.png")

	x0 = []
	y0 = []
	for p in two.path_points:
		[a, b] = mercator_projection(p)[:]
		x0.append(a)
		y0.append(b)
	#plt.plot(x0, y0, 'bo', alpha = 0.25)
	plt.plot(x0, y0, 'bo')
	plt.savefig("test_alt.png")

#	for t in range(11):
#		x = []
#		y = []
#		for person in agents:
#			result = mercator_projection(person.call(t)) 
#			if result != None:
#				[a, b] = result
#				x.append(a); y.append(b)
#
#		plt.plot(x, y, 'bo')
#		print t, x,y
#		plt.savefig("test%d.png" % t)
