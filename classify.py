import os
import math


#These first two functions require os operations and so are completed for you
#Completed for you
def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

#Completed for you
def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    global a
    a = cutoff
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r', encoding="utf-8") as doc:
                #encoding = "utf-8"
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

#The rest of the functions need modifications ------------------------------
#Needs modifications
def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    wordcount = 0
    wordcountnone = 0
    c = 0
    for i in vocab:
        c+=1
        with open(filepath, 'r', encoding="utf-8") as doc: ###############################################
            for word in doc:
                word = word.strip()
                if(c==1):
                    if (word not in vocab):
                        wordcountnone += 1
                if(i == str(word)):
                    wordcount += 1
                #print(wordcount)
            if(wordcount >= a):
                bow[i] = wordcount
        wordcount = 0
    if(wordcountnone != 0):
        bow[None] = wordcountnone
    return bow


#Needs modifications
def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    # TODO: add your code here
    numfile1 = 0
    numfile2 = 0
    for dic in training_data:
        if(dic["label"] == label_list[0]):
            numfile1 += 1
        elif(dic["label"] == label_list[1]):
            numfile2 += 1
        numtotal = numfile1 + numfile2

        prob1 = (numfile1+1)/(numtotal+2)
        prob2 = (numfile2 + 1) / (numtotal + 2)

        logprob[label_list[0]] = math.log(prob1)
        logprob[label_list[1]] = math.log(prob2)


    return logprob

#Needs modifications
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here

    return word_prob


##################################################################################
#Needs modifications
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = os.listdir(training_directory)
    # TODO: add your code here


    return retval

#Needs modifications
def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    # TODO: add your code here


    return retval

if __name__ == '__main__':
    vocab = {}
    #vocab = create_vocabulary('./EasyFiles/', 2)
    #print(vocab)
    #print(create_bow(vocab, './EasyFiles/2016/1.txt'))
    #vocab = create_vocabulary('./corpus/training/', 2)
    #training_data = load_training_data(vocab,'./corpus/training/')
    #print(training_data)
    vocab = create_vocabulary('./corpus/training/', 2)
    training_data = load_training_data(vocab, './corpus/training/')
    print(prior(training_data, ['2020', '2016']))

