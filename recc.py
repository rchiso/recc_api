import numpy as np
from numpy.linalg import norm
import heapq


def process_data(data1, data2):
    k = len(data1[0].fv)

    df1 = []
    df2 = []
    ref1 = {}
    ref2 = {}

    for i in range(len(data1)):
        if data1[i].id == data2[i].id:
            del data1[i]
            del data2[i]
        else:
            df1.append(data1[i].fv)
            df2.append(data2[i].fv)
            ref1[i] = data1[i]
            ref2[i] = data2[i]

    df1 = np.array(df1)
    df2 = np.array(df2)        
    for i in range(k):
        maxim = max(np.max(df1[:,i]), np.max(df2[:,i]))
        minim = min(np.min(df1[:,i]), np.min(df2[:,i]))

        if maxim == minim:
            continue

        df1[:,i] = (df1[:,i] - maxim) / (maxim - minim)
        df2[:,i] = (df2[:,i] - maxim) / (maxim - minim)

    return df1, df2, ref1, ref2

def find_similar_songs(data1, data2, num=3):
    df1, df2, ref1, ref2 = process_data(data1, data2)
    n = len(df1)
    num = min(n,num)
    scores_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            scores_matrix[i,j] = cosine(df1[i], df2[j])
            
    top_songs = top_k_unique_columns(scores_matrix, num)
    reccs = []
    for song_index in top_songs:
        reccs.append(ref2[song_index])
    return reccs



def cosine(x,y):
    return np.dot(x,y)/(norm(x)*norm(y))

def top_k_unique_columns(matrix, k):
    n = len(matrix)
    
    # Max-heap to store (-value, row, col)
    max_heap = []
    
    # Fill the heap with all elements
    for i in range(n):
        for j in range(n):
            heapq.heappush(max_heap, (-matrix[i][j], i, j))
    
    result = []
    used_columns = set()
    
    while len(result) < k and max_heap:
        _, _, col = heapq.heappop(max_heap)
        if col not in used_columns:
            result.append(col)  # Store the column index
            used_columns.add(col)
    
    return result
