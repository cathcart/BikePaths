import numpy as np
#from collections import defaultdict 
import itertools
import random

def total_arrive_leave(pop):

	temp_pop = []; temp_al = [[0,0]]
	for x in range(1,len(pop)):
		delta = np.array(pop[x]) - np.array(pop[x-1])
		#print x, delta
		temp_al.append([-1*sum(filter(lambda x: x < 0 ,delta)), sum(filter(lambda x: x > 0 ,delta))])

	return temp_al

def bikes(temp_al, pop):
	
	leave = [x[0] for x in temp_al]#all leaving
	leave_values = [x[0] for x in temp_al if x[0]]#list of leaving values
	leave_indexes = []
	for value in leave_values:
		i = leave.index(value)
		leave[i] = 0
		for x in range(temp_al[i][0]):
			leave_indexes.append(i)
	

	arrive = [x[1] for x in temp_al]#all leaving
	arrive_values = [x[1] for x in temp_al if x[1]]#list of indexes for leaving
	arrive_indexes = []
	for value in arrive_values:
		i = arrive.index(value)
		arrive[i] = 0
		for x in range(temp_al[i][1]):
			arrive_indexes.append(i)
	#indexes created

	journies = []
	while len(leave_indexes)> 0 or len(arrive_indexes) > 0:
		l = leave_indexes.pop(0)
		a = arrive_indexes.pop(0)
		leave = temp_al[l][0]
		arrive = temp_al[a][1]

		delta_l = np.array(pop[l]) - np.array(pop[l-1])
		delta_a = np.array(pop[a]) - np.array(pop[a-1])

		ss = map(bool, delta_l).index(True)
		es = map(bool, delta_a).index(True)
	
		pop[l-1][ss] -= 1	
		#pop[a][es] -= 1	
		journies.append([l, a, ss, es])
	
	return journies	

def checks(al):

	if sum([x[0] for x in al]) != sum([x[1] for x in al]):
		print "ERROR: Bike number not conserved"
		exit(1)
	traveling = 0
	for x in al:
		if x[1] > traveling:
			print "ERROR: bike arrives and leaves within a single timestep"
			exit(1)
		traveling += x[0]

def valid_journey(T, s, pop):

	st = random.randint(1,T-2)
	et = random.choice([ x for x in range(1,T) if x > st])

	start = [i for i in range(s) if pop[st][i] > 0]
	try:
		ss = random.choice(start)
	except:
		#no valid journey allowed
		return None
		print "ERROR, var dump"
		print start, st, et, pop	
		exit(1)
	
	end = range(s)
	end.remove(ss)	
	es = random.choice(end)

	return [st, et, ss, es]
	
class Population():

	def __init__(self, T, s, m):
		
		self.T = T
		self.s = s
		self.m = m
		self.__gen_station()
		self.__gen_timesteps()
		self.journies = []
		
	def __gen_station(self):
		self.basic_station = [random.randint(0,self.m-1) for x in range(self.s)]
		
	def __gen_timesteps(self):
		self.pop = [self.basic_station[:] for t in range(self.T)]
	
	def add_journey(self, journey):
		[st, et, ss, es] = journey
		self.journies.append(journey)

		pop_new = []
		for t in range(self.T):
			x = self.pop[t]
			if t >= st:
				x[ss] -= 1
			if t >= et:
				x[es] += 1
			pop_new.append(x)
		self.pop = pop_new[:]

def random_pop(T, s, m, j):
#	T = 4 #number of timesteps
#	s = 3 #number of stations 
#	m = 10 #max number of bikes at a station
#	j = 1 #number of journies that are to be taken
	
	test_pop = Population(T, s, m)
	#print "pre",test_pop.pop
	for i in range(j):
		journey = valid_journey(T, s, test_pop.pop)
		#print "journey", journey
		if journey != None:
			test_pop.add_journey(journey)
	#print "post",test_pop.pop
	return [test_pop.journies, test_pop.pop]

def report(journies, real_journies, pop):
	
	s = 0; p = 0; j = 0
	if len(real_journies) == len(journies):
		deltas = sum(map(lambda x, y: sum(np.array(x) - np.array(y)), sorted(journies), sorted(real_journies)))
		if abs(deltas) != 0:
			#print "ERROR: times or stations of predicited journeies are incorrect"
			#print "pop", pop
			#print "real_journies", real_journies
			#print "journies", journies
			#print "end of error"
			p = 1
		else:
			#print "SUCCESS: everything predicited correctly"
			#print "pop", pop
			#print "real_journies", real_journies
			#print "journies", journies
			#print "end of success"
			s = 1
	else:
		#[1, 2, 1, 0], [2, 3, 0, 1]]
		#print "real", real_journies
		if [sum(pop[0]) != sum(pop[-1])]:# two journies look like one
			#print "SUCCESS: mild success. journey reduction"
			#print "pop", pop
			#print "real_journies", real_journies
			#print "journies", journies
			#print "end of success"
			s = 1
		else:
			#print "ERROR: incorrect number of journies predicted"
			#print "pop", pop
			#print "real_journies", real_journies
			#print "journies", journies
			#print "end of error"
			j = 1
	
	#success, fail predict, fail journies
	return np.array([s, p, j])

def multi_trial():	
	#negaive bike numbers allowed.....why forbid it??
	#pop = [[2,0,0],[0,0,0],[0,1,0],[0,1,1]] #works
	#pop = [[2,0,1],[0,0,1],[0,1,1],[0,1,2]] #works
	#pop = [[1,2,1],[1,1,1],[1,2,2],[1,1,2]] #bike timestep error, correctly caught
	#pop = [[1,2,1],[1,1,1],[1,2,2],[1,2,2]] #bike conservation error, correctly caught
	#pop = [[3, 4, 8], [3, 4, 8], [3, 4, 8], [3, 4, 8], [4, 4, 7]] # weird effect due to travel occuring duing 1 time step. have to identify and disallow this type of transfer # this is now caught correctly
	#pop = [[1, 4, 7], [1, 4, 6], [0, 4, 6], [0, 6, 6], [0, 6, 6]]# double journey test. works with verison two and three
	#print "journey", [1, 3, 2, 1], [2, 3, 0, 1]
	#pop = [[4, 2], [4, 1], [4, 1], [4, 2]] # this is a double journey that comes up as a single journey. this is because the arriving of the first and leaving of the second occur at the same time
	#real_journies [[1, 2, 1, 0], [2, 3, 0, 1]]


	for time in range(4,20):
		for station in range(2,20):
			count = np.array([0, 0, 0])
			for x in range(20):
				[T, s, m, j] = [time, station, 10, 4]
				[real_journies, pop] = random_pop(T, s, m, j)	
			
				al = total_arrive_leave(pop)
				checks(al)
				#print "al", al
				journies = bikes(al, pop)
				results = report(journies, real_journies, pop)
		
				count += results
			print time, station, count[0], count[1], count[2]

def pop_to_journies(pop):
	al = total_arrive_leave(pop)
	checks(al)
	return bikes(al, pop)
	
if __name__ == "__main__":

#				multi_trial()
				[T, s, m, j] = [6, 3, 10, 4]
				[real_journies, pop] = random_pop(T, s, m, j)	
			
				al = total_arrive_leave(pop)
				checks(al)
				#print "al", al
				journies = bikes(al, pop)
				results = report(journies, real_journies, pop)
				print sorted(real_journies)
				print sorted(journies)
				print "al", al
				print pop

