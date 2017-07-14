import numpy as np

def identity(*args):
    if len(args) == 1:
        return args[0]
    return args

class TransitionModel:
	def __init__(self,getInitialState,getNextState,isEndState,maxSteps,goToState):
		self.getInitialState = getInitialState
		self.getNextState = getNextState
		self.isEndState = isEndState
		self.maxSteps = maxSteps
		self.goToState = goToState


def TransitionModelInit(getInitialState,getNextState,isEndState,maxSteps):
	getInitialState = getInitialState
	getNextState = getNextState
	isEndState = getNextisEndStateAction
	maxSteps = maxSteps
	goToState = goToState
	return TransitionModel(getInitialState,getNextState,maxSteps,goToState)

def simulate(model,p,policy,rng=np.random.RandomState(),verbose=False):
	cum_reward = 0.0
	actions = []
	s = model.getInitialState(rng)
	for i in range(model.maxSteps):
		if verbose:
			print("Step: ",i," of ", model.maxSteps)
		a = policy(p,s)
		actions.append(a)
		s,r = model.getNextState(s,a,rng)
		cum_reward += r
		if model.isEndState(s):
			break
	return cum_reward, actions