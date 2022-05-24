from random import random
import numpy as np
import keras
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

model = tf.keras.models.load_model('/home/rohitkaushal/code/github/rohitkaushal7/rhyme-detection/server/services/rhyme_detection.h5')

allCharactersList = ['अ','आ','इ','ई','उ','ऊ','ऋ','ए','ऐ','ओ','औ','अं','अः','ा','ि','ी','ु','ू',' ृ','ॄ','ॅ','ॆ','े','ै','ॉ','ॊ','ो','ौ','क','ख','ग','घ','ङ',
              'च','छ','ज','झ','ञ',
              'ट','ठ','ड','ढ','ण',
              'त','थ','द','ध','न',
              'प','फ','ब','भ','म',
              'य','र','ल','व','श',
              'ष','स','ह','क्ष','त्र','श्र','ज्ञ']
char2idx = {}
for i in range(len(allCharactersList)):
    char2idx[allCharactersList[i]] = i+1
max_len = 14
char_dim = 66

def convertToNPArray(train_data):
  m = len(train_data)
  X = np.zeros((m, max_len, 66))
  for i in range(len(train_data)):
    for j in range(len(train_data[i])):
      X[i, j, train_data[i][j]] = 1
  return X

def generateTestData(test_pairs):
  train_sequences_1 = []
  train_sequences_2 = []
  for i in test_pairs:
    ts1 = []
    ts2 = []
    for character in i[0]:
      if(character in char2idx.keys()):
        ts1.append(char2idx[character])
    for character in i[1]:
      if(character in char2idx.keys()):
        ts2.append(char2idx[character])
    train_sequences_1.append(ts1)
    train_sequences_2.append(ts2)
  leaks = [[len(set(x1)), len(set(x2)), len(set(x1).intersection(x2))]
             for x1, x2 in zip(train_sequences_1, train_sequences_2)]
  train_padded_data_1 = pad_sequences(train_sequences_1, maxlen=max_len)
  train_padded_data_2 = pad_sequences(train_sequences_2, maxlen=max_len)
  leaks = np.array(leaks)
  train_padded_data_1 = convertToNPArray(train_padded_data_1)
  train_padded_data_2 = convertToNPArray(train_padded_data_2)
  return train_padded_data_1, train_padded_data_2, leaks



def is_rhyming(word1, word2):
    test_pairs = [(word1, word2)]


    test_data_x1, test_data_x2, leaks_test = generateTestData(test_pairs)

    preds = list(model.predict([test_data_x1, test_data_x2, leaks_test], verbose=1).ravel())

    if(preds[0] >= 0.91):
        return True
    return False
    

if __name__ == '__main__':
    print(is_rhyming("तैयार","विस्तार"))
    print(is_rhyming("कब","व्यक्ति"))