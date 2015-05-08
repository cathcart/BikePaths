import numpy as np
import itertools
import collections
import random
import os

TimeInfo = collections.namedtuple("TimeInfo", ["duration", "start", "steps"])

def total_arrive_leave(pop):

	arrive = []; leave =[]
	for x in range(1,len(pop)):
		delta = np.array(pop[x]) - np.array(pop[x-1])

		for i, v in enumerate(delta):
			if v != 0:
				if v < 0:#leave
					for count in range(abs(v)):
						leave.append((x,i+1))
				if v > 0:#arrive
					for count in range(abs(v)):
						arrive.append((x,i+1))
	
		#leaving, arriving

	return [arrive, leave]

def correct(arrive, leave):

	l = len(arrive) - len(leave)

	if l == 0:
		return [sorted(arrive, key=lambda x: x[0]), sorted(leave, key=lambda x: x[0])]

	elif l > 0:
		#add to leave
		for i in range(l):
			leave.append((random.choice([x[0] for x in leave]), random.choice([x[1] for x in leave])))#random choice according to distributions of time and stations
	elif l < 0:
		#add to arrive
		for i in range(l):
			arrive.append((random.choice([x[0] for x in arrive]), random.choice([x[1] for x in arrive])))#random choice according to distributions of time and stations

	return [sorted(arrive, key=lambda x: x[0]), sorted(leave, key=lambda x: x[0])]

def distance_time_filter(x):
	#this could be used to reject journy/travel time combinations which are physically impossible
	return True

def acceptable_ending_times(start, arrive):
        max_time = 5#max number of time units to allow
        min_time = 5#max number of time units to allow
        k = 1
        region = filter(lambda x: x[0] > start[0] and x[0] <= start[0] + k*max_time and x[1] != start[1], arrive)
       	if len(region) == 0:
                region = filter(lambda x: x[0] > start[0] and x[1] != start[1], arrive)
		print "problem", region, start, arrive[-1]
        return region

def bikes(pop):

	[arrive, leave] = total_arrive_leave(pop)

	[a, l] = correct(arrive, leave)

	journies = []
	while len(journies) < len(l):
		start = random.choice(l) #random starting station
		l.pop(l.index(start))
		delta_l = acceptable_ending_times(start, a)
		try:
			end = random.choice(delta_l)
			journies.append([start[0], end[0], start[1], end[1]])
			print start, end
			a.pop(a.index(end))
		except:
			print "problem with journey, ignoring"

	return journies
	
def load_data(file_in):

	pop = []
	times = []
	for line in open(file_in).read().strip().split("\n"):
		items = line.strip().split()
		try:
			pop.append([int(x) for x in items[1:]])
			times.append(float(items[0]))
		except IndexError:
			print line
			print items
			print len(items)
			raise IndexError
		except ValueError:
			print line
			print items[0]
			raise ValueError

	
	return pop, TimeInfo(duration=times[-1]-times[0], start=times[0], steps=len(times))
	
def write_journies(journies, data_file):

	out=open(".".join(data_file.split(".")[:-1])+".journey", "w")
	for j in journies:
		out.write("%d %d %d %d\n" %(j[0], j[1], j[2], j[3]) )

def read_journies(data_file):

	in_file = open(".".join(data_file.split(".")[:-1])+".journey", "r")
	journies = []
	for line in in_file:
		journies.append([int(x) for x in line.split()])
	return journies

def get_journies(data_file):

	in_file_name = ".".join(data_file.split(".")[:-1])+".journey"

	if os.path.exists(in_file_name):
		print "Found %s. Reading journies from file" % in_file_name
		return read_journies(data_file)	
	else:
		print "loading pop from file %s" % data_file
		pop, time_info = load_data(data_file)
		print "calculating values"
		journies = bikes(pop)
		print "writing values to file"
		write_journies(journies, data_file)
		return journies

if __name__ == "__main__":

	data_file = "data.dat"
	print get_journies(data_file)
