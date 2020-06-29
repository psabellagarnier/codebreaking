import numpy as np
import random, copy


letters=[chr(i) for i in range(97,123)]
digits=[str(i) for i in range(10)]

#Dictionaries to go from characters to their indices and back (all digits get mapped to '0')

char_to_n=dict(zip(letters+digits+[" "]+["\n"]+["\t"],[a for a in range(len(letters))]+len(digits)*[len(letters)]+[len(letters)+1]+[len(letters)+2]+[len(letters)+3]))   
n_to_char=dict(zip([a for a in range(len(letters))]+[len(letters)]+[len(letters)+1]+[len(letters)+2]+[len(letters)+3],letters+['0']+[' ']+['\n']+['\t']))  

#Dictionaries, lists to keep track of 2-grams and 3-grams
two_grams = []
for a in letters:
    for b in letters:
        two_grams.append(a+b)
three_grams = []
for a in letters:
    for b in letters:
        for c in letters:
            three_grams.append(a+b+c)

two_gram_to_n = dict(zip(two_grams,range(26*26)))
three_gram_to_n = dict(zip(three_grams,range(26*26*26)))

def alphabetize(inText):
    """Make string lowercase, remove everything except letters"""
    outText=""
    inText=inText.lower() #Make lowercase
    for character in inText:
        if character in letters: outText+=character
       # elif character in digits: outText+=''
        else: outText+=" "
    return " ".join(outText.split())

def vectorize(string):
    """Take a string as input and return an array of integers corresponding to each character's value"""
    out=[char_to_n[char] for char in string]
    return np.array(out)

def stringify(vect):
    """Take an array of integer values and return corresponding string"""
    out=""
    for n in vect:
        out+=n_to_char[n]
    return out


#def rot(sentence, n=13):
#    tokens = []
#    for a in sentence:
#        old_token = char_to_n[a]
#        if old_token < 26: tokens += [(old_token + n) % 26]
#        else: tokens += [old_token]
#    cipher_text = "".join([n_to_char[a] for a in tokens])
#    return cipher_text  

def rot(sentence, n=13):
    """Apply a Caesar cypher to a string, shifting all letters by n (default is n=13)"""
    tokens = []
    for a in sentence:
        old_token = char_to_n[a]
        if old_token < 26: tokens += [(old_token + n) % 26]
        else: tokens += [old_token]
    return tokens  

def jumble(sentence, seed=0):
    """Generate a random substitution cipher and encode a string with it. Return the encrypted string and the list of characters that the plaintext was mapped to (i.e. [c,d,...] means 'a' was mapped to 'c', 'b' to 'd' etc.""" 
    random.seed(seed)
    target_characters = random.sample(letters,26)
    key = dict(zip(letters+['0'], target_characters+['0']))
    jumbled_sentence = "".join(key[char] for char in sentence)
    return jumbled_sentence, target_characters

def oh_to_word(vec):
    return stringify(np.array([np.argmax(a) for a in vec]))


def get_frequency_list(string):
    """Count the relative frequency of each character in a string"""
    tokenized_text = [char_to_n[a] for a in string]
    frequencies = [tokenized_text.count(a)/len(tokenized_text) for a in range(n_tokens)]
    return frequencies


def get_twogram_frequencies(string):
    """Count relative frequency of each 2-gram"""
    string_two_grams = [string[i:i+2] for i in range(len(string)-1)]
    tokenized_two_gram = [two_gram_to_n[char] for char in string_two_grams]
    frequencies = np.zeros(26*26)
    for token in tokenized_two_gram:
        frequencies[token]+= 1./len(tokenized_two_gram)
    return frequencies

def get_threegram_frequencies(string):
    """Count relative frequency of each 3-gram"""
    string_three_grams = [string[i:i+3] for i in range(len(string)-2)]
    tokenized_three_gram = [three_gram_to_n[char] for char in string_three_grams]
    frequencies = np.zeros(26*26*26)
    for token in tokenized_three_gram:
        frequencies[token]+= 1./len(tokenized_three_gram)
    return frequencies

def string_accuracy(string1, string2):
    """Evaluate how well string1 matches string 2. Return accuracy and list of characters in string1 that are wrong"""
    accuracy = np.sum(np.array(list(string1)) == np.array(list(string2)))/len(string1)
    wrong_characters = np.unique(np.array(list(string1))[np.where(np.array(list(string1)) != np.array(list(string2)))])
    return accuracy, wrong_characters