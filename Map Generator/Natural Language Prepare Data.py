#Natural Text Program For Paul
import string

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

# turn a doc into clean tokens
def clean_doc(doc):
    # replace '--' with a space ' '
    doc = doc.replace('--', ' ')
    # split into tokens by white space
    tokens = doc.split()
    # remove punctuation from each token
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # make lower case
    tokens = [word.lower() for word in tokens]
    return tokens

# save tokens to file, one dialog per line
def save_doc(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()

#Options
past_words = 16

#The levels that the program goes through
levels = ['1 1', '2 1', '4 1', '5 1', '5 2', '7 1', '8 1', '8 2']
#If you want to look at one level
#levels = ['1 1']

sequences = []

for level_name in levels:
    # load document
    in_filename = 'Text Levels/World ' + level_name[0] + '/Mario W' + level_name[0] + ' L' + level_name[-1] + '.txt'
    doc = load_doc(in_filename).replace('T', 'F').replace('-', 't').replace('=', 'z').replace('?', 'Q').replace('!', 'i')\
        .replace('<', 'd').replace('^', 'u').replace('|', 'j').split('\n')
    #print(doc[:200])
    
    #Rotate Level
    turned_doc = ''
    for y_column in range(len(doc[0])):
        side_doc = ''
        for x_row in doc:
            side_doc = x_row[y_column] + side_doc
        turned_doc += side_doc + ' '
        #print(side_doc)
        
    doc = ' '.join(turned_doc[:-1].split()[16:]) 
    
    # clean document
    tokens = clean_doc(doc)
    #print(tokens[:200])
    #print('Total Tokens: %d' % len(tokens))
    #print('Unique Tokens: %d' % len(set(tokens)))
    
    # organize into sequences of tokens
    length = past_words + 1
    for i in range(length, len(tokens)):
        # select sequence of tokens
        seq = tokens[i-length:i]
        # convert into a line
        line = ' '.join(seq)
        # store
        sequences.append(line)
        
print('Total Sequences: %d' % len(sequences))

#save sequences to file
out_filename = 'Sequences/Mario Sequence Number ' + str(past_words) + '.txt'
save_doc(sequences, out_filename)