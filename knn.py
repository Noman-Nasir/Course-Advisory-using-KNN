import numpy as np
from collections import Counter


class KNN:
	def __init__(self, k=1):
		self.k = k
	
	def train(self, x, y):
		
		# Take 20% Validation set &
		# 80% training Set

		size = int(len(x)/5)
		self.ValX = x[:size]
		self.ValY = y[:size]
		self.X = x[size:]
		self.Y = y[size:]
		return

	def predict(self, x):
		label = []
		for i in range(x.shape[0]):
			diff = self.X - x[i]
			euc = np.sum(np.square(diff), axis=1)
			min_vals = np.argpartition(euc, self.k)[0:self.k]
			l = list(self.Y[:, 0][min_vals])
			d = dict((x, l.count(x)) for x in set(l))
			mV = max(d, key=d.get)
			label.append(mV)
		return label

	def evaluate(self, x, y):
		pred_labels = self.predict(x)
		score = 0
		for i in range(y.shape[0]):
			if pred_labels[i] == y[i]:
				score += 1
		return score / y.shape[0]
	
	# Iterate From 1 to 13 and chooses Best K
	def findBestK(self):
		ks = []
		for i in range(1,21,2):
			self.k = i
			ks.append(self.evaluate(self.ValX,self.ValY))
		self.k = (np.argmax(ks)*2)+1
