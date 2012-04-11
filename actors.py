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

	start = [float(x) for x in value.strip("W").split("N")]	
	origin = [53.340962, 6.262287]

	theta = path.bearing(origin, start)
	d = path.distance(origin, start)

	return [d * math.cos(theta), d * math.sin(theta)]
	
if __name__ == "__main__":
	x = []
	y = []

	#plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
	#plt.scatter(x, y, 'ro')

	locations = path.get_station_locations()
	for t in locations.values():
		[a, b] = convert_long_lat(t)
		x.append(a)
		y.append(b)
		

	journey = [2, 5, 25, 26]
	one = Actor(journey)
	journey = [4, 9, 26, 25]
	two = Actor(journey)

	agents = [one, two]
	
	#trial_path = path.Path(journey[2], journey[3])

	#plt.plot(x, y, 'ro')
	#plt.savefig("test.png")

	for t in range(11):
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
