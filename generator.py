URL = "https://vimm.net/vault/"

start = 63500
finish = 65500

links = [f"{URL}{i}\n" for i in range(start, finish)]

with open("links.txt", "w") as f:
    f.writelines(links)
