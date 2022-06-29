
# from translate import Translator
import sys


hdir = "/users/kylefoley/downloads/egyptian/"
fdir = '/Users/kylefoley/PycharmProjects/inference_engine2/inference2/proofs/hieroglyphs/'
fcdir = fdir + 'flash_cards/'
hdirp = fdir + 'hi_pickles/'
sdir = "/applications/JSesh-7.3.2/jsesh_texts"

# dotted h

h2 = chr(7717)  # 'ḥ'
A2 = chr(42786)
t2 = chr(7791)
a2 = chr(42789)
h3 = chr(7723)
h4 = chr(7830)
d2 = chr(7695)
s2 = chr(353)

#  ś = chr(347)


codage = {
    "H": h2,
    "A": A2,
    "T": t2,
    "a": a2,
    'x': h3,
    'X': h4,
    "D": d2,
    "S": s2
}

re_codage = {v: k for k, v in codage.items()}

def is_prep(pos, word, lemma):
    exceptions = {79800}


    if word in ['r', 'n','m','Hr','xr','Xr','jm',
                'xtf']:
        return True
    if not pos:
        return False

    if pos[0] in ['i','e'] or lemma in exceptions:
        return True
