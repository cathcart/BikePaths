import numpy as np
from collections import defaultdict 
import itertools
import random

#def total_arrive_leave(n_pop):
#
#	n = len(n_pop[0])
#	n_time = len(n_pop)
#	d = defaultdict(lambda: np.array([0 for x in range(n)]))
#	for i in range(n_time):
#		d[i] = n_pop[i]
#
#	arrive_leave = []
#	for i in range(n_time):
#		#leave, arrive
#		arrive_leave.append([-1*sum(filter(lambda x: x<0, d[i] - d[i+1])),sum(filter(lambda x: x>0, d[i] - d[i-1]))])
#
#	#correct arrive_leave 
#	#nothing arrives at t=0
#	arrive_leave[0][1] = 0
#	#nothing leaves at t=T
#	arrive_leave[-1][0] = 0
#
#	return arrive_leave

def total_arrive_leave(pop):

	temp_pop = []; temp_al = [[0,0]]
	for x in range(1,len(pop)):
		delta = np.array(pop[x]) - np.array(pop[x-1])
		#print x, delta
		temp_al.append([-1*sum(filter(lambda x: x < 0 ,delta)), sum(filter(lambda x: x > 0 ,delta))])

	return temp_al

def bikes(temp_al, pop):

	journies = []
	#print "start"
	#print temp_al

	leave = [x[0] for x in temp_al]#all leaving
	#print leave
	leave_values = [x[0] for x in temp_al if x[0]]#list of leaving values
	#print leave_values
	leave_indexes = []
	for value in leave_values:
		i = leave.index(value)
		leave[i] = 0
		leave_indexes.append(i)
	#print "leave_indexes", leave_indexes
	

	arrive = [x[1] for x in temp_al]#all leaving
	#print arrive
	arrive_values = [x[1] for x in temp_al if x[1]]#list of indexes for leaving
	#print arrive_values
	arrive_indexes = []
	for value in arrive_values:
		i = arrive.index(value)
		arrive[i] = 0
		arrive_indexes.append(i)
	#print arrive_indexes
	#print "end"

	
	r = 0#this is the remainder 
	journies = []
	while len(leave_indexes)> 0 or len(arrive_indexes) > 0:
		if r == 0:
			l = leave_indexes.pop(0)
			a = arrive_indexes.pop(0)

		elif r > 0: # more than one bike left, get another arriving time
			a = arrive_indexes.pop(0)

		elif r < 0: # more than one bike arrived, get another leaving time
			l = leave_indexes.pop(0)

		leave = al[l][0]
		arrive = al[a][1]

		delta_l = np.array(pop[l]) - np.array(pop[l-1])
		delta_a = np.array(pop[a]) - np.array(pop[a-1])

		ss = map(bool, delta_l).index(True)
		es = map(bool, delta_a).index(True)
	
		pop[l-1][ss] -= 1	
		#pop[a][es] -= 1	
		journies.append([l, a, ss, es])
	
		r = leave - arrive

	return journies	

#def bikes(al, pop):
#
#	n = len(pop[0])
#	n_time = len(pop)
#	journey_list = []
#
#	list_which_times(al, pop)
#
#	for i in range(n_time):
#		print "i",i
#		if al[i][0] > 0:
#			print "al[i][0]",al[i][0]
#			s = 0
#			j = i + 1
#			leaving_correct = n_pop[i] - n_pop[i+1]
#			while (s < al[i][0]):
#				print n_pop[i], n_pop[j],al[j]
#				#at each step subtract off those that come before
#				arriving_correct = [ x if x>0 else 0 for x in n_pop[j] - n_pop[i]]
#				for k in range(j-1, i, -1):
#					arriving_correct -= np.array([ x if x>0 else 0 for x in n_pop[k] - n_pop[i]])
#				#each nonzero value in arriving_correct correspons to a journey
#				for k in range(len(arriving_correct)):
#					if arriving_correct[k]>0:
#						#index of the leaving station, first nonzero element from leaving_correct
#						print "leaving", leaving_correct
#						l = map(bool, leaving_correct).index(True)
#						print "A bike leaves station %d at time %d arriving at station %d at time %d" %(l,i,k,j)
#						journey_list.append([i,j,l,k])
#						#print arriving_correct,al[j]
#						leaving_correct[l] -= 1
#				s += al[j][1]
#				al[j][1] = 0
#				j +=1
#		al[i][0] = 0
#	return journey_list
#
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

def valid_journey(T, s):

	#journey = start_time end_time start_station end_station
	#this will generated invalid journeys 
	#valid journies start after the first timestep and end before the last
	j = [random.randint(1,T-2) for x in range(2)] + [random.randint(0,s-1) for x in range(2)]
	#check for validity:
	if j[1] < j[0]: #bike arrives earlier than it left
		j = valid_journey(T,s)
	if j[0] == j[1] or j[2] == j[3]: #bikes can't leave and arrive at the same station or time
		j = valid_journey(T,s) 
	return j	
	
class Population():

	def __init__(self, T, s, m):
		
		self.T = T
		self.s = s
		self.m = m
		self.__gen_station()
		self.__gen_timesteps()
		
	def __gen_station(self):
		self.basic_station = [random.randint(0,self.m-1) for x in range(self.s)]
		
	def __gen_timesteps(self):
		self.pop = [self.basic_station[:] for t in range(self.T)]
	
	def add_journey(self, journey):
		[st, et, ss, es] = journey

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
	print "pre",test_pop.pop
	for i in range(j):
		journey = valid_journey(T, s)
		print "journey", journey
		test_pop.add_journey(journey)
	print "post",test_pop.pop
	return test_pop.pop
	
if __name__ == "__main__":

	#negaive bike numbers allowed.....why forbid it??
	#pop = [[2,0,0],[0,0,0],[0,1,0],[0,1,1]] #works
	#pop = [[2,0,1],[0,0,1],[0,1,1],[0,1,2]] #works
	#pop = [[1,2,1],[1,1,1],[1,2,2],[1,1,2]] #bike timestep error, correctly caught
	#pop = [[1,2,1],[1,1,1],[1,2,2],[1,2,2]] #bike conservation error, correctly caught
	#pop = [[3, 4, 8], [3, 4, 8], [3, 4, 8], [3, 4, 8], [4, 4, 7]] # weird effect due to travel occuring duing 1 time step. have to identify and disallow this type of transfer # this is now caught correctly
	#pop = [[1, 4, 7], [1, 4, 6], [0, 4, 6], [0, 6, 6], [0, 6, 6]]# double journey test. works with verison two and three
	#print "journey", [1, 3, 2, 1], [2, 3, 0, 1]

	[T, s, m, j] = [5, 3, 10, 2]
	#print pop
	pop = random_pop(T, s, m, j)	

	al = total_arrive_leave(pop)
	checks(al)
	journies = bikes(al, pop)
	
	print journies
