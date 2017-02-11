#okay so nltk used to have these nice ngram and generate methods
#but they were deleted due to bugs or something
#so we get to do this by hand

import nltk
import json, random, os

chain = {}
data = ""
for file in os.listdir("data"):
    file = open(os.path.join("data", file), "r")
    for line in file:
        data += "\n " + line.strip()

data = data.split(" ")

prev_words = []

def record(hist, word):
    hist = hist[0] + "|" + hist[1]
    if hist in chain:
        if word in chain[hist]:
            chain[hist][word]+=1
        else:
            chain[hist][word] = 1
    else:
        chain[hist] = {}
        chain[hist][word] = 1

for word in data:
    if len(prev_words) == 2:
        record(prev_words, word)
        prev_words[0] = prev_words[1]
        prev_words[1] = word
    else:
        prev_words.append(word)

def write(name, data):
    f = open(name, "w")
    f.write(data)
    f.close()


#okay, now we have the model
#we pick a random key to start with, then just go for like 5000 words
generated = ""
words = random.choice(list(chain.keys())).split("|")
for i in range(5000):
    try:
        options = chain["|".join(words)]
        totally_nasty_hack_list = []
        for word in options:
            if bool(word):
                totally_nasty_hack_list = totally_nasty_hack_list + (options[word] * [word])
        next_word = random.choice(totally_nasty_hack_list)
        generated += " " + next_word
        words[0] = str(words[1])
        words[1] = next_word
    except IndexError:
        #I think python droppod some of our data or something
        words = random.choice(list(chain.keys())).split("|") #lets just reset

write("records/generated.txt", generated)