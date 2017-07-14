import copy
import MDP
import MCTSdpw
import numpy as np
import RNGWrapper as RNG

DEFAULT_RSGLENGTH = 3
G_RNG = np.random.RandomState()

def get_reward_default(prob, event, terminal, dist, ast, sim):
	r = np.log(prob)
	if event:
		r += 0.0
	elif terminal:
		r += -dist
	return r

class ASTParams:
	def __init__(self,max_steps,rsg_length,init_seed,reset_seed):
		self.max_steps = max_steps
		self.rsg_length = rsg_length
		self.init_seed = init_seed
		self.reset_seed = reset_seed

def ASTParamsInit():
	return ASTParams(0,DEFAULT_RSGLENGTH,0,None)

class AdaptiveStressTest:
	def __init__(self,p,sim,initialize_fn,update_fn,isterminal_fn,reward_fn=get_reward_default):
		self.params = p
		self.sim = sim
		self.sim_hash = hash(0)
		self.initialize = initialize_fn
		self.update = update_fn
		self.isterminal = isterminal_fn
		self.get_reward = reward_fn
		self.rsg = RNG.RSGInit(p.rsg_length, p.init_seed)
		self.initial_rsg = copy.deepcopy(self.rsg)
		if not p.reset_seed is None:
			self.reset_rsg = RNG.RSGInit(p.rsg_length,p.reset_seed)
		else:
			self.reset_rsg = None
		self.transition_model = self.transition_model()
	def transition_model(self):
		return transition_model(self,self.sim)
	def reset_rsg1(self):
		self.rsg = copy.deepcopy(self.initial_rsg)

class ASTAction:
	def __init__(self,rsg):
		self.rsg = rsg
	def __hash__(self):
		return hash(self.rsg)
	def __eq__(self,other):
		return self.rsg == other.rsg

def ASTActionInit(rsg_length=DEFAULT_RSGLENGTH,seed=0):
	obj = ASTAction(RNG.RSGInit(rsg_length,seed))
	return obj

class ASTState:
	def __init__(self,t_index,hash,parent,action):
		self.t_index = t_index
		self.hash = hash
		self.parent = parent
		self.action = action
	def __hash__(self):
		if self.parent is None:
			return hash((self.t_index,None,hash(self.action)))
		else:
			return hash((self.t_index,self.parent.hash,hash(self.action)))
	def __eq__(self,other):
		return hash(self) == hash(other)


def ASTStateInit(t_index,parent,action):
	obj = ASTState(t_index,0,parent,action)
	obj.hash = hash(obj)
	return obj

def transition_model(ast,sim):
	def get_initial_state(rng):
		ast.t_index = 1
		ast.initialize(ast.sim)
		if not ast.reset_rsg is None:
			ast.rsg = copy.deepcopy(ast.reset_rsg)
		s = ASTStateInit(ast.t_index, None, ASTAction(rsg=copy.deepcopy(ast.initial_rsg)))
		ast.sim_hash = s.hash
		return s
	def get_next_state(s0,a0,rng):
		assert ast.sim_hash == s0.hash
		ast.t_index += 1
		RNG.set_global(a0.rsg)
		prob, event, dist = ast.update(ast.sim)
		s1 = ASTStateInit(ast.t_index, s0, a0)
		ast.sim_hash = s1.hash
		r = ast.get_reward(prob, event, ast.isterminal(ast.sim), dist, ast, ast.sim)
		return s1, r
	def isterminal(s):
		assert ast.sim_hash == s.hash
		return ast.isterminal(ast.sim)
	def go_to_state(target_state):
		s = get_initial_state(G_RNG)
		actions = get_action_sequence(target_state)
		R = 0.0
		for a in actions:
			s,r = get_next_state(s, a, G_RNG)
			R += r
		assert s == target_state
		return R, actions
	return MDP.TransitionModel(get_initial_state, get_next_state, isterminal, ast.params.max_steps, go_to_state)

def random_action(rsg):
	rsg.next1()
	return ASTAction(rsg=copy.deepcopy(rsg))

def get_action_sequence(s):
	actions = []
	while not s.parent is None:
		actions.append(s.action)
		s = s.parent
	actions = list(reversed(actions))
	return actions

def hash_multi_ASTAction(A):
	return hash(tuple(A))

def isequal(w,v):
	if type(w) == ASTAction:
		return RNG.isequal(w.rsg,v.rsg)
	elif type(w) == ASTState:
		return hash(w) == hash(v)


