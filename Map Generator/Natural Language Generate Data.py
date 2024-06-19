from random import randint
from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

#Save a string variable to a file
def save_doc(data, filename):
    file = open(filename, 'w')
    file.write(data)
    file.close()

# generate a sequence from a language model
def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
    result = list()
    in_text = seed_text
    # generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        # truncate sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        # predict probabilities for each word
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        # append to input
        in_text += ' ' + out_word
        result.append(out_word)
    return ' '.join(result)

#generate a sequence from a language model and don't stop till there is a flag
def generate_map(model, tokenizer, seq_length, seed_text):
    generated_total = ''
    i = 0
    while True:
        generated = generate_seq(model, tokenizer, seq_length, seed_text + generated_total, 2)
        generated_total += generated + ' '
        i += 2
        if 'f'in generated or i >= 2000:
            return generated_total
        
def rotate_horizontal(generated, details = False):
    if type(generated) == str:
        generated = generated.split()
        
    turned_gen = ''
    for x_row in list(range(len(generated[0])))[::-1]:
        side_gen = ''
        for y_column in generated:
            side_gen += y_column[x_row]
        if details:
            print(side_gen)
        turned_gen += side_gen + '\n'  
        
    return turned_gen

def rotate_vertical(doc, details = False):
    if type(doc) == str:
        doc = doc.split()
        
    turned_doc = ''
    for y_column in range(len(doc[0])):
        side_doc = ''
        for x_row in doc:
            side_doc = x_row[y_column] + side_doc
        if details:
            print(side_doc)              
        turned_doc += side_doc + '\n'  
        
    return turned_doc
    

def check_duplicates(generated, prev_amount):
    generated = rotate_vertical(generated).split('\n')
    new_gen = ''
    prev = []
    for x, gen in enumerate(generated):
        prev.append(gen)
        if len(prev) == prev_amount:
            if prev == [prev[0]] * prev_amount and x >= 36:
                new_gen += '==------------\n==------------\n==---------F--\n==WFFFFFFFFFF-\n==------------\n==------------'                
                return rotate_horizontal(new_gen + gen, True)
            new_gen += prev.pop(0) + '\n'
    new_gen += '==------------\n==------------\n==---------F--\n==WFFFFFFFFFF-\n==------------\n==------------'
    return rotate_horizontal(new_gen, True)


#Option
past_words = 16
epoch_amount = 200
seed_amount = 13
seed_text = ('zztttttttttttt ' * seed_amount)[:-1]

#Fancy Seeds
seed_amount = 'O'
seed_text = 'zztttqtttttttt zztttttttttttt zztttttttttttt zztttttttttttt zztttbtttttttt zzgttqrttttttt zztttbtttqtttt zztttqtttttttt zztttbtttttttt zztttttttttttt'


# load cleaned text sequences
in_filename = 'Sequences/Mario Sequence Number ' + str(past_words) + '.txt'
doc = load_doc(in_filename)
lines = doc.split('\n')

seq_length = len(lines[0].split()) - 1

# load the model
model = load_model('Models/Mario Model Number ' + str(past_words) + '-' + str(epoch_amount) + '.h5')

# load the tokenizer
tokenizer = load(open('Tokenizers/Mario Tokenizer Number ' + str(past_words) + '.pkl', 'rb'))

# select a seed text
seed_text = seed_text.lower()

# generate new text
generated = generate_map(model, tokenizer, seq_length, seed_text)
generated = (seed_text + ' ' + generated).replace('z', '=').replace('t', '-').replace('q', '?').replace('i', '!')\
    .replace('d', '<').replace('u', '^').replace('j', '|').upper().split(' ')[:-1]

if type(seed_amount) == int:
    generated = ['==------------'] * 2 + ['==M-----------'] + ['==------------'] * (13 - seed_amount) + generated + ['==------------', '==------------']
else:
    generated = ['==------------'] * 2 + ['==M-----------'] + ['==------------'] * (13) + generated + ['==------------', '==------------']

turned_gen = rotate_horizontal(generated, True)

#print(generated[:2])

if len(turned_gen.split('\n')[0]) <= 1999:
    if len(turned_gen.split('\n')[0]) >= 84:
        save_doc(turned_gen.strip(), 'Mario N' + str(past_words) + ' E' + str(epoch_amount)[0] + 'x S' + str(seed_amount) +  '.txt')
    else:
        print('\nMap does not follow requirements')
else:
    generated = check_duplicates(turned_gen.strip(), 30)
    if len(generated.split('\n')[0]) >= 72 and len(generated.split('\n')[0]) <= 1899:
        save_doc(generated, 'Mario N' + str(past_words) + ' E' + str(epoch_amount)[0] + 'x S' + str(seed_amount) +  '.txt')
    else:
        print('\nMap does not follow requirements')
        
        