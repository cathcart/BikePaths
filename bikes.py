import numpy as np
#from collections import defaultdict 
import itertools
import random
import os

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

def alt_correct(arrive, leave):

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
	return True

def acceptable_ending_times(leave, start, total_time):
	end_time = np.random.poisson(min(start[0] + 72, total_time), 1)
	acceptable = []
	delta = -1

	while len(acceptable) < 1:
		delta += 1
		acceptable = filter(lambda x: x[0] >= end_time-delta and x[0] <= end_time+delta and x[1] != start[1], leave)
	return acceptable

def alt_bikes(pop):

	[arrive, leave] = total_arrive_leave(pop)

	[a, l] = alt_correct(arrive, leave)

	journies = []
	Total_journies = len(a)
	while len(journies) < Total_journies:
		print len(journies), Total_journies
		#print "Working on journey %d of %d" % (len(journies), len(a))
		start = random.choice(l) #random starting station
		#delta_l = [x for x in l[a.index(start):] if x[1] != start[1]] #acceptable ending stations
		#delta_l = acceptable_ending_times(l, start, len(pop))
		delta_l = filter(lambda x: x[0] >= start[0] and x[1] != start[1], a)
		#delta_l = filter(lambda x: distance_time_filter(x), delta_l)
		try:
			end = random.choice(delta_l)
		except IndexError:
			print delta_l
			print start
			print filter(lambda x: x[0] >= start[0], a)
			raise Error

		journies.append([start[0], end[0], start[1], end[1]])
		l.pop(l.index(start))
		a.pop(a.index(end))

	return journies
	

