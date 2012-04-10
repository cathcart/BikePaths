import random
from math import sqrt
import matplotlib.pyplot as plt

look_up_paths = {}
look_up_stations = {}

def station_locations(stations):
	for s in range(stations):
		look_up_stations[s] = [random.randint(1, 50), random.randint(1, 50)]

class Path(object):
	#express path polynomial in a parametic equation in terms of distance travelled
	def __init__(self, journey):
		self.start = journey[2]
		self.end = journey[3]

		self.slope = float(end[1] - start[1])/(end[0] - start[0])
		
	def distance(self):
		return sqrt((float(start[0])-float(end[0]))**2 + (float(start[1])-float(end[1]))**2)
		
	def path(self):
		
		#return lambda t: [t/self.distance] 
		return lambda t: [(self.end[0]-self.start[0])*t + self.start[0], (self.end[1]-self.start[1])*t + self.start[1]]#fractional 

class Actor(object):
	def __init__(self, journey):
		self.start_time = journey[0]
		self.end_time = journey[1]
		self.time_delta = self.end_time - self.start_time -1 
		path_obj = look_up_paths(str(journey[2]) + str(journey[3]))	
	
		self.path = path_obj.path
		self.distance = path_obj.distance

	def call(time):
		if time < self.start_time or time > self.end_time:
			return None
		else:
			run_time = time - self.start_time
			fraction_of_journey = run_time/self.time_delta
			distance_travelled = self.distance * fraction_of_journey

			return self.path(distance_travelled)
		
if __name__ == "__main__":
	station_locations(10)
	pos = look_up_stations.values()
	x = [t[0] for t in pos]
	y = [t[1] for t in pos]

	plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
	#plt.scatter(x, y, 'ro')

	plt.plot(x, y, 'ro')
	plt.savefig("test.png")

	plt.plot(x, y, 'bo')
	plt.savefig("test2.png")

	#plt.show()


	
