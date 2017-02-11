# exactly like markov_chain.py except it allows you to specify a key word, and it works backwards kind of

import random, os, json, helpers

#region data prep
chain = {}
if "reverse_markov_data.json" in os.listdir("records"):
    chain = json.loads(open("records/reverse_markov_data.json").read())
else:
    data = ""
    for file in os.listdir("data"):
        file = open(os.path.join("data", file), "r")
        for line in file:
            data += "\n " + line.strip()

    data = data.replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("\n", "").split(" ")
    data.reverse()

    word_1 = data[0]
    word_2 = data[1]
    del data[0:1]

    for word in data:
        if word_1 in chain:
            if word_2 in chain[word_1]:
                if word in chain[word_1][word_2]:
                    chain[word_1][word_2][word] += 1
                else:
                    chain[word_1][word_2][word] = 1
            else:
                chain[word_1][word_2] = {}
                chain[word_1][word_2][word] = 1
        else:
            chain[word_1] = {}
            chain[word_1][word_2] = {}
            chain[word_1][word_2][word] = 1
        word_1 = word_2
        word_2 = word

    def write(name, data):
        f = open(name, "w")
        f.write(data)
        f.close()

    write("records/reverse_markov_data.json", json.dumps(chain, indent=2))

#endregion

#region gen function

def gen(seed, syllables):
    used_words = [seed]

    tries = 0
    total_tries = 0
    while helpers.syllables(helpers.remove_punc(" ".join(used_words))) != syllables:
        total_tries += 1
        if total_tries > 50:
            #apparently we are unable to create a viable chain with this data
            #eh, screw it
            return " ".join(used_words)

        if helpers.syllables(helpers.remove_punc(" ".join(used_words))) > syllables:
            used_words.pop()
            if tries > 5:
                used_words.pop()
            tries += 1
        else:
            tries = 0
            if len(used_words) < 2:
                if(len(used_words) == 0):
                    #we bail a lot in this program
                    return ""
                for i in list(range(len(used_words[0]))):
                    try:
                        word_key = used_words[i]
                    except IndexError:
                        #I don't know why this is happening
                        #let's bail
                        return " ".join(used_words)
                    if word_key in chain:
                        options = chain[word_key]
                        break
                else:
                    #lets just bail on this line, I guess
                    #I don't know whats happening
                    return " ".join(used_words)
                keys = options.keys()
                list_keys =(list(keys))
                choice = random.choice(list_keys)
                used_words.append(choice)
            else:
                options = chain[used_words[-2]][used_words[-1]]
                array = []
                for option in options:
                    array = array + (options[option] * [option])
                used_words.append(random.choice(array))

    used_words.reverse()
    return " ".join(used_words)

#endregion
