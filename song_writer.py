import random, os, helpers, json, reverse_markov_chain

#region setup

file = random.choice(os.listdir("data"))
print(file)

file = open(os.path.join("data", file))

created = []

rhyme_group = 0
line_id = 0
used_rhyme_groups = {}

rhyme_groups = json.loads(open("records/rhyme_groups.json").read())

for line in file:
    if helpers.remove_punc(line).strip() == "":
        continue
    # we need to do three things here
    # one, record the syllable amounts
    # two, record the "hash" of the line, so like lines are like in our generated file
    # three, record the rhyme group of the last word

    # region syllables - good
    syllables = helpers.syllables(line)
    # endregion syllables

    # region line id - good
    modified = helpers.remove_punc(line.lower().strip())
    this_line_id = 0

    for prev_line in created:
        if prev_line[3] == modified:
            this_line_id = prev_line[1]
            break
    else:
        this_line_id = line_id + 1
        line_id = this_line_id
    # endregion

    # region rhyme groups - bad

    last_word = line.split(" ").pop().strip()

    this_rhyme_group = 0
    for group in used_rhyme_groups:
        if last_word in used_rhyme_groups[group]:
            this_rhyme_group = group
            break
    else:
        rhyme_group+=1
        this_rhyme_group = rhyme_group
        new_rhyme_group = {}
        for group in rhyme_groups:
            if last_word in group:
                used_rhyme_groups[rhyme_group] = group
                break
        else:
            used_rhyme_groups[rhyme_group] = {}


    #endregion

    created.append([syllables, this_line_id, this_rhyme_group, modified])

helpers.write("records/summary.json", json.dumps(created, indent=2))

#endregion

#region generation

#we need to record the frequency of each rhyme group
used_rhyme_groups_freq = {}
for line in created:
    group = line[2]
    if group in used_rhyme_groups_freq:
        used_rhyme_groups_freq[group]+=1
    else:
        used_rhyme_groups_freq[group] = 1

#we now use the frequency to choose a possible rhyme group for each used rhyme group
#god I suck at naming
already_used_groups = []
for group in used_rhyme_groups_freq:
    while True:
        possible_index = random.choice(range(len(rhyme_groups)))
        possible_len = len(rhyme_groups[possible_index])
        if possible_len >= used_rhyme_groups_freq[group]:
            used_rhyme_groups_freq[group] = rhyme_groups[possible_index]
            break

#okay now we give it a sane name
rhyme_group_map = used_rhyme_groups_freq

#okay, now we use our reverse_markov_chain.py to generate lines for each of the seed lines
song = []
used_rhyme_groups = {}
for line in created:
    if len(line) < 4:
        continue
    syllables = line[0]
    id = line[1]
    rhyme_group = line[2]

    #deal with id
    for lyric in song:
        if lyric[1] == id:
            song.append([lyric[0], lyric[1]])
            break
    else:
        #okay cool
        #now we need a seed and the syllables
        seed = random.choice(rhyme_group_map[rhyme_group])
        song.append([reverse_markov_chain.gen(seed, syllables), id])

text_song = ""
for line in song:
    text_song+= line[0] + "\n"

helpers.write("records/created_song.txt", helpers.format_lyrics(text_song))

#endregion

