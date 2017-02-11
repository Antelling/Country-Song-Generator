import os

for file in os.listdir("data"):
    f = open(os.path.join("data", file), "r")
    data = f.read()
    data = data.replace(" ", "")
    f = open(os.path.join("data", file), "w")
    f.write(data)
    f.close()
