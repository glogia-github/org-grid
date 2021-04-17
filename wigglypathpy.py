import sys
import random
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

def Diff_set(A,B):
	B_gen = iter(B)
	while True:
		try:
			i = next(B_gen)
			A.discard(i)
		except StopIteration:
			break
	return A

class Point:
	#must define gridsize before initializing
	def __init__(self, data1=None, data2=None):
		self.data = (data1,data2)
		self.nextval = None
		self.neighbors = set()
		self.bring_sugar()
		
	def bring_sugar(self): #find neighbors: this is not a smart way to do it. it involves adding everything and then removing stuff conditionalyl, there's probably a better way.
		for ii in (-1,0,1):  #full circle of 8
			self.neighbors.add( (self.data[0] - ii, self.data[1] + 1) )
			self.neighbors.add( (self.data[0]- ii, self.data[1]  - 1) )
		self.neighbors.add( (self.data[0] + 1, self.data[1] ) )
		self.neighbors.add( (self.data[0] - 1, self.data[1] ) )
		nb0 = iter(self.neighbors)
		removal = set()
		while True:
			try:
				xx, yy = next(nb0)
				if not (xx < 0 or yy <0 or xx >= grid_size or yy >= grid_size): #conditions in order: over the left, over the top, over the right, over the bottom of the grid
					continue
			except StopIteration:
				break
			else:
				removal.add( (xx,yy) )
		self.neighbors = Diff_set(self.neighbors, removal)
	def reset(self):
		self.nextval = None

	

class Links:
	def __init__(self):
		self.head = None
		self.current= None
		
	def path_print(self):
		printval = self.head
		while printval is not None:
			print printval.data, "|",
			printval = printval.nextval
			
	def path_plot(self):
		Coords = []
		Codes = [Path.MOVETO,]
		printval = self.head
		while printval is not None: #get coords
			Coords.append(printval.data)
			printval = printval.nextval
		for crd in range(len(Coords) - 1): #get codes
			#Codes.append(Path.LINETO)
			Codes.append(Path.CURVE3)
		path = Path(Coords, Codes)
		fig, ax = plt.subplots()
		
		#curves
		#patch = patches.PathPatch(path, facecolor='none', lw=2)
		#ax.add_patch(patch)
		
		#lines
		xs, ys = zip(*Coords)
		ax.plot(xs, ys, '--', lw=2, color='black', ms=10)
		
		#settings and plot
		ax.set_xlim(0, grid_size - 1)
		ax.set_ylim(0, grid_size - 1)
		plt.show()
	'''
	def RemoveNode(self, Removekey):

        HeadVal = self.head

        if (HeadVal is not None):
            if (HeadVal.data == Removekey):
                self.head = HeadVal.next
                HeadVal = None
                return

        while (HeadVal is not None):
            if HeadVal.data == Removekey:
                break
            prev = HeadVal
            HeadVal = HeadVal.next

        if (HeadVal == None):
            return

        prev.next = HeadVal.next

        HeadVal = None
	
	def AtBegining(self,newdata):
        NewNode = Node(newdata)
		# Update the new nodes next val to existing node
        NewNode.nextval = self.headval
        self.headval = NewNode

	
	def Inbetween(self,middle_node,newdata):
        if middle_node is None:
            print("The mentioned node is absent")
            return

        NewNode = Node(newdata)
        NewNode.nextval = middle_node.nextval
        middle_node.nextval = NewNode
		
	def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        laste = self.headval
        while(laste.nextval):
            laste = laste.nextval
        laste.nextval=NewNode
	'''

def Move(Current, Final, Prev):
	#if type(Current) != 'instance' or type(Final) !=  'instance':
	#	print "error: not a point"
	
	#moves = list(Current.neighbors) # all moves, the neighbors, so set of 2 element tuples
	moves = list(Diff_set(Current.neighbors,exclude_p))
	print moves, Prev
	if len(moves) == 0 :
		path.path_plot()
		converged = True
		return Current.data
		#sys.exit("Error: too many repeats")
	
	##RANDOM
	x, y = moves[random.randint(0,len(moves) - 1)] # select randomly
	'''
	##Constrained
	#y-y1=m(x-x1) + Current.data[1]
	#distance from point to line abs( (Final.data[0]-Current.data[0]) * (Current.data[1]-mv[1]) - (Current.data[0]-mv[0])*(Final.data[1] - Current.data[1]) ) /sqrt((Final.data[0]-Current.data[0])**2 + ()**2)
	
	moves_gen = iter(moves)
	max_diag = [0,(0,0)]
	while True:
		try:
			mv = next(moves_gen)
		except StopIteration:
			break
		else:
			#favor furthest from diagonal
			dist_diag = abs( (Final.data[0]-Current.data[0])*(Current.data[1]-mv[1]) - (Current.data[0]-mv[0])*(Final.data[1]-Current.data[1]) )/math.sqrt((Final.data[0]-Current.data[0])**2 + (Final.data[1]-Current.data[1])**2)
			#print mv, dist_diag
			if dist_diag > max_diag[0]:
				max_diag = [dist_diag, mv]
#			elif "above and below":
#				moves.remove(nb)
#			elif "directional ( below perpendicular to diagonal?)"
#				moves.remove(nb)
	x ,y = max_diag[1]
	'''
	### once it is selected
	if (x,y) in exclude_p:
		return Current.data
	elif (x,y) == Prev:
		converged = True
	else:
		pass
	#if x == x-1 or y== y-1:
	exclude_p.add( (x,y) )
	path.current.nextval = grid[x][y] #next point
	path.current = grid[x][y]
	return Current.data

if __name__ == "__main__":
	grid_size = 4
	#START = (0,0)
	#END = (grid_size -1,grid_size-1)
	START = (0,3)
	END = (3,0)
	
	for run in range(1):
		##Initialization
		exclude_p = set()
		# a list of class objects to mimic a C type array of structures
		grid = [[Point(i,j) for i in range(grid_size)] for j in range(grid_size)] #this will be crazy expensive?
		#grid = [ [Point(0,0),Point(0,1)], [Point(1,0),Point(1,1)] ]
		path = Links()
		path.head = grid[START[0]][START[1]]
		path.current = grid[START[0]][START[1]] 
		Prev = None
		##Move loop
		converged = False
		while not converged:
			Prev = Move(path.current, grid[END[0]][END[1]], Prev)
			if path.current == grid[END[0]][END[1]]:
				converged = True
		##Print
		path.path_print()
		print ""
		##Plot
		path.path_plot()