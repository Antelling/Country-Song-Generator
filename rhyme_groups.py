import os, json, requests
import helpers

words = []

for file in os.listdir("data"):
    file = open(os.path.join("data", file), "r")
    for line in file:
        last_word = line.strip().split(' ')[-1]
        words.append(helpers.remove_punc(last_word))

print("last words found")

words = list(set(words))

groups = []

#so for every word, we loop through every group to see if it already exists
#if it does not, we make a new group with all the words

def get_data(word):
    print('requesting ' + word)
    url = "https://api.datamuse.com/words?rel_rhy=" + word
    good_words = []
    rhymed_words = json.loads(requests.get(url).text)
    for word in rhymed_words:
        word = word["word"]
        if word in words:
            good_words.append(word)
    print(good_words)
    return good_words



for word in words:
    for group in groups:
        if word in group:
            break
    else:
        groups.append(get_data(word))


helpers.write("records/rhyme_groups.json", json.dumps(groups))