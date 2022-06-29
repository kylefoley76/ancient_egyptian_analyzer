import add_path
from general import *
import random
from global_hiero import *
from mine_tle import tle_entry
import hieroglyphs as hi
from hieroglyphs import vocab_tester, temp_word, print_entries, other_tests
from collections import deque


class classify_words:
    def __init__(self):
        self.tle_dct = pi.open_pickle("tle_dct6", 'hi')

    def is_unknown(self):
        if reg(r'^-\.+-$', self.word):
            self.unknown.append(self.word)



def split_infixes(words_in_sent, rejoin=False):
    e = 0
    while e < len(words_in_sent):
        word = words_in_sent[e]

        word = re.sub(r'[\(\)]', "", word)
        if "-" in word and "." in word:
            idx1 = word.rindex('-')
            idx2 = word.rindex('.')
            if idx1 < idx2:
                pre_word = word[:idx1]
                pre_word = pre_word.replace('.', ',')
                post_word = word[idx1:]
                word = pre_word + post_word

        if word.startswith('j.'):
            stem = word[2:]
            words_in_sent[e] = 'j.'
            e += 1
            words_in_sent.insert(e, stem)
        elif '.' in word:
            lst = word.split('.')
            lst[0] = lst[0].replace(',', '.')

            words_in_sent[e] = lst[0]
            e += 1
            for x in lst[1:]:
                words_in_sent.insert(e, "." + x)
                e += 1
        else:
            e += 1

    if not rejoin:
        return ' '.join(words_in_sent)
    else:
        return words_in_sent


def get_new_mil_lem(dct_cls, tle_dct, w2a):
    for x, y in tle_dct.items():
        if int(y.lemma_no) > 999_999:
            w2a.append(y.word)
    return


def add_lemmas2vocab():
    dct_cls = pi.open_pickle('dictionary', 'hi')
    tle_dct = pi.open_pickle('tle_dct6', 'hi')
    pro_spell = hi.get_pro_spell(tle_dct)
    redun_tle = pi.open_pickle("redun_tle", 'hi')

    for word, lemmas in pro_spell.items():
        full_def = []
        for lemma in lemmas:
            lemma = redun_tle.get(lemma, lemma)
            entry = tle_dct[lemma]
            pos = entry.pos
            eng = entry.eng_word
            lst1 = [lemma, pos, entry.rank, eng]
            full_def.append(lst1)
        ins = tle_entry()
        ins.word = word
        ins.eng_word = full_def
        ins.lemma_no = lemmas

        ins.nxt_tst = time.time()
        dct_cls[word] = ins

    pi.save_pickle(dct_cls, 'dictionary', 'hi')
    return


def reduce2root2(word, sentence, dct_cls):
    suff_dct2 = {
        'wt': ['wt', 't', ''],
        'ww': ['w'],
        'tjt': ['t'],
        'yt': ['t'],
        'j': ['j', ''],
        'tj': ['tj'],
        't': ['t', ''],
        'w': ['w', ''],
        'wj': ['w', ''],
        'f': [''],
        's': [''],
        'n': [''],
        'sn': [''],
        'st': [''],
        'k': [''],
        'T': [''],
        'Tn': [''],
        'tn': [''],
        'kw': ['']

    }

    lst = word.split('-')
    for non_com in lst:
        if '.' in lst1:
            lst1 = non_com.split('.')
            suffixes = lst1[1:]
            candidates = [lst1[0]]
            candidates = list(candidates)
            lst1 = []
            for lsuffix in suffixes:
                lst1 = suff_dct2[lsuffix]
                if len(lst1) == 1:
                    if not lst1[0]:
                        pass
                    else:
                        for candidate in candidates:
                            candidate.append(lst1[0])
                else:

                    for suffix in lst:
                        if not suffix:
                            pass
                        else:
                            b = len(suffix)
                            for c in range(b):
                                new_cand = jsonc(candidates)


def fix_test_sents():
    test_sents = pi.open_pickle('test_sentences', 'hi')
    all_words = set()
    delete_dot = set()
    for cls in test_sents.values():
        lst = cls.word.split()
        all_words |= set(lst)

    lst = [re.sub(r'[\(\)]', "", x) for x in all_words if '.' in x]
    one_dot = [x for x in lst if x.count('.') == 1]
    pl_dot = [x for x in lst if x.count('.') > 1]

    for e, x in en(all_words):
        p(f'{e} of {len(all_words)}')
        p(x)
        str1 = input('remove dot return for no: ')
        if str1:
            x.add(delete_dot)

    to.from_lst2txt(delete_dot, fcdir + 'delete_dot')


