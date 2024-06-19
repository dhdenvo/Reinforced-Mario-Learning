from numpy import array
from pickle import dump
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

#Options
past_words = 16
epoch_amount = 200

# load
in_filename = 'Sequences/Mario Sequence Number ' + str(past_words) + '.txt'
doc = load_doc(in_filename)
lines = doc.split('\n')
        
# integer encode sequences of words
tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines)

# vocabulary size
vocab_size = len(tokenizer.word_index) + 1

# separate into input and output
sequences = array(sequences)
X, y = sequences[:,:-1], sequences[:,-1] #Seperates it into two arrays of the first 50 elements and the last one
y = to_categorical(y, num_classes=vocab_size)
seq_length = X.shape[1]

#define the model
model = Sequential()
model.add(Embedding(vocab_size, past_words, input_length=seq_length))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())

print("Starting Training.... Help Me :-)")
# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit model
model.fit(X, y, batch_size=128, epochs=epoch_amount) 

# save the model to file
model.save('Models/Mario Model Number ' + str(past_words) + '-' + str(epoch_amount) + '.h5')
# save the tokenizer
dump(tokenizer, open('Tokenizers/Mario Tokenizer Number ' + str(past_words) + '.pkl', 'wb'))