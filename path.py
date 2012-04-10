import xml.etree.cElementTree as etree
import urllib2
import os
import decoder
import math
import numpy as np

def get_station_locations():
	tree = etree.parse('carto.xml')

	locations = {}

	for value in tree.getiterator(tag='marker'): 
		n = value.get('number')
		lat = value.get('lat')
		lng = str(abs(float(value.get('lng'))))
		name = value.get('name')

		#print "%s %s %s \"%s\"" %(n,lat,lng,name)
		#locations[int(n)] = (lat, lng)
		locations[int(n)] = ("%sN%sW" % (lat, lng))

	return locations

class Path(object):
	
	def __init__(self, start, end):

		self.start = start
		self.end = end
		#load station information
		locations = get_station_locations()
		#get path data
		map_data = self.__call_maps(start, end, locations)
		self.__parse_map(map_data)
		self.fractional_times = []

	def __call_maps(self, start, end, locations):
	
		#check if the file exists first
		if os.path.exists("paths/path_%d_%d.xml" %(start, end)) or os.path.exists("paths/path_%d_%d.xml" %(end, start)):
			print "Load path info from file"
			if os.path.exists("paths/path_%d_%d.xml" %(start, end)):
				directions = file("paths/path_%d_%d.xml" %(start, end)).read()
			else:
				directions = file("paths/path_%d_%d.xml" %(end, start)).read()
		else:
			print "file doesn't exist. download from google"
		
			directions = urllib2.urlopen("http://maps.googleapis.com/maps/api/directions/xml?origin=%s&destination=%s&sensor=false" % (locations[start], locations[end]) ).read()
			file("paths/path_%d_%d.xml" %(start, end), "w").write(directions)
		
		return directions

	def __parse_map(self, map_data):
	
		tree = etree.fromstring(map_data)
	
		p = tree.findtext("route/overview_polyline/points")
		self.path_points = decoder.decode_line(p)
	
		steps = tree.findall('route/leg/step/distance')
		self.distances = [int(x.findtext('value')) for x in steps]

	def __distance(self, start, end):

		#calculate the distance between two long lat points with the haversine formula
		lat1, lon1 = start
		lat2, lon2 = end
		radius = 6371 # km
	
		dlat = math.radians(lat2-lat1)
		dlon = math.radians(lon2-lon1)
		a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
		    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = radius * c
	
		return d*1000

	def position(self, time):
		#calculate what fraction of the total journey each point corresponds to if we haven't already
		if len(self.fractional_times) == 0:
			points = self.path_points[:]
			initial = points.pop(0)
			next = points.pop(0)
			calc_dis = []
			calc_dis.append(self.__distance(initial, next))
			while len(points) > 0:
				initial = next[:]
				next = points.pop(0)
				calc_dis.append(self.__distance(initial, next))
	
			total_dis = sum(self.distances)
			self.fractional_times = [sum(calc_dis[:i+1])/total_dis for i in range(len(calc_dis))]

		#find out between which two points the time corresponds to
		something = map(lambda x: abs(x-time), self.fractional_times)
		nearest = sorted(something)[0:2]
		[start, end] = [something.index(x) for x in nearest]

		#create a vector
		one = np.array(path.path_points[start])
		two = np.array(path.path_points[end])
		vec = two - one

		return vec*time + one

if __name__ == "__main__":

	#problem here with reversing the start and end stations. should be easy enough to fix really though

	start = 25; end = 26
	start = 26; end = 25
	path = Path(start, end)

	for x in np.arange(0,1.1,0.1):
		print path.position(x)
	print sorted(path.path_points)