class add2vocab:
    def main(self, **kwargs):

        self.word = kwargs['word']
        self.tle_dct = kwargs['tle_dct']
        self.dictionary = kwargs['dictionary']
        self.sentence = kwargs['sentence']

        self.mistake = True
        while True:
            p(f"""
            begin with 1 to go back into root, 
            2 to not go back in
            4 to add new lemma
            5 to replace compound with 2 words
            """)
            self.word = input('spell again, n to move to next sent: ')
            while True:
                if self.word[0] not in ['1', '2', '3', '4', '5', 'n']:
                    self.word = input('wrong input')
                else:
                    break

            if self.word == 'n':
                self.next_sent = True
                break

            elif self.word[0] == '1':
                self.word = self.word[2:]
                str3 = self.word
                self.word = self.reduce2root(self.word)
                if self.word in self.dictionary:
                    return self.word
                else:
                    p(f'{self.word} is not in your dictionary')


            elif self.word[0] == '2':
                self.word = self.word[2:]
                if self.word in self.dictionary:
                    return self.word
                else:
                    p(f'{self.word} is not in your dictionary')

            elif self.word[0] == '4':
                self.handle_new_meanings()
                break

            elif self.word[0] == '5':
                return self.word[2:]

    def chop_off_suffix(self):
        pass

    def get_posssibilities(self):
        special_suffixes = ['wt', 't', 'ww', 'w', ]

    def reduce2root(self, word):
        suff_dct = {
            "wt": 't',
            "ww": "w",
            "tjt": "t",
            'yt': 't'
        }

        repl_w_blank = ['f', 's', 'n', 'sn', 'st', 'k',
                        'T', 'Tn', 'tn', 'kw', 'y', 'kj', 'kwj',
                        'nw', 'wjn', 'tjwnj', 'wj', 'wjj', 'tjj',

                        ]

        has_diff_repl = ['wj']

        keep = []
        # keep = ['tj']
        sometimes = ['j', 't', 'w', 'wt', 'tj']

        second_delete = ['j']

        if not "." in word:
            return word
        elif reg(r'\.[^\-]+\-[^\.]+$', word):
            return word

        end = word
        begin = ""
        if '-' in word:
            didx = word.rindex(word)
            begin = word[:didx + 1]
            end = word[didx + 1]

        lst = end.split('.')
        for e, syl in en(lst[1:]):
            repl = suff_dct.get(syl)

            if e > 0 and syl in second_delete:
                lst[e + 1] = ""
            elif syl in sometimes:
                p(' ')
                p(self.sentence)
                p(f'{word} {syl}')

                str1 = input('keep? y or no ')

                if str1 == 'y':
                    pass
                elif repl:
                    lst[e + 1] = repl
                else:
                    lst[e + 1] = ""
            elif syl in has_diff_repl:
                p('')
                p(self.sentence)
                p(f'input how you want to replace {syl} in {word}')
                str1 = input('input: ')
                if not str1:
                    lst[e + 1] = ""
                else:
                    lst[e + 1] = str1

            else:
                if repl:
                    lst[e + 1] = repl
                elif syl in repl_w_blank:
                    lst[e + 1] = ""
                elif syl in keep:
                    pass

        e = 1
        while e < len(lst):
            str1 = lst[e]
            if not str1:
                del lst[e]
            else:
                e += 1
        end = ".".join(lst)

        return begin + end

    def split_infixes(self):
        e = 0
        while e < len(self.words_in_sent):
            word = self.words_in_sent[e]
            word = re.sub(r'[\(\)]', "", word)
            self.words_in_sent[e] = word
            if word.startswith('j.'):
                stem = word[2:]
                self.words_in_sent[e] = 'j='
                self.words_in_sent.insert(e + 1, stem)
            e += 1
        return

    def handle_new_meanings(self):
        self.word = self.word[2:]
        self.ins = temp_word()
        p(f"""
                put in 
                eng_word | source | pos
                """)
        str3 = input('input: ')
        lst2 = vgf.strip_n_split(str3, "|")
        self.ins.word = self.word
        self.ins.eng_word = lst2[0]
        self.ins.secondary_source = lst2[1]
        self.ins.pos = lst2[2]
        self.word1 = self.word
        self.must_test()
        lemma = hi.handle_new_meanings(self.tle_dct, self.ins)
        hi.add_single_lemma(self.ins, self.dct_cls, lemma)


class get_top_words:
    def __init__(self):
        dct_cls = pi.open_pickle('dictionary', 'hi')
        tle_dct = pi.open_pickle('tle_dct6', 'hi')
        lemma2freq = pi.open_pickle('lemma2freq', 'hi')
        ignore_for_now = pi.open_pickle('ignore_for_now', 'hi')
        ignore_for_now = set(ignore_for_now)

        done_lemmas = set()
        for x, y in dct_cls.items():
            for lemma in y['lemma_no']:
                done_lemmas.add(lemma)

        b = 0
        new_words = set()
        c = 0
        lst = []
        for x, y in lemma2freq.items():
            lemma = tle_dct[x]
            c += 1
            if x not in ignore_for_now:
                pos = lemma.pos
                use = False

                if pos[0] not in ['p', 'i', 'e', 'r', 'q', 'c', 'm', 'u']:
                    if "-" in x:
                        pass
                    elif pos == 'npa':
                        use = True
                    elif pos.startswith('np') or pos in ['jp', 'jn']:
                        pass
                    elif len(pos) > 1 and pos[:2] in ['vc']:
                        pass
                    else:
                        use = True

                    if use:
                        word = lemma['word']
                        if "-" not in word and word not in dct_cls \
                                and "(" not in word:

                            eng_word = lemma['eng_word']
                            lst.append([x, pos, word, eng_word])
                            new_words.add(word)

                            p(word)

                            # dc_entry = dct_cls.get(word)
                            # if dc_entry:
                            #     eng_word = lemma['eng_word']
                            #     p (eng_word)
                            #

                            if len(new_words) > 500:
                                break

        pi.save_pickle(new_words, 'temp_lemmas', 'hi')
        return

args = vgf.get_arguments()




if 'al' in args:
    add_lemmas2vocab()

elif 'fs' in args:
    fix_sentences(args)


## fix lacunae bug