import nltk
import os
import json

stopwords = json.loads(open("stopwords.json").read())


# okay, now we loop over all our data and if it isn't a stop word load it into our model
p_model = {}
allwords = 0


def remove_punc(string):
    newstring = ""
    for letter in string:
        if letter in list("abcdefghijklmnopqrstuvwxyz -'"):
            newstring += letter
    return newstring


for file in os.listdir("data"):
    try:
        file = open(os.path.join("data", file), "r")
        for line in file:
            line = nltk.word_tokenize(line)
            line = nltk.pos_tag(line)
            for tuple in line:
                word = remove_punc(tuple[0].lower())
                if not word in stopwords and tuple[1][0] == "N":
                    allwords += 1
                    try:
                        if p_model[word] > 0:
                            p_model[word] += 1
                    except KeyError:
                        p_model[word] = 1
    except:
        print("error reading" + str(file))

file = open("records/freq.json", "w")
file.write(json.dumps(p_model))
file.close()

# okay, now we need to do the same for the brown corpus
# this is going to be huge
brown_p_model = {}
brown_allwords = 0
brown_sentences = " ".join(nltk.corpus.brown.words()).split(".")
for line in brown_sentences:
    line = nltk.word_tokenize(line)
    line = nltk.pos_tag(line)
    for tuple in line:
        word = remove_punc(tuple[0].lower())
        if not word in stopwords and tuple[1][0] == "N":
            brown_allwords += 1
            try:
                if brown_p_model[word] > 0:
                    brown_p_model[word] += 1
            except KeyError:
                brown_p_model[word] = 1

# wew okay, now we need to find the true difference in proportion for all of these
most_country_model = []

def is_statistically_significant(diff, n, p):
    pass

for word in p_model:
    try:
        if p_model[word] > 5 and brown_p_model[word] > 5:
            observed = p_model[word]/allwords
            expected = brown_p_model[word]/brown_allwords
            diff = ((observed - expected) * (observed - expected))/expected
            smaller_n = observed if observed < expected else expected
            if is_statistically_significant(diff, n=smaller_n, p=.05):
                if observed < expected:
                    diff = -diff

                most_country_model.append([word, diff])
    except KeyError:
        pass
    except ZeroDivisionError:
        pass


def cmp(list):
    return -list[1]


most_country_model.sort(key=cmp)


def write(name, data):
    f = open(name, "w")
    f.write(data)
    f.close()


write("records/words.json", json.dumps(most_country_model, indent=2))
