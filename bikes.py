import numpy as np




if __name__ == "__main__":
	pop = [[2,0,0],[0,0,0],[0,1,0],[0,1,1]] # this is the raw station population data
	pop = [np.array(x) for x in pop]

	m =len(pop[0])
	timesteps = m - 2 # this is the number of timesteps, assume no bikes travelling at start and end

	for t in range(1, m):
		print t, pop[t]
	#the first delta matrix is:
	
	delta1 = pop[1] - pop[0]
	print delta1

	dM = delta1 * np.eye(3,3) #delta matrix

	arriveM = np.select([dM > 0],[dM])
	leaveM = np.select([dM < 0],[abs(dM)])

	#print arriveM
	print leaveM

	#first complete all arriving bikes
	#create guess leaving

	#leave_pathGM = (1.0/(m-1)) * leaveM * (np.ones((m,m)) - np.eye(m,m))
	leave_pathGM =  np.dot(leaveM, (np.ones((m,m)) - np.eye(m,m)))

	print leave_pathGM

