import os
import glob
import sys
import random

#VARIABLES
#Arg1: Length of generated text (int) default 1000
#Arg2: Approximate length? (If true, stop at end of sentence after len reached) ('T' or 'F') default T
#Arg3: Approximate length cap (how much longer to search for end of sentence?) (int) default 50
arguments = sys.argv[1:]
gen_size = 1000
approximate = True
approx_cap = 50
if len(arguments) > 0:
    gen_size = int(arguments[0])
    if len(arguments) > 1:
        approximate = arguments[1] != 'F'
        if len(arguments) > 2:
            approx_cap = int(arguments[2])
path = 'input_text'
input_texts = []
chain = {}
starting_word = []
end_punctuation = ['.', '?', '!']
punctuation = end_punctuation + ['~', ':', ';', ',', "\"", "”", "“"]
gen_text = ''

#PARSE INPUT
for filename in glob.glob(os.path.join(path, '*.txt')):
    f = open(filename, 'r')
    text = f.read()
    for punc in punctuation:
        text = text.replace(punc, ' ' + punc + ' ')
    input_texts += [text.split()]
#TRANSFORM INPUT INTO LISTS AND DICTIONARY
for text in input_texts:
    for k in range(len(text)): #for each word in each line
        word = text[k]
        if word not in chain:
            chain[word] = []
        if (k == 0 or prev_word in end_punctuation) and word not in punctuation:
            starting_word += [word]
        elif prev_word:
            chain[prev_word] += [word]
        prev_word = word
if not input_texts:
    exit()

#GENERATE TEXT
next_word = random.choice(starting_word)
for i in range(gen_size):
    if next_word in punctuation:
        gen_text += next_word
    else:
        gen_text += ' ' + next_word
    next_list = chain[next_word]
    if next_list:
        next_word = random.choice(next_list)
    else:
        next_word = random.choice(starting_word)

if (gen_text[gen_size - 1] not in end_punctuation) and approximate:
    for i in range(approx_cap):
        if next_word in punctuation:
            gen_text += next_word
        else:
            gen_text += ' ' + next_word
        next_list = chain[next_word]
        if next_list:
            next_word = random.choice(next_list)
        else:
            next_word = random.choice(starting_word)
print(gen_text)

#make it so any of arg can be passed in in any order
