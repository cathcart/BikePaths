import xml.etree.cElementTree as etree
import urllib2
import os
import decoder
import math
import time
import numpy as np
import collections

LatLng = collections.namedtuple("LatLng", ["lat", "lng"])

def get_station_locations():

	if not os.path.exists("carto.xml"):
		#raise NameError("Can't find carto.xml")
		carto = urllib2.urlopen("http://www.dublinbikes.ie/service/carto").read()
		file("carto.xml", "w").write(carto)
		
	tree = etree.parse('carto.xml')

	locations = {}

	for value in tree.getiterator(tag='marker'): 
		n = value.get('number')
		lat = value.get('lat')
		lng = value.get('lng')
		name = value.get('name')

		locations[int(n)] = LatLng(lat=float(lat), lng=float(lng))

	return locations

class Path(object):
	
	def __init__(self, start, end):

		self.start = start
		self.end = end
		self.fractional_times = []
		self.reverse = False

		#load station information
		locations = get_station_locations()

		#get path data
		map_data = self.__call_maps(start, end, locations)
		self.__parse_map(map_data)

	def __call_maps(self, start, end, locations):
	
		#check if paths folder exists
		if not os.path.exists("paths"):
			try:
				os.mkdir("paths")
			except OSError:
				print "Something has gone horribly wrong. Tried to create a folder where one already existed. Exiting now."
				os.exit(1)
				
		#check if the file exists first
		if os.path.exists("paths/path_%d_%d.xml" %(start, end)) or os.path.exists("paths/path_%d_%d.xml" %(end, start)):
			print "Load path info from file"
			if os.path.exists("paths/path_%d_%d.xml" %(start, end)):
				directions = file("paths/path_%d_%d.xml" %(start, end)).read()
			else:
				directions = file("paths/path_%d_%d.xml" %(end, start)).read()
				self.reverse = True
		else:
			print "file doesn't exist. download from google"
		
			#need to catch this failing
			try:
				directions = urllib2.urlopen("http://maps.googleapis.com/maps/api/directions/xml?origin=%s&destination=%s&sensor=false" % (str(locations[start].lat)+"N"+str(abs(locations[start].lng))+"W", str(locations[end].lat)+"N"+str(abs(locations[end].lng))+"W" ) ).read()
			except KeyError:
				print start, end
				raise KeyError
			file("paths/path_%d_%d.xml" %(start, end), "w").write(directions)
			time.sleep(1)	

		return directions

	def __parse_map(self, map_data):
	
		tree = etree.fromstring(map_data)
	
		p = tree.findtext("route/overview_polyline/points")

		points = [LatLng(lat=x[0], lng=x[1]) for x in decoder.decode_line(p)]

		if self.reverse:
			self.path_points = [x for x in reversed(points)]
		else:
			self.path_points = points[:]
	
		steps = tree.findall('route/leg/step/distance')
		self.distances = [int(x.findtext('value')) for x in steps]

	def __distance(self, start, end):

		#calculate the distance between two long lat points with the haversine formula
		lat1, lon1 = start.lat, start.lng
		lat2, lon2 = end.lat, end.lng
		#radius = 6371 # km
		radius =  6378137 # m	epsg:3857 std
	
		dlat = math.radians(lat2-lat1)
		dlon = math.radians(lon2-lon1)
		a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
		    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		d = radius * c

		return d	
		#return d*1000

	def position(self, time):

		#calculate what fraction of the total journey each point corresponds to if we haven't already
		if len(self.fractional_times) == 0:
			points = self.path_points[:]
			initial = points.pop(0)
			next = points.pop(0)
			calc_dis = []
			calc_dis.append(self.__distance(initial, next))
			while len(points) > 0:
				#initial = next[:]
				initial = next
				next = points.pop(0)

				calc_dis.append(self.__distance(initial, next))
	
			total_dis = sum(self.distances)
			self.fractional_times = [sum(calc_dis[:i+1])/total_dis for i in range(len(calc_dis))]

		#find out between which two points the time corresponds to
		something = map(lambda x: abs(x-time), self.fractional_times)
		nearest = sorted(something)[0:2]
		[start, end] = sorted([something.index(x) for x in nearest])

		#create a vector
		one = np.array(self.path_points[start])
		two = np.array(self.path_points[end])
		vec = two - one

		result = vec*time + one
		return LatLng(lat=result[0], lng=result[1])

	def points_to_here(self, time):
	
		#returns a list of points that trace the path up to the fractional time, time

		current_point = self.position(time)

		times = [ x for x in self.fractional_times if x <= time]

		indexes = [times.index(i) for i in times]
		
		return [self.path_points[idx] for idx in indexes] + [current_point]

if __name__ == "__main__":

	start = 25; end = 26
	path = Path(start, end)
	print path.path_points

	start = 26; end = 25
	path = Path(start, end)
	print path.path_points

	for x in np.arange(0,1.1,0.1):
		print path.position(x)
		print type(path.position(x))
	print sorted(path.path_points)
