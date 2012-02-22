import numpy as np




if __name__ == "__main__":
	pop = [[2,0,0],[0,0,0],[0,1,0],[0,1,1]] # this is the raw station population data
	pop = [np.array(x) for x in pop]
	#the first delta matrix is:
	
	delta1 = pop[1] - pop[0]
	print delta1
