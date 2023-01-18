import numpy as np
import csv

class Search:
	def __init__(self, indexPath):
		self.indexPath = indexPath

	def search(self, queryFeatures, limit = 6):
		results = {}

		with open(self.indexPath) as f:
			reader = csv.reader(f)

			for row in reader:
				features = [float(x) for x in row[1:]]
				d = self.difference(features, queryFeatures)
				if d < 0 :
					continue

				results[row[0]] = d

			f.close()

		results = sorted([(v, k) for (k, v) in results.items()])

		return results[:limit]

	def difference(self, histA, histB, eps = 1e-10):
		d = np.sum([(a - b) for (a, b) in zip(histA, histB)])

		return d