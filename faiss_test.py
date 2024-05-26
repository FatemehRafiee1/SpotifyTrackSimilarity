import faiss
import numpy as np

# Data preparation
d = 128  # dimension
nb = 1000000  # database size
nq = 10000  # number of queries
np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')
xq = np.random.random((nq, d)).astype('float32')
print(xb, np.shape(xb))
# Index creation and training
index = faiss.IndexFlatL2(d)
index.add(xb)
print('search')
# Searching
k = 5  # number of nearest neighbors
D, I = index.search(xq, k)
print(I)
print(D)
