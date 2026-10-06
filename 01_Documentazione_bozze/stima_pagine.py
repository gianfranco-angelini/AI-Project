import math

def stima_pagine(contenuto, prima=3, righe_pag=46.0):
    def r_testo(t, larg):
        cpl = max(10, larg / 9060.0 * 105)
        return max(1, math.ceil(len(t) / cpl))
    pos, pag, out = 0.0, prima, {}
    for it in contenuto:
        t = it[0]
        if t == "h":
            add = 3.0 if it[1] == 1 else 2.2
            if pos + add + 3 > righe_pag:
                pag, pos = pag + 1, 0.0
            out[it[2]] = pag
        elif t == "p":
            add = r_testo(it[1], 9060) + 0.8
        elif t == "bullets":
            add = sum(r_testo(b, 8600) + 0.4 for b in it[1])
        elif t == "table":
            cols = it[1]
            add = 1.3 + sum(max(r_testo(c, w) for c, w in zip(row, cols)) * 0.9 + 0.4 for row in it[3])
        elif t == "box":
            add = 1.5 + sum(r_testo(x, 8800) * 0.9 for x in it[3])
        elif t == "steps":
            add = sum(max(1.6, sum(r_testo(d, 6060) * 0.9 for d in ds)) + 0.5 for _, ds in it[1])
        elif t == "code":
            add = len(it[1]) * 0.9 + 1
        pos += add
        while pos > righe_pag:
            pag, pos = pag + 1, pos - righe_pag
    return out
