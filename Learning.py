from Config import *
from pprint import pprint
import random

#this class is responsible for learning what the best light timing values are
#it uses reinforcement learning (it makes changes and monitors their effects, readjusting accordingly)
#each changeable variable is changed one at a time until its 'optimal' value is found, this is repeated 
#for each variable throughout the entirety of runtime so the variables can dynamically adjust to their optimal
#values for any given traffic conditions
class Learning():

	def __init__(self, overwatch):
		self.ow = overwatch
		self.analytics = self.ow.analytics

		self.ticks = 0
		self.samples = {}
		self.changes = {}

		#changes are made in increments of this value
		self.changeInterval = LEARNING_CHANGE_INTERVAL

		#samples are taken in increments of this value
		self.sampleInterval = LEARNING_SAMPLE_INTERVAL

		#yellow time, green time, and inactivity pause are the variables that can be safely
		#changed and will effect the effectiveness metric
		self.yt = YELLOW_TIME #seconds a light will stay yellow before turning red
		self.ytRange = {'min':2.0,'max':7.0}

		self.gt = MIN_GREEN_TIME #minimum seconds a light will stay green
		self.gtRange = {'min':1.0,'max':10.0}

		self.ip = INACTIVITY_PAUSE #seconds to pause between light switching decisions
		self.ipRange = {'min':0.0,'max':10.0}


		self.names = ['yt','gt','ip']

		#the current variable being altered
		self.currVar = self.names[0]



	#is called every frame
	def auto(self):
		#if sample time interval has passed
		if self.getTimePassed() > 0.0 and self.getTimePassed() % self.sampleInterval == 0:
			currtime = self.getTimePassed()
			#add stat sample entry for weighted effectiveness metric
			self.samples[currtime] = self.analytics.data["Weighted Effectiveness Metric"]
			#figure out which change to make, and make it
			self.evaluate(currtime, var=self.currVar)
			self.printInfo(currtime)



	def evaluate(self, currtime, var=None):
		self.changes[currtime] = {}
		#if this is the first evaluation, just record first sample and make a change
		if self.ticks == 0:
			self.samples[currtime] = self.analytics.data["Weighted Effectiveness Metric"]
			#increase first var by the standard interval
			amt = self.changeInterval
			#make the change if it's within the limits
			if self.canChange(var=var, amt=amt) : self.change(var=var, amt=amt)
			#record the change
			self.changes[currtime][var] = amt
			self.ticks += 1
		elif self.ticks >= 1:
			self.samples[currtime] = self.analytics.data["Weighted Effectiveness Metric"]
			if self.wasEffective(init=self.samples[currtime-self.sampleInterval], final=self.samples[currtime]):
				amt = self.changes[currtime-self.sampleInterval][var]
			else:
				amt = (-1 * self.changes[currtime-self.sampleInterval][var])

			#make the change if it's within the limits
			if self.canChange(var=var, amt=amt) : self.change(var=var, amt=amt)
			#record the change
			self.changes[currtime][var] = amt
			#after 3 iterations, switch to a new variable
			if self.ticks >= 5:
				self.ticks = 0
				self.currVar = self.getNextName()
				return

			self.ticks += 1


	#returns the name of the next variable to be altered
	def getNextName(self):
		maxInd = len(self.names)-1
		for i,val in enumerate(self.names):
			if self.currVar == val and i < maxInd:
				return self.names[i+1]
			elif self.currVar == val and i == maxInd:
				return self.names[0]


	#returns whether or not a change had a positive effect
	def wasEffective(self, init=None, final=None):
		return (final-init > 0.0)

	#returns whether or not a change can be made within the defined limits
	def canChange(self, var=None, amt=None):
		if var == 'yt':
			return (self.yt+amt) >= self.ytRange['min'] and (self.yt+amt) <= self.ytRange['max']
		if var == 'gt':
			return (self.gt+amt) >= self.gtRange['min'] and (self.gt+amt) <= self.gtRange['max']
		if var == 'ip':
			return (self.ip+amt) >= self.ipRange['min'] and (self.ip+amt) <= self.ipRange['max']


	#makes the actual variable change and pushed it to all the intersections
	def change(self, var=None, amt=None):
		if var == 'yt' : self.yt += amt
		elif var == 'gt' : self.gt += amt
		elif var == 'ip' : self.ip += amt

		self.ow.lc.setTimingVars(self.yt, self.gt, self.ip)


	#returns the time passed in relation to the learning modules (it doesn't start until a few minutes in)
	def getTimePassed(self):
		return (self.analytics.getTimePassed() - BASELINE_WARMUP_TIME - BASELINE_TIME - WARMUP_TIME)


	def printInfo(self, currtime):
		print ('')
		print ('Time Passed: ', self.getTimePassed()/60)
		print ("Weighted Effectiveness Metric: ",self.samples[currtime])
		#print ('Changes: ')
		#pprint (self.changes)
		print ('yt: ', self.yt)
		print ('gt: ', self.gt)
		print ('ip: ', self.ip)
		print ('')

