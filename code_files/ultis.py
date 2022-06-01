import re
import numpy as np

def prefix_neg(words):
    '''
    :param words: a list of words to process.
    :return: a list of words with the 'neg_' suffix.
    This function receives a list of words and appends a 'neg_' suffix to every word following a negation (no, not, nor)
    and up to the next punctuation mark (., !, ?). For example:
    ['not', 'complex', 'example', '.', 'could', 'not', 'simpler', '!']
    ->
    ['not', 'neg_complex', 'neg_example', '.', 'could', 'not', 'neg_simpler', '!']
    TODO
    Implement prefix_neg
    HINT: you might find the statment 'continue' useful in your implementation, althought it is not neceessary.
    [15 points]
    '''
    after_neg = False
    proc_words = []
    nono_words = ['no','not','nor']
    stap_words = ['!', '?', '.']
    for word in words:
        if after_neg:
            word = r'neg_'+word
        proc_words.append(word)
        if word in nono_words:
            after_neg = True
            continue
        if word in stap_words:
            after_neg = False
    return proc_words

def filter_voc(words, voc):
    mask = np.ma.masked_array(words, ~np.in1d(words, voc))
    return mask[~mask.mask].data

def proc_text(text):
    '''
        This function takes as input a non processed string and returns a list
        with the clean words.
        :param text: The text to be processed
        :param sw: A list of stop words
        :return: a list containing the words of the clean text.
        TODO
        Implement the following transformations:
        1.- Set the text to lowercase.
        2.- Make explicit negations:
              - don't -> do not
              - shouldn't -> should not
              - can't -> ca not (it's ok to leave 'ca' like that making it otherwise will need extra fine tunning)
        3.- Clean html and non characters (except for '.', '?' and '!')
        4.- Add spacing between punctuation and letters, for example:
                - .hello -> . hello
                - goodbye. -> goodbye
        5.- Truncaters punctuation and characters with multiple repetitions into three repetitions.
            Punctuation marks are consider 'multiple' with at least **two** consecutive instances: ??, !!, ..
            Characters are considre 'multiple' with at least **three**  consecutive instances: goood, baaad.
            for example:
                - very gooooooood! -> very goood
                - awesome !!!!!! -> awesome !!!
                - nooooooo !!!!!! -> nooo !!!
                - how are you ?? -> how are you ???
            NOTE: Think about the logic behind this transformation.
        6.- Remove whitespace from start and end of string
        7.- Return a list with the clean words after removing stopwords (DO NOT REMOVE NEGATIONS!) and
            **character** (letters) strings of length 2 or less. for example:
               - ll, ss
        8.- Removes any single letter: 'z', 'w', 'b', ...
    This is the most important function and the only one that will include a test case:
    input = 'this...... .is a!! .somewhat??????,, # % & messy 234234 astring... noooo.asd HELLLLOOOOOO!!! what is thiiiiiiissssss?? <an> <HTML/> <tag>tagg</tag>final. test! z z w w y y t t'
    expected_output = ['...', '.', '!!!', '.', 'somewhat', '???', 'messy', 'astring', '...', 'nooo', '.', 'asd', 'helllooo', '!!!', 'thiiisss', '???', 'tagg', 'final', '.', 'test', '!']
    [40 points]
    '''

    trans1 = str(text).lower()
    
    # trans3 Clean html and non characters (except for '.', '?' and '!')
    trans3 = re.sub(re.compile('<.*?>') , ' ', trans1)
    trans3 = trans3.replace("#","").replace("&","and").replace("%", "").replace(",","")
    trans3.strip()
    trans3 = re.sub(r'[0-9]*',"",trans3)
    
    # trans4 Add spacing between punctuation and letters
    #trans4 = trans3b.replace(". "," . ").replace("."," . ").replace("!"," ! ")
    trans4 = re.sub(r'([.,!?()])([a-z])', r'\1 \2', trans3)
    trans4 = re.sub(r'([a-z])([.,!?()])', r'\1 \2', trans4)
    
    # trans5 Truncate
    trans5 = re.sub(r'(!)\1+','!!!', trans4)
    trans5 = re.sub(r'\?{2,}','???', trans5)
    trans5 = re.sub(r'\.\.\.{2,}','...', trans5)
    trans5 = re.sub(r'([a-z])\1\1+',r'\1\1\1', trans5)
    
    # trans8 Remove single letters
    trans8 = re.sub(r'(?<![\w])(?:[a-zA-Z0-9](?: |$))', ' ', trans5)        
    words = trans8.split()
    
    return words

def connotation(text):
    text_file1 = open("positive_words.txt", "r")
    text_file2 = open("negative_words.txt", "r")
    pos_words = text_file1.read().split()
    neg_words = text_file2.read().split()
    text_as_list = proc_text(text)
    # positive = num_conn[0] , negative = num_conn[1]
    num_conn = [0,0]
    for pw in pos_words:
        num_conn[0] += list(text_as_list).count(pw)
    for nw in neg_words:
        num_conn[1] += list(text_as_list).count(nw)
    if num_conn[0] > num_conn[1]:
        con_final = 'positive'
    elif num_conn[0] < num_conn[1]:
        con_final = 'negative'
    else:
        con_final = 'informative'
    return [num_conn[0],num_conn[1],con_final]
