# Country-Song-Generator

This procedurally generates country songs. The algorithm works like this:

1. Randomly choose a country song to use as a template. 
2. From every line of the song, extract three things.
  1. The amount of syllables
  2. If it is a duplicate
  3. The words it rhymes with
3. Loop over the extracted data, and generate new lines that fit the parameters using a reverse markov chain and a 
data file of ryhme groups. 

Although I think theres a bug with the rhyme groups or something because none of the generated songs rhyme much. 

---

There is also a file to determine which words have the highest difference in proportion between country songs and normal text. They
are:

1. yeah
2. baby
3. hey
4. daddy
5. love
