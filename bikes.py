import numpy as np

def leavingGM(m, leaveM):

	return  (1.0/(m-1)) * np.dot(leaveM, (np.ones((m,m)) - np.eye(m,m)))

def arrivingGM(m, arriveM):

	return  (1.0/(m-1)) * (np.dot((np.ones((m,m))), arriveM) - arriveM)

def make_M(m, delta):
	return delta * np.eye(m,m) #delta matrix
	
def make_arrive_leave(m, delta):
	dM = make_M(m, delta)

	arriveM = np.select([dM > 0],[dM])
	leaveM = np.select([dM < 0],[abs(dM)])

	return [arriveM, leaveM]

def logical(M):
	return np.select([abs(M) > 0],[1])
	
def my_logical_AND(M1, M2):
	return np.select([abs(M1) > 0 and abs(M2) >0],[1])
	

if __name__ == "__main__":
	pop = [[2,0,0],[0,0,0],[0,1,0],[0,1,1]] # this is the raw station population data
	pop = [np.array(x) for x in pop]

	m =len(pop[0])
	timesteps = m - 2 # this is the number of timesteps, assume no bikes travelling at start and end

	print pop

	l = []
	leaving_list = []
	arriving_list = []
	travelling = []

	for t in range(0, m + 1):

		[arriveM, leaveM] = [[], []]	
		if t < m:	
			delta_leave = pop[t+1] - pop[t]
			[junk, leaveM] = make_arrive_leave(m, delta_leave)
		if t > 0:
			delta_arrive = pop[t] - pop[t-1]
			[arriveM, junk] = make_arrive_leave(m, delta_arrive)

		print "time %d"	% t
		print arriveM
		print pop[t]
		print leaveM

		#print delta
		#[arriveM, leaveM] = make_arrive_leave(m, delta)

#		arriveGM = arrivingGM(m, arriveM)
#		leaveGM = leavingGM(m, leaveM)
#
#		leaving_list.append(leaveGM)
#		arriving_list.append(arriveGM)
#		travelling.append(leaveGM)

#		print "arrive %d" % t
#		print arriveGM
#		print "leave %d" % t
#		print leaveGM
#		l.append([logical(arriveGM), logical(leaveGM)])

#	#print np.logical_and(np.array([1,0,0]), np.array([2,0,0]))
#	print arriving_list[0]
#	print "leaving_list"
#	for l in leaving_list:
#		print l
#	print "arriving_list"
#	for l in arriving_list:
#		print l
#	print map(lambda x: np.logical_and(leaving_list[0], x), arriving_list)
