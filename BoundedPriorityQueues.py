import queue
import copy

class BoundedPriorityQueue:
	def __init__(self,pq,N):
		self.pq = pq
		self.N = N
	def enqueue(self, k, v, make_copy=False):
		if k in [pair[1] for pair in self.pq.queue]:
			return
		if make_copy:
			k = copy.deepcopy(k)
		self.pq.put((v,k))
		while self.pq.qsize() > self.N:
			self.pq.get()
	def length(self):
		return self.pq.qsize()
	def empty(self):
		while self.pq.qsize() > 0:
			self.pq.get()
	def isempty(self):
		return self.pq.qsize() == 0
	def haskey(self,k):
		return k in [pair[1] for pair in self.pq.queue]
	def __iter__(self):
		return start(self)

def BoundedPriorityQueueInit(N):
	return BoundedPriorityQueue(queue.PriorityQueue(),N)

class BPQIterator:
	def __init__(self,sorted_pairs,index):
		self.sorted_pairs = sorted_pairs
		self.index = index
	def __next__(self):
		if self.index > len(self.sorted_pairs) - 1:
			raise StopIteration
		else:
			item = self.sorted_pairs[self.index]
			self.index += 1
			return item

def start(q):
	kvs = list(reversed(sorted(q.pq.queue,key=lambda x: x[0])))
	return BPQIterator(kvs,0)

def done(q,it):
	return it.index > len(it.sorted_pairs)-1

def next(q,it):
	item = it.sorted_pairs[it.index]
	it.index += 1
	return item, it


			