import math
import random

import clusters


def wineprice(rating, age):
  peak_age = rating - 50

  price = rating/2
  if age > peak_age:
    price = price * (5 - (age - peak_age))
  else:
    price = price * (5 * ((age + 1)/peak_age))
  return max(0, price)


def wineset1():
  rows = []
  for i in range(300):
    rating = random.random()*50 + 50
    age = random.random() * 50
    price = wineprice(rating, age) * (random.random()*0.4 + 0.8)
    rows.append({'input': (rating, age), 'result': price})
  return rows


euclidean = clusters.euclid_dist


def getdistances(data, vec1):
  distancelist = map(lambda v: euclidean(vec1, v['input']), data)
  return sorted(zip(distancelist, range(len(data))))


def knnestimate(data, vec1, k=3):
  return weightedknn(data, vec1, k=k, weightfun=lambda d:1.0)


def inverseweight(dist, num=1.0, const=0.1):
  return num/(dist + const)


def subtractweight(dist, const=1.0):
  # Returns 0 for items with no neighbors within `dist`
  return max(0, const - dist)


def gaussianweight(dist, sigma=10.0):
  return math.exp(-0.5 * (dist/sigma)**2)


def weightedknn(data, vec1, k=3, weightfun=gaussianweight):
  # Compute all n distances, but then only use k. What the hell.
  dlist = getdistances(data, vec1)

  avg = 0.0
  totalweight = 0.0
  for i in range(k):
    dist, idx = dlist[i]
    weight = weightfun(dist)
    avg += weight * data[idx]['result']
    totalweight += weight
  avg /= totalweight
  return avg


def partition(l, pred):
  """Paritions a list into to lists, based on a binary predicate."""
  flist, tlist = [], []
  for row in l:
    (tlist if pred(row) else flist).append(row)
  return flist, tlist


def dividedata(data, pTest=0.05):
  return partition(data, lambda r: random.random() < pTest)


def testalgorithm(algfun, trainset, testset):
  error = 0.0
  for row in testset:
    guess = algfun(trainset, row['input'])
    error += (row['result'] - guess)**2
  return error / len(testset)


def crossvalidate(algfun, data, trials=100, pTest=0.05):
  error = 0.0
  for i in range(trials):
    trainset, testset = dividedata(data, pTest)
    error += testalgorithm(algfun, trainset, testset)
  return error / trials


if __name__ == '__main__':
  s = wineset1()

  print knnestimate(s, (95.0, 3.0), k=1)
  print knnestimate(s, (95.0, 3.0), k=3)
  print knnestimate(s, (95.0, 3.0), k=5)
  print weightedknn(s, (95.0, 3.0), k=3)
  print wineprice(95.0, 3.0)

  print crossvalidate(knnestimate, s)
  print crossvalidate(lambda d, v: knnestimate(d, v, k=1), s)
  print crossvalidate(lambda d, v: knnestimate(d, v, k=5), s)
  print crossvalidate(lambda d, v: knnestimate(d, v, k=7), s)
  print crossvalidate(lambda d, v: weightedknn(d, v, k=5), s)