#def bikes(temp_al, pop):
#	
#	leave = [x[0] for x in temp_al]#all leaving
#	leave_values = [x[0] for x in temp_al if x[0]]#list of leaving values
#	leave_indexes = []
#	#for value in leave_values:
#	for value in random.sample(leave_values, len(leave_values)):
#		i = leave.index(value)
#		leave[i] = 0
#		for x in range(temp_al[i][0]):
#			leave_indexes.append(i)
#	
#
#	arrive = [x[1] for x in temp_al]#all leaving
#	arrive_values = [x[1] for x in temp_al if x[1]]#list of indexes for leaving
#	arrive_indexes = []
#	#for value in arrive_values:
#	for value in random.sample(arrive_values, len(arrive_values)):
#		i = arrive.index(value)
#		arrive[i] = 0
#		for x in range(temp_al[i][1]):
#			arrive_indexes.append(i)
#	#indexes created
#
#	print "Arriving and leaving time indexes created"
#	journies = []
#	while len(leave_indexes)> 0 or len(arrive_indexes) > 0:
#		l = leave_indexes.pop(0)
#		a = arrive_indexes.pop(0)
#		#leave = temp_al[l][0]
#		#arrive = temp_al[a][1]
#
#		delta_l = np.array(pop[l]) - np.array(pop[l-1])
#		delta_a = np.array(pop[a]) - np.array(pop[a-1])
#		print l, pop[l], delta_l
#
##		ss = map(bool, delta_l).index(True)
##		es = map(bool, delta_a).index(True)
#		ss = random.choice([x for x in range(len(pop[0])) if bool(delta_l[x])])
#		es = random.choice([x for x in range(len(pop[0])) if bool(delta_a[x])])
#	
#		pop[l-1][ss] -= 1	
#		#pop[a][es] -= 1	
#		journies.append([l, a, ss, es])
#	
#	return journies	
#
#def checks(al):
#
#	if sum([x[0] for x in al]) != sum([x[1] for x in al]):
#		print "ERROR: Bike number not conserved"
#		exit(1)
#	traveling = 0
#	for x in al:
#		if x[1] > traveling:
#			print "ERROR: bike arrives and leaves within a single timestep"
#			exit(1)
#		traveling += x[0]
#
#def valid_journey(T, s, pop):
#
#	st = random.randint(1,T-2)
#	et = random.choice([ x for x in range(1,T) if x > st])
#
#	start = [i for i in range(1, s) if pop[st][i] > 0]
#	try:
#		ss = random.choice(start)
#	except:
#		#no valid journey allowed
#		return None
#		print "ERROR, var dump"
#		print start, st, et, pop	
#		exit(1)
#	
#	end = range(1,s)
#	end.remove(ss)	
#	es = random.choice(end)
#
#	return [st, et, ss, es]
#	
#class Population():
#
#	def __init__(self, T, s, m):
#		
#		self.T = T
#		self.s = s
#		self.m = m
#		self.__gen_station()
#		self.__gen_timesteps()
#		self.journies = []
#		
#	def __gen_station(self):
#		self.basic_station = [random.randint(0,self.m-1) for x in range(self.s)]
#		
#	def __gen_timesteps(self):
#		self.pop = [self.basic_station[:] for t in range(self.T)]
#	
#	def add_journey(self, journey):
#		[st, et, ss, es] = journey
#		self.journies.append(journey)
#
#		pop_new = []
#		for t in range(self.T):
#			x = self.pop[t]
#			if t >= st:
#				x[ss] -= 1
#			if t >= et:
#				x[es] += 1
#			pop_new.append(x)
#		self.pop = pop_new[:]
#
#def random_pop(T, s, m, j):
##	T = 4 #number of timesteps
##	s = 3 #number of stations 
##	m = 10 #max number of bikes at a station
##	j = 1 #number of journies that are to be taken
#	
#	test_pop = Population(T, s, m)
#	#print "pre",test_pop.pop
#	for i in range(j):
#		journey = valid_journey(T, s, test_pop.pop)
#		#print "journey", journey
#		if journey != None:
#			test_pop.add_journey(journey)
#	#print "post",test_pop.pop
#	return [test_pop.journies, test_pop.pop]
#
#def report(journies, real_journies, pop):
#	
#	s = 0; p = 0; j = 0
#	if len(real_journies) == len(journies):
#		deltas = sum(map(lambda x, y: sum(np.array(x) - np.array(y)), sorted(journies), sorted(real_journies)))
#		if abs(deltas) != 0:
#			#print "ERROR: times or stations of predicited journeies are incorrect"
#			#print "pop", pop
#			#print "real_journies", real_journies
#			#print "journies", journies
#			#print "end of error"
#			p = 1
#		else:
#			#print "SUCCESS: everything predicited correctly"
#			#print "pop", pop
#			#print "real_journies", real_journies
#			#print "journies", journies
#			#print "end of success"
#			s = 1
#	else:
#		#[1, 2, 1, 0], [2, 3, 0, 1]]
#		#print "real", real_journies
#		if [sum(pop[0]) != sum(pop[-1])]:# two journies look like one
#			#print "SUCCESS: mild success. journey reduction"
#			#print "pop", pop
#			#print "real_journies", real_journies
#			#print "journies", journies
#			#print "end of success"
#			s = 1
#		else:
#			#print "ERROR: incorrect number of journies predicted"
#			#print "pop", pop
#			#print "real_journies", real_journies
#			#print "journies", journies
#			#print "end of error"
#			j = 1
#	
#	#success, fail predict, fail journies
#	return np.array([s, p, j])
#
#def multi_trial():	
#	#negaive bike numbers allowed.....why forbid it??
#	#pop = [[2,0,0],[0,0,0],[0,1,0],[0,1,1]] #works
#	#pop = [[2,0,1],[0,0,1],[0,1,1],[0,1,2]] #works
#	#pop = [[1,2,1],[1,1,1],[1,2,2],[1,1,2]] #bike timestep error, correctly caught
#	#pop = [[1,2,1],[1,1,1],[1,2,2],[1,2,2]] #bike conservation error, correctly caught
#	#pop = [[3, 4, 8], [3, 4, 8], [3, 4, 8], [3, 4, 8], [4, 4, 7]] # weird effect due to travel occuring duing 1 time step. have to identify and disallow this type of transfer # this is now caught correctly
#	#pop = [[1, 4, 7], [1, 4, 6], [0, 4, 6], [0, 6, 6], [0, 6, 6]]# double journey test. works with verison two and three
#	#print "journey", [1, 3, 2, 1], [2, 3, 0, 1]
#	#pop = [[4, 2], [4, 1], [4, 1], [4, 2]] # this is a double journey that comes up as a single journey. this is because the arriving of the first and leaving of the second occur at the same time
#	#real_journies [[1, 2, 1, 0], [2, 3, 0, 1]]
#
#
#	for time in range(4,20):
#		for station in range(2,20):
#			count = np.array([0, 0, 0])
#			for x in range(20):
#				[T, s, m, j] = [time, station, 10, 4]
#				[real_journies, pop] = random_pop(T, s, m, j)	
#			
#				al = total_arrive_leave(pop)
#				checks(al)
#				#print "al", al
#				journies = bikes(al, pop)
#				results = report(journies, real_journies, pop)
#		
#				count += results
#			print time, station, count[0], count[1], count[2]
#
#def pop_to_journies(pop):
#
#	al = total_arrive_leave(pop)
#	#checks(al)
#	#return bikes(al, pop)
#	return alt_bikes(al, pop)
#
#def pop_correct(pop):
#	missing_bikes = sum(pop[0]) - sum(pop[-1])
#	if missing_bikes < 0:
#		raise NameError("Stating point not early enough. Either add %d bikes to starting popution or add additional time steps" % abs(missing_bikes))
#	for bike in range(missing_bikes):
#		station = random.randint(0, len(pop[0]) -1)
#		try:
#			pop[-1][station] += 1
#		except IndexError:
#			print station
#			print len(pop[0])
#			raise Error
#	return pop
#
def load_data(file_in):

	pop = []
	for line in open(file_in).read().strip().split("\n"):
		items = line.strip().split(" ")
		try:
			#pop[float(items[0])] = [int(x) for x in items[1:]]
			pop.append([int(x) for x in items[1:]])
		except IndexError:
			print line
			print items
			print len(items)
			raise IndexError
		except ValueError:
			print line
			print items[0]
			raise ValueError

	return pop
	
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
		pop = load_data(data_file)
		print "calculating values"
		#journies = alt_bikes(pop)
		journies = alt_bikes(pop)
		print "writing values to file"
		write_journies(journies, data_file)
		return journies

if __name__ == "__main__":

	data_file = "feb8good.dat"
	print get_journies(data_file)
#	pop = load_data(data_file)
#	n_pop = pop.values()[:]
#	print "population ready"
##	print sum(n_pop[0])
##	print sum(n_pop[-1])
#	correct_pop = pop_correct(n_pop)
#	print "population corrected"
##	print sum(correct_pop[0])
##	print sum(correct_pop[-1])
#	journies = read_journies(data_file)
#	print "journies read"
#	#journies = pop_to_journies(correct_pop)
#	#print "writing journies"
#	#write_journies(journies, data_file)
##	journies = pop_to_journies(n_pop)
##	print journies
##	out = open("journies.dat", "w")
##	for time in journies:
##		for station in time:
##			out.write("%d "% station)
##		out.write("\n")
##	out.close()

##				multi_trial()
#				[T, s, m, j] = [6, 3, 10, 4]
#				[real_journies, pop] = random_pop(T, s, m, j)	
#			
#				al = total_arrive_leave(pop)
#				checks(al)
#				#print "al", al
#				journies = bikes(al, pop)
#				results = report(journies, real_journies, pop)
#				print sorted(real_journies)
#				print sorted(journies)
#				print "al", al
#				print pop
#
