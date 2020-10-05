import pandas as pd
import numpy as np
from joblib import Parallel, delayed






with open("C:\\Users\\user\\Desktop\\a\\d_tough_choices.txt", "r", encoding='utf-8') as file:
    f = file.read().split("\n")
    books_sent = {}
    libraries = []
    books = {}
    first = f[0].split(" ")
    n_books = first[0] 
    second = f[1].split(" ")
    for b in range(len(second)):
        books[b] = second[b]
        books_sent[b]= False
    days = int(first[2])
    scores = f[1].split(" ")
    a = 0
    for i in range(2, len(f), 2):
        lib_first = f[i].split(" ")
        lib_sum = 0
        for book in f[i+1].split(" "):
            lib_sum = lib_sum + int(books[int(book)])
        # if int(float(lib_first[1])) < 60 and int(float(lib_first[0])) > 800:

        libraries.append({'name':a, 
                        'n_books':int(float(lib_first[0])), 
                        'signup':int(float(lib_first[1])), 
                        'ship':int(float(lib_first[2])), 
                        'books':f[i+1].split(" "),
                        "score": lib_sum
                        })
        l = libraries[-1]
        b = [ [e, int(books[int(e)])] for e in l["books"]]
        b.sort(key=lambda t: t[1], reverse=True)
        l["books"]= [i[0] for i in b]
        a = a+1
    libraries.sort(key=lambda t: t["n_books"], reverse=True)

print(len(libraries))



def s(l):
    b = [ [e, int(books[int(e)])] for e in l["books"] if books_sent[int(e)] == False]
    b.sort(key=lambda t: t[1], reverse=True)
    l["books"]= [i[0] for i in b]
    lib_sum = 0
    for book in l["books"]:
        lib_sum = lib_sum + int(books[int(book)])
    l['score'] = lib_sum
    l['n_books'] = len(l["books"])
    


def sorta():
    Parallel(n_jobs=16)(delayed(s)(l) for l in libraries)
    libraries.sort(key=lambda t: t["n_books"], reverse=True)

from progress.bar import Bar


out = [str(len(libraries))]
d = 0
n = 0

while d < days and n < len(libraries):
    if d + libraries[n]["signup"] > days:
        break
    d = d + libraries[n]["signup"]
    n = n + 1
d = 0
out = [str(n)]

print("inizio")
bar = Bar('Processing', max=n)
for num_lib in range(n):
    r = []
    d = d + libraries[num_lib]["signup"]
    giorni_restanti = days-d
    libri_inviabili = giorni_restanti * libraries[num_lib]["ship"]
    libri_inviati = 0
    i = 0
    while i < libraries[num_lib]["n_books"] and libri_inviati <= libri_inviabili:
        ships = libraries[num_lib]["ship"]
        consegnati = 0
        while consegnati < ships and i < libraries[num_lib]["n_books"]:
            if books_sent[int(libraries[num_lib]["books"][i])] == False:
                books_sent[int(libraries[num_lib]["books"][i])] = True
                r.append(libraries[num_lib]["books"][i])
                consegnati = consegnati + 1
                libri_inviati = libri_inviati + 1
            i = i + 1
    out.append(" ".join([str(libraries[num_lib]["name"]), str(len(r))]))
    out.append(" ".join(r))
    sorta()
    bar.next()
bar.finish()
    
out = "\n".join(out)
    

with open("C:\\Users\\user\\Desktop\\a\\b_res.txt", "w+", encoding='utf-8') as file:
    file.write(out)