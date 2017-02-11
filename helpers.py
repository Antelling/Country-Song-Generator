import nltk
from nltk.corpus import cmudict


def _rhyme(inp, level):
    entries = cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)


def doTheyRhyme(word1, word2):
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1):
        return False

    return word1 in _rhyme(word2, 1)

_d = cmudict.dict()
def syllables(text):
    words = nltk.word_tokenize(text)
    total = 0
    for word in words:
        try:
            total += [len(list(y for y in x if y[-1].isdigit())) for x in _d[word.lower()]][0]
        except KeyError:
            total += _fallback(word)
        except IndexError:
            return 1
    return total

def _fallback(word):
    try:
        count = 0
        vowels = 'aeiouy'
        word = word.lower().strip(".:;?!")
        if word[0] in vowels:
            count +=1
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        if word.endswith('e'):
            count -= 1
        if word.endswith('le'):
            count+=1
        if count == 0:
            count +=1
        return count
    except IndexError:
        return 1

def remove_punc(string):
    newstring = ""
    for letter in string:
        if letter in list("abcdefghijklmnopqrstuvwxyz -'"):
            newstring += letter
    return newstring

def write(name, data):
    f = open(name, "w")
    f.write(data)
    f.close()

def get_set_item(set):
    for i in set:
        return i

def format_lyrics(song):
    song = song.split("\n")
    new_song = ""
    for line in song:
        line = _fix_capitals(line)
        line = _fix_quotes(line)
        line = _fix_spacing(line)

        new_song += line + "\n"
    return new_song

def _fix_capitals(line):
    line = nltk.word_tokenize(line)
    line = nltk.pos_tag(line)
    new_line = []
    for word_tuple in line:
        if word_tuple[1] == "NNP":
            new_line.append(word_tuple[0])
        else:
            new_line.append(word_tuple[0].lower())
    return " ".join(new_line)

def _fix_quotes(line):
    num = line.count('"')
    if num % 2 == 1:
        line += '"'
    return line

def _fix_spacing(line):
    punc = ["?", '.', ',', '!', "'", "n't", ":"]
    for p in punc:
        line = line.replace(" " + p, "")
    return line
