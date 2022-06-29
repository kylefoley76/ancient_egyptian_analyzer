import add_path
import time, os
from general import *
from global_hiero import *
from mine_tle import tle_entry
import hieroglyphs as hi
from googletrans import Translator as pytrans
from translate import Translator
from google.cloud import translate
from random import randint

class add_idioms:
    def __init__(self, txt=""):
        txt = hdir + 'grammar books/allen/allen_grammar.txt'
        self.txt = txt
        lst = to.from_txt2lst(self.txt)
        for x in lst:
            if x.startswith('%'):
                lst1 = x.split('|')
                idiom = lst1[0]
                meaning = lst[1]
                literal = lst[2]









class add_englishcl:
    def __init__(self, num, start=0, stop=0):
        txts = pi.open_pickle('tle_txts5', 'hi')
        english = to.from_txt2lst(hdir+f"tle_trans/{num}_english.txt")
        self.english = [x for x in english if reg(r'\S',x)]
        ger2eng = pi.open_pickle('ger2eng', 'hi')
        long_str = " ".join(self.english)
        lst = vgf.strip_n_split(long_str, "|")
        lst = lst[:-1]
        txt = txts[num]
        txt.english = lst
        # if start:
        #     for x in range(start):
        #         txt.english.insert(0, "")

        if not stop:
            stop = len(txt.german2)

        for e, x in en(txt.german2[start:stop]):
            if e > len(txt.english) -1:
                break

            p (x)
            str1 = vgf.limit_str_70(txt.english[e])
            ger2eng[x] = str1
            p (str1)
            p ("")

        str1 = input('return to save')
        if not str1:
            pi.save_pickle(ger2eng, 'ger2eng', 'hi')
            pi.save_pickle(txts, 'tle_txts5', 'hi')

        return










class translate_txt:
    def __init__(self, kind="korean"):
        texts = pi.open_pickle('tle_txts5', 'hi')
        # contents = pi.open_pickle('tle_categories', 'hi')
        self.kind = kind
        all_words = 0
        errors = 0
        self.get_translator()
        self.num = 0
        for e, x in en(list(texts.values())):
            if e > 7550:
                x.checked_french = False

        b = 0
        be_nice = 0
        for txt in texts.values():
            p (f'{b} of {len(texts.values())}')
            self.start = 0
            if not pi.open_pickle('bool1'):
                pi.save_pickle(texts, 'tle_txts5', 'hi')
                return
            # elif b > 7563:
            #     bb = 8

            elif b > 12509 and self.meets_conditions(txt):
                for self.word in txt.german2[self.start:]:
                    words = self.word.count(' ') + 1
                    be_nice += 1
                    if be_nice and be_nice % 40 == 0:
                        mm = randint(7,13)
                        p ('now sleeping')
                        time.sleep(mm)
                    all_words += words
                    try:
                        self.trans_word()
                        self.tword = vgf.limit_str_70(self.tword)
                        txt.translit2english.append(self.tword)
                        errors = 0
                    except:
                        p('error')
                        errors += 1
                        if errors > 4:
                            p ('now saving')
                            pi.save_pickle(texts, 'tle_txts5', 'hi')
                            return

                    time.sleep(2)
                    p(b, all_words)
                    self.num += 1

            b += 1



        pi.save_pickle(texts, 'tle_txts5', 'hi')

    def meets_conditions(self, txt):
        lst1 = txt.translit2english
        lst2 = txt.translit2german
        if all(x==y for x, y in zip(lst1, lst2)):
            # if not txt.checked_french:
            txt.checked_french = True
            for z in lst2:
                try:
                    lang = self.translator.detect(z)
                    self.num += 1
                    if self.num % 10 == 0:
                        tr = vgf.reset_tor()
                    if lang.lang == 'fr':
                        txt.translit2english = []
                        p (f'{z} is french')
                        return True
                except:
                    p ('failed to detech language')
                    return False

        return False

        # if not txt.translit2english:
        #     return True
        # if len(txt.translit2english) != len(txt.translit2german):
        #     self.start = len(txt.translit2german)
        #     return True

    def get_translator(self):
        if self.kind == 'google':
            self.use_google_trans()
        elif self.kind == 'azure':
            self.use_azure()
        elif self.kind == 'mymemory':
            self.use_mymemory()
        elif self.kind == 'korean':
            tr = vgf.reset_tor()
            self.translator = pytrans()





    def use_google_trans(self):
        str1 = hdir + 'My First Project-7a3577f30498.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str1
        self.translator = translate.Client()

    def use_mymemory(self):
        self.translator = Translator(provider='mymemory', from_lang='fr', to_lang="en",
                                     de='kylefoley202@hotmail.com')

    def use_korean(self):
        if self.num % 10 == 0:
            tr = vgf.reset_tor()
            self.translator = pytrans()


        try:
            eng = self.translator.translate(self.word, src='fr', dest='en')
        except:
            bb = 8
        x = eng.text
        self.tword = x.replace("&#39;", "'")
        p (self.tword)


    def trans_word(self):
        if reg(r'\w', self.word):
            if self.kind == 'google':
                eng = self.translator.translate(self.word, target_language='en', source_language='de')
                x = eng['translatedText']
                self.tword = x.replace("&#39;", "'")
            elif self.kind == 'mymemory':
                self.tword = self.translator.translate(self.word)
            elif self.kind == 'korean':
                self.use_korean()
        else:
            self.tword = self.word


def from_ger2eng(word):
    # word = 'was die Möde streng geteilt'
    translator = pytrans()
    eng = translator.translate(word, dest='en', src='de')

    print(eng.text)
    print('')
    print('possible translations:')
    for x in eng.extra_data["possible-translations"]:
        for z in x[2]:
            print(z[0])







args = vgf.get_arguments()



if 'ge' in args:
    if len(args) > 2:
        from_ger2eng(args[2])
    else:
        str1 = input('sentence: ')
        from_ger2eng(str1)

elif 'ae' in args:
    add_englishcl('842', 20)

elif 'tt' in args:
    translate_txt('korean')

elif 'pt2a' in args:
    prepare_txt2audio()

