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
    a = cutoff
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r', encoding="utf-8") as doc:
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
            if(wordcount > 0):
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

        prob1 = (numfile1+smooth)/(numtotal+2)
        prob2 = (numfile2 + smooth) / (numtotal + 2)

        logprob[label_list[0]] = math.log(prob1)
        logprob[label_list[1]] = math.log(prob2)


    return logprob

#Needs modifications
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here
    total_word = 0

    word_prob[None] = 0


    for dic in training_data:

        for index0, i0 in enumerate(dic['bow']):
            if (list(dic['bow'])[index0] in word_prob):
                continue;
            word_prob[list(dic['bow'])[index0]] = 0
            #word_prob[None] = 0
        if(dic["label"] == label):
            for index, i in enumerate(dic["bow"]):
                if(list(dic['bow'])[index] in vocab):
                    if(list(dic['bow'])[index] in word_prob):

                        word_prob[list(dic['bow'])[index]] += dic["bow"][i]
                    else:
                        word_prob[list(dic['bow'])[index]] = dic["bow"][i]
                else:
                    if(None in word_prob):
                        word_prob[None] += dic["bow"][i]
                    else:
                        word_prob[None] = 0

                total_word += dic["bow"][i]
                #word_prob [None] = 5

    for h in word_prob:
        word_prob[h] = math.log((word_prob[h] + smooth*1)) - math.log((total_word + smooth*(len(vocab) +1)))


    return word_prob


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

    vocal = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocal, training_directory)
    log_prior = prior(load_training_data(label_list, training_directory), label_list)
    label_word2020 = p_word_given_label(vocal,training_data, label_list[1])
    label_word2016 = p_word_given_label(vocal, training_data, label_list[0])
    retval['vocabulary'] = vocal
    retval['log prior'] = log_prior
    retval['log p(w|y=2016)'] = label_word2016
    retval['log p(w|y=2020)'] = label_word2020

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


    vocab_x = model['vocabulary']
    prob_word_2016_total = 0
    prob_word_2020_total = 0

    bow_doc = create_bow(vocab_x,filepath)

    for i in bow_doc:
        prob_word_2016_total += model['log p(w|y=2016)'][i] * bow_doc[i]
        prob_word_2020_total += model['log p(w|y=2020)'][i] * bow_doc[i]


    label_2016 = model['log prior']['2016'] + prob_word_2016_total
    label_2020 = model['log prior']['2020'] + prob_word_2020_total

    if label_2016 > label_2020:
        label_x = '2016'

    else:
        label_x = '2020'

    retval['predicted y'] = label_x
    retval['log p(y=2016|x)'] = label_2016
    retval['log p(y=2020|x)'] = label_2020



    return retval

if __name__ == '__main__':
    vocab = {}
    #vocab = create_vocabulary('./EasyFiles/', 2)
    #print(vocab)
    #print(create_bow(vocab, './EasyFiles/2016/1.txt'))
    #vocab = create_vocabulary('./corpus/training/', 2)
    #training_data = load_training_data(vocab,'./corpus/training/')
    #print(training_data)
    #vocab = create_vocabulary('./corpus/training/', 2)
    #training_data = load_training_data(vocab, './corpus/training/')
    #print(prior(training_data, ['2020', '2016']))
    #vocab = create_vocabulary('./EasyFiles/', 1)
    #load_data = load_training_data(vocab, './EasyFiles/')
    #print(load_data)
    #for x in load_data:
     #   for key in x["bow"]:
     #      print(x['bow'][key])
    #vocab = create_vocabulary('./EasyFiles/', 1)
    #training_data = load_training_data(vocab, './EasyFiles/')
    #print(training_data)
    #print(p_word_given_label(vocab, training_data, '2016'))
    #print(train('./EasyFiles/', 2))
    #model = train('./corpus/test/', 2)
    #print(classify(model, './corpus/test/2016/0.txt'))

    #vocab = create_vocabulary('./EasyFiles/', 1)
    #print(create_bow(vocab, './EasyFiles/2016/1.txt'))

    #vocab = create_vocabulary('./EasyFiles/', 1)
    #print(load_training_data(vocab, './EasyFiles/'))

    #vocab = create_vocabulary('./corpus/training/', 2)
    #training_data = load_training_data(vocab, './corpus/training/')
    #print(prior(training_data, ['2020', '2016']))

    #vocab = create_vocabulary('./EasyFiles/', 1)
    #training_data = load_training_data(vocab, './EasyFiles/')
    #print(training_data)
    #print(p_word_given_label(vocab, training_data, '2016'))
    #print(p_word_given_label(vocab, training_data, '2020'))

    #print(train('./EasyFiles/', 2))
####
    #print(create_vocabulary('./EasyFiles/', 2))

    #vocab = create_vocabulary('./EasyFiles/', 2)
    #print(create_bow(vocab, './EasyFiles/2016/1.txt'))

    #vocab = create_vocabulary('./EasyFiles/', 1)
    #print(load_training_data(vocab, './EasyFiles/'))

    #vocab = create_vocabulary('./corpus/training/', 2)
    #training_data = load_training_data(vocab, './corpus/training/')
    #print(prior(training_data, ['2020', '2016']))

    #vocab = create_vocabulary('./EasyFiles/', 1)
    #training_data = load_training_data(vocab, './EasyFiles/')
    #print(p_word_given_label(vocab, training_data, '2016'))

    #vocab = create_vocabulary('./EasyFiles/', 2)
    #training_data = load_training_data(vocab, './EasyFiles/')
    #print(p_word_given_label(vocab, training_data, '2016'))

    #print(train('./EasyFiles/', 2))

    model = train('./corpus/training/', 2)
    print(classify(model, './corpus/test/2016/0.txt'))





