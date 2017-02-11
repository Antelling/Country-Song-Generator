from bs4 import BeautifulSoup
import requests

i = 0

def write(name, data):
    f = open(name, "w")
    f.write(data)
    f.close()

url_base = "http://www.anycountrymusiclyrics.com/artist/"
for letter in "abcdefghijklmnopqrstuvwxyz":
    print(letter)
    url = url_base + letter
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find("table", {"width": "90%"}).findAll('a')
    for link in links:
        url = link["href"]
        print("    " + url)
        subpage = BeautifulSoup(requests.get(url).text, "html.parser")
        song_links = subpage.findAll("a")
        del song_links[0:33]
        for song_url in song_links:
            song_url = song_url["href"]
            print("        " + song_url)
            song_page = BeautifulSoup(requests.get(song_url).text, "html.parser")
            paras = song_page.findAll(["p", "font"])
            del paras[0:45]
            del paras[-7:]

            lyrics = ""

            for para in paras:
                para = para.get_text() \
                    .replace("<br/>", "\\n") \
                    .replace("<br>", "\\n") \
                    .replace("</br>", "\\\n") \
                    .replace("<p>", " ") \
                    .replace("</p>", " ")
                lyrics += " " + para

            i+=1
            write("data/" + str(i), lyrics)