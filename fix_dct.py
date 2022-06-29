import add_path
from general import *
from global_hiero import *
from mine_tle import tle_entry, tle_file

import add_path
import read_txts
from PIL import ImageColor, Image

b = ImageColor.getcolor('red', 'RGBA')


class lemmatizecl:
    def __init__(self):
        pass

    def lemmatize(self):
        vgf.save_open_file("new_lemmas.txt")
        for e, y in en(self.txt.revised):
            for f, x in en(y):
                if len(x) == 2:
                    try:
                        eng_sent = self.eng_sents[e]
                        egy_sent = self.egy_sents[e]

                        idx = x[0]
                        word = x[1]
                        word2 = re.sub(r'[\[\]\{\}\(\)\.\<\>\-\']', '', word)
                        obj = self.word2lemma.get(word2)

                        p(f"""
                        {word2}
                        {eng_sent}
                        {egy_sent}
                        """)

                        if not obj:
                            p(f'{word2} is not in the dictionary')
                        else:
                            obj = list(obj)
                            for g, lemma in en(obj):
                                entry = self.tle_dct[lemma]
                                word3 = entry.word
                                eng = entry.eng_word
                                pos = entry.pos
                                p(f'{g} {word3}  {pos}  {eng}')
                    except:
                        p(f'error in {x}')
                        return False
                    while True:
                        try:
                            p('input * to give up and move on, semicolon to manually add lemma')

                            str1 = input('choose, start with period to add lemma ')
                            if str1 == '*':
                                self.txt.revised[e][f] = [idx, 999_999, "z", word]
                                break
                            else:
                                self.oc_eg = True
                                if str1[0] == '.':
                                    self.new_lem = True
                                    self.add_lemma()
                                    num = self.max_lemma
                                elif str1[0] == ';':
                                    str2 = input('manual lemma: ')
                                    num = int(str2)
                                    self.word2lemma[word2] = {num}
                                else:
                                    num = obj[int(str1)]
                                pos = self.tle_dct[num].pos

                                self.txt.revised[e][f] = [idx, num, pos, word]
                                break
                        except:
                            p('wrong input')

    def add_lemma(self):
        while True:
            try:
                str1 = input("add word, eng_word, pos, source, delimit comma ")
                lst = str1.split(",")
                self.max_lemma += 1
                lst1 = [self.max_lemma, lst[2], lst[0], lst[1], lst[3]]
                self.add_lemma2(lst1)
                break
            except:
                p('wrong input')

    def add_lemma2(self, lst):
        self.new_lem = True
        entry = tle_entry()
        entry.lemma_no = lst[0]
        entry.word = lst[2]
        entry.eng_word = lst[3]
        entry.source = lst[4]
        entry.pos = lst[1]
        self.tle_dct[self.max_lemma] = entry
        if entry.pos != 'x':
            st = self.word2lemma.get(entry.word)
            if not st:
                self.word2lemma[entry.word] = {self.max_lemma}
            else:
                st.add(self.max_lemma)
                self.word2lemma[entry.word] = st

    def fix_new_lemmas(self):
        file = hdirp + "new_lemmas.txt"
        lst = to.from_txt2lst_tab_delim(file)
        for x in lst:
            lem = x[0]
            if type(lem) == int and lem not in self.tle_dct:
                self.new_lem = True
                self.add_spec_lemma(lemma, x)
            elif type(lem) == str:
                self.new_lem = True
                lemma = int(lem[1:])
                if "*" in lem:
                    del self.tle_dct[lemma]
                elif "/" in lem:
                    entry = self.tle_dct[lemma]
                    entry.pos = x[1]
                    old_word = entry.word
                    if old_word != x[2]:
                        self.fix_word2lemma(old_word, x[2], lemma)
                    entry.word = x[2]
                    entry.eng_word = x[3]
                    if len(x) > 4:
                        entry.source = x[4]


        return

    def remove_punct(self, word):
        word = re.sub(r'[\[\]\(\)\<\>\.\-\s]', "", word)
        return word

    def fix_word2lemma(self, old_word, new_word, lemma):
        old_word2 = self.remove_punct(old_word)
        st = self.word2lemma.get(old_word2)
        try:
            st.remove(lemma)
        except:
            pass
        new_word2 = self.remove_punct(new_word)
        new_st = self.word2lemma.get(new_word2)
        if new_st:
            new_st.add(lemma)

    def add_spec_lemma(self, lemma, x):
        self.max_lemma = lemma + 1
        x.insert(0, lemma)
        self.add_lemma2(x)

    def print_new_lemmas(self):
        if self.new_lem:
            vgf.close_file('new_lemmas.txt')
            lst1 = []
            for x, y in self.tle_dct.items():
                if x > 999_999:
                    pos = y.pos
                    word = y.word
                    eng = y.eng_word
                    so = y.main_source
                    if not so:
                        so = 'ns'
                    lst = [x, pos, word, eng, so]
                    lst1.append(lst)

            to.from_lst2txt_tab_delim(lst1, hdirp + "new_lemmas.txt")
            vgf.open_txt_file(hdirp + "new_lemmas.txt")


class link_wordscl:
    def __init__(self):
        pass

    def link_words(self):
        self.tough_phrases()
        self.get_idx2word()
        self.link_words2()
        to.from_lst2txt_tab_delim(self.future_study, fcdir + f'to_study_{self.tar_day}.txt')
        self.save_txt2word()

    def tough_phrases(self):
        file = fcdir + f'tough_phrases/{self.file_name}.txt'
        try:
            lst1 = to.from_txt2lst(file)
        except:
            lst1 = []
        lst_egy = ""
        lst_eng = ""

        for e, x in en(self.txt.sent_type['test']):
            egy = self.txt.trust[x]
            eng = self.txt.english2[x]
            if e < len(self.txt.sent_type['test']) - 1:
                nxt = self.txt.sent_type['test'][e + 1]
                if nxt == x + 1:
                    str1 = " " if lst_egy else ""
                    egy = f"{lst_egy}{str1}{egy}"
                    eng = f"{lst_eng}{str1}{eng}"
                    lst_egy = egy
                    lst_eng = eng
                else:
                    str1 = " " if lst_egy else ""
                    egy = f"{lst_egy}{str1}{egy}"
                    eng = f"{lst_eng}{str1}{eng}"
                    if egy not in lst1:
                        tpl = (egy, eng)
                        self.test_phrases.append(tpl)
                        lst1.append(egy)
                    lst_egy = ""
                    lst_eng = ""

        file = fcdir + f"tough_phrases/{self.file_name}.txt"
        to.from_lst2txt(lst1, file)
        to.from_lst2txt_tab_delim(self.test_phrases, fcdir + f'tough_phrases_{self.dat}.txt')
        return

    def get_idx2word(self):
        self.get_txt2word()
        self.idx2word = {}
        for e, x in en(self.txt.revised):
            for y in x:
                if len(y) == 4:
                    self.idx2word[y[0]] = [y[1], y[3], e]

    def get_txt2word(self):
        file = fcdir + f"txt2word/{self.file_name}.txt"
        try:
            lst = to.from_txt2lst_tab_delim(file)
            self.txt2word = set()
            for x in lst:
                y = tuple(x)
                self.txt2word.add(y)
        except:
            self.txt2word = set()

    def link_words2(self):
        self.used_lemmas = set()
        for e, y in en(self.en_lst):
            unknown = []
            preps = 0
            lem_sent = jsonc(self.txt.revised[e])

            _ = self.link_words3(lem_sent, preps, unknown, y)
            lst1, preps, rev = _

            if unknown:
                if preps > 0:
                    eg_sent = [x[3] for x in lem_sent if x[1] > 0]
                    eg_sent = " ".join(eg_sent)
                else:
                    eg_sent = self.egy_sents[lst1[2]]
                esent = self.eng_sents[e]
                esent1 = ""
                eg_sent1 = ""
                if e > 0:
                    esent1 = self.eng_sents[e - 1]
                    eg_sent1 = self.egy_sents[lst1[2] - 1]
                tegy_sent = f'{eg_sent1} {eg_sent}'
                ten_sent = f'{esent1} {esent}'
                ten_sent = re.sub(r'=\d+\**', '', ten_sent)
                if "{{" in ten_sent:
                    bb = 8

                ten_sent = re.sub(r'\{\{.*\}\}', "", ten_sent)
                if not rev:
                    unknown.insert(0, tegy_sent)
                    unknown.insert(0, ten_sent)
                else:
                    unknown.insert(0, ten_sent)
                    unknown.insert(0, tegy_sent)

                self.future_study.append(unknown)
        return

    def link_words3(self, lem_sent, preps, unknown, y):
        lst1 = []
        rev = False
        for en_word in y:
            if reg(r'=\d', en_word):
                nword, num = self.word_equal(en_word)
                tpl = (num, nword)
                if tpl not in self.txt2word:
                    rev = False
                    self.txt2word.add(tpl)
                    lst1 = self.idx2word[num]
                    lemma = lst1[0]
                    entry = self.tle_dct[lemma]
                    rank = entry.rank
                    freq = entry.frequency

                    pos = entry.pos
                    eg_word = lst1[1]
                    if rank > 0 and rank < 70:
                        rank = self.common_root(eg_word, entry)

                    if is_prep(pos, eg_word, lemma):
                        preps += 1
                        self.build_eg_sent(lem_sent, num, preps)
                        if preps > 1:
                            bb = 8

                    if lemma not in self.used_lemmas and \
                            (rank > 69 or rank == 0):
                        eg_word = re.sub(r'\{.\}', '', eg_word)
                        eg_word = re.sub(r'[\[\]\<\>]', '', eg_word)
                        self.used_lemmas.add(lemma)
                        if nword[-1] == '.':
                            rev = True
                            unknown.append(nword[:-1])
                            unknown.append(eg_word)

                        else:
                            unknown.append(eg_word)
                            unknown.append(nword)
                        unknown.append(lemma)
        return lst1, preps, rev

    def word_equal(self, word):
        idx = word.index("=")
        b = word[idx + 1:].strip()
        while 1:
            try:
                num = int(b)
                break
            except:
                p(f'failed to get number on {word}')
                str1 = input('fix sheet')

        return word[:idx], num

    def build_eg_sent(self, lem_sent, num, pidx):
        for x in lem_sent:
            if x[0] == num:
                x[3] = f"_{pidx}_"

    def common_root(self, word, entry):
        p(f"""
        the word {word} is uncommon which is defined as
        {entry.eng_word}
        """)

        str1 = input('return for common, else uncommon')
        if not str1:
            return 70
        else:
            return 1

    def save_txt2word(self):
        file = fcdir + f"txt2word/{self.file_name}.txt"
        dct1 = {}
        for x in self.txt2word:
            dct1[x[0]] = x[1]
        dct1 = sort_dct_key(dct1)
        lst = [[x, y] for x, y in dct1.items()]
        to.from_lst2txt_tab_delim(lst, file)


class run_time_test(read_txts.score_comprehension,
                    read_txts.parent,
                    lemmatizecl,
                    link_wordscl):

    def __init__(self, args):
        read_txts.parent.__init__(self, args)
        read_txts.score_comprehension.__init__(self)
        lemmatizecl.__init__(self)
        link_wordscl.__init__(self)
        self.file_name = args.get('file_name')
        self.start = args.get('start', 0)
        self.estart = args.get('estart', 0)
        self.get_date()
        self.get_txts()
        self.file = hdir + f'tle_trans/{self.file_name}_divided.txt'
        self.eng_file = hdir + f'tle_trans/{self.file_name}_english_div.txt'
        self.txt = self.txts[self.file_name]
        self.lst_bk = 0
        self.get_stats()

    def just_check(self, bool1=False):
        while True:
            str1 = self.main(bool1)
            if str1 == 'q':
                break
        return

    def build_trust(self):
        lsts = []
        for x in self.txt.revised:
            lst = []
            for z in x:
                try:
                    if z[1] > 0 or z[2] in ['.', ',']:
                        if len(z) == 4:
                            lst.append(z[3])
                        elif len(z) == 3:
                            lst.append(z[2])
                    elif z[1] == -7:
                        lst.append("..")

                except:
                    p(z)
                    p('error in build trust')
                    sys.exit()
            lsts.append(lst)

        self.txt.trust = [" ".join(x) for x in lsts]
        for e, x in en(self.txt.trust):
            x = re.sub(r'[\[\]\<\>]', '', x)
            x = re.sub(r'\{.\}', '', x)
            self.txt.trust[e] = x

    def erase_sent_type(self):
        self.txt.sent_type = {
            'unsatisfactory': [],
            'misunderstood': [],
            'damaged': [],
            'test': [],
        }

    def main(self, bool1=False):
        self.oc_eg = False
        self.new_lem = False
        self.get_lsts()
        self.future_study = self.get_to_study(self.tar_day)
        self.get_tough_phrases()
        self.get_max_lemma()
        self.score_loop()
        self.check_matches_loop()
        self.get_eng4read()
        self.lemmatize()
        self.fix_new_lemmas()
        self.print_new_lemmas()
        self.build_trust()
        self.adjust_dct()
        self.count_words()
        self.reopen()
        self.save_pickles()
        if bool1:
            return
        p(f'words will be saved to {self.tar_day}')
        str1 = input('hit return to continue, q to quit, l to link, lc to link and continue ')
        if str1 == 'q':
            return 'q'
        elif str1[0] == 'l':
            if len(str1) > 2:
                self.tar_day = str1[2:].strip()
            self.link_words()
            self.fix_apostrophe2(self.future_study)
            self.for_review()
            if 'c' not in str1:
                return 'q'

    def get_lsts(self, ignore_score=0):
        self.erase_sent_type()
        vgf.save_open_file(self.file_name + '_divided.txt')
        vgf.save_open_file(self.file_name + '_english_div.txt')
        while True:
            self.eg_lst = to.from_txt2lst_tab_delim(self.file)
            done = self.is_well_formed()
            if not done:
                str1 = input('redo sheet')
            else:
                self.en_lst = to.from_txt2lst(self.eng_file, 1)
                done = self.abridge()
                if not done:
                    str1 = input('redo sheet')
                else:
                    break

        self.get_max_num()
        self.get_revised_egy(self.eg_lst, ignore_score)

    def is_well_formed(self):
        for e, x in en(self.eg_lst):
            if not type(x) == list:
                p(f"""
                after 
                {self.eg_lst[-1]}
                the line is not a list
                """)
            if x[0] == '/':
                pass

            if len(x) == 1:
                if type(x[0]) != str:
                    p(f'{x} is wrong')
                    return False
            if len(x) > 1:
                if type(x[0]) not in [int, str]:
                    p(f'{x} is wrong')
                    return False

                if x[1] == '':
                    p(f'{x} is wrong')
                    return False

            if len(x) > 2:
                if type(x[0]) != int:
                    p(f'{x} is wrong')
                    return False
                if type(x[1]) != int:
                    p(f'{x} is wrong')
                    return False

        return True

    def get_tough_phrases(self):
        try:
            self.test_phrases = to.from_txt2lst_tab_delim(fcdir + f'test_phrases_{dat}.txt')
        except:
            self.test_phrases = []

    def get_max_lemma(self):
        self.max_lemma = max(list(self.tle_dct.keys()))

    def abridge(self):
        for i in range(2):
            if not i:
                lst = self.eg_lst
                str1 = 'egyptian'
            else:
                lst = self.en_lst
                str1 = 'english'
            b = 0
            for e, x in en(lst):
                if not i and x[0] == 'zzz':
                    b += 1
                elif i and x == 'zzz':
                    b += 1
            if b != 1:
                p(f'incorrect zzz in {str1}')
                return False

        for e, x in en(self.eg_lst):
            if x[0] == 'zzz':
                lst2 = self.eg_lst[:e]
                self.other_eg = self.eg_lst[e:]
                self.eg_lst = lst2
                break

        for e, x in en(self.en_lst):
            if x == 'zzz':
                self.en_lst = self.en_lst[:e]
                break
        return True

    def replace_omissions(self):
        lst = ['J', "N", "M", "W", "/", 'R', 'Q','Y']
        lst1 = ['(j)', "(n)", "(m)", "(w)", "(A)", '(r)', "(t)",'(y)']
        for x in self.txt.revised:
            for b in x:
                for z, w in zip(lst, lst1):
                    if len(b) > 2 and type(b[2]) == str and b[1] > 0:
                        b[2] = b[2].replace(z, w)
                    elif len(b) == 2 and type(b[1]) == str:
                        b[1] = b[1].replace(z, w)

    def adjust_dct(self):
        '''
        to change a lemma put a - before the lemma on the sheet
        '''
        found = False
        file1 = f'{self.file_name}_div_answers.txt'
        file2 = hdir + f'tle_trans/{file1}'
        vgf.save_open_file(file1)
        lst_rw = 0
        txt_dct = to.from_txt2lst_tab_delim(file2)
        txt_dct2 = []
        for e, rw in en(txt_dct):
            if rw[0] == 'zzz':
                pass
            elif len(rw) == 7 and rw[0] == 144640:
                bb = 8

            elif len(rw) == 7 and \
                    type(rw[0]) == str and \
                    rw[0][0] == '/':
                found = True
                lemma = int(rw[0][1:])
                entry = self.tle_dct[lemma]
                entry.pos = rw[2]
                nword = rw[4]
                entry.eng_word = rw[6]
                lst_rw = e
                if nword != entry.word:
                    st = self.word2lemma.get(entry.word)
                    if st and lemma in st:
                        st.remove(lemma)
                    st1 = self.word2lemma.get(nword)
                    if st1:
                        st1.add(lemma)
                rw[0] = lemma
                txt_dct2.append(rw)
            else:
                txt_dct2.append(rw)

        if found:
            txt_dct2.insert(lst_rw, ['zzz'])
            self.close_txt("_div_answers.txt")
            to.from_lst2txt_tab_delim(txt_dct2, file2)
            vgf.open_txt_file(file2)

    def get_eng4read(self):
        lst = []
        for x in self.eng_sents:
            x = re.sub(r'=\d+\**', '', x)
            lst.append(x)

        self.txt.english2 = lst

    def get_revised_egy(self, lst, ignore_score=0):
        if not lst:
            file = hdir + f"tle_trans/{self.file_name}_divided.txt"
            lst = to.from_txt2lst_tab_delim(file)
        lsts = []
        lst1 = []

        for e, x in en(lst):

            if x[0] == 130:
                bb = 8

            if type(x[0]) == str and x[0].startswith('zzz'):
                assert False
            if type(x[0]) == str and not reg('\S', x[0]):
                pass
            elif type(x[0]) == str and x[0].startswith('/') and \
                    not ignore_score:
                lst1.append(x)

            elif type(x[0]) == str and x[0].startswith('/') and \
                    ignore_score:
                pass

            elif x[0] in ['|', '.']:
                self.max_num += 1
                lst1.append([self.max_num, -11, '.'])
                lsts.append(lst1)
                lst1 = []
                self.oc_eg = True

            elif x[0] == ',':
                self.max_num += 1
                lst1.append([self.max_num, -10, ','])
                lsts.append(lst1)
                lst1 = []
                self.oc_eg = True
            elif type(x[0]) == str:
                self.max_num += 1
                lst1.append([self.max_num, x[0]])
                self.oc_eg = True
            elif x[1] in [-10, -11]:
                if x[1] == -10:
                    x[2] = ','
                else:
                    x[2] = '.'

                if lst1:
                    lst1.append(x)
                    lsts.append(lst1)
                lst1 = []
                self.oc_eg = True
            else:
                if len(x) > 3:
                    x[3] = str(x[3])
                if len(x) == 3:
                    x[2] = str(x[2])
                elif len(x) == 2:
                    x[1] = str(x[1])
                    self.oc_eg = True
                lst1.append(x)

        self.txt.revised = lsts

    def check_matches_loop(self):
        self.attempt = 0
        while True:
            done = self.check_matches()
            if not done:
                self.get_lsts(1)
            else:
                break
            self.attempt += 1

    def get_max_num(self):
        lst6 = []
        for x in self.eg_lst:
            if type(x[0]) == int:
                lst6.append(x[0])
        self.max_num = max(lst6)

    def build_english(self, lst, use_sent_type=True):
        if not lst:
            file = hdir + f'tle_trans/{self.file_name}_english_div.txt'
            lst = to.from_txt2lst(file, 1)
        english = [x for x in lst if reg(r'\S', str(x))]
        lst1 = []
        found = False
        lst = []
        sidx = 0
        for e, x in en(english):
            if x.startswith('zzz'):
                break
            lst1.append(x)
            if "=" in x:
                found = True

            if "|" in x:
                if not use_sent_type:
                    lst.append(lst1)
                else:
                    lst.append(lst1[:-1])
                if use_sent_type:
                    if "?" in x:
                        self.txt.sent_type.setdefault('misunderstood', []).append(sidx)
                    elif 'd' in x:
                        self.txt.sent_type.setdefault('damaged', []).append(sidx)
                    elif 't' in x:
                        self.txt.sent_type.setdefault('test', []).append(sidx)
                    elif 'u' in x:
                        self.txt.sent_type.setdefault('unsatisfactory', []).append(sidx)
                sidx += 1
                lst1 = []
        for x in range(self.estart):
            lst.insert(0, ["*"])

        return lst, found

    def check_matches(self, just_link=False):
        self.egy_sents = []
        self.eng_sents = []
        isc = 1 if self.attempt > 0 else 0
        self.replace_omissions()
        self.en_lst, _ = self.build_english(self.en_lst)
        for x, y in zip(self.txt.revised, self.en_lst):
            temp_egy = self.get_temp_egy(x)
            temp_eng = [w for w in y]
            self.egy_sents.append(" ".join(temp_egy))
            self.eng_sents.append(" ".join(temp_eng))

        if just_link:
            return

        if len(self.txt.revised) == len(self.en_lst):
            if self.debug:
                return True
            self.quick_check()
            str2 = input('print all? y for yes ')
            if str2 != 'y':
                return True

        self.print_sents()

        str1 = input('make changes')
        return False

    def get_temp_egy(self, x):
        lst = []
        for z in x:
            if type(z[0]) == str and z[0][0] == '/':
                pass
            elif type(z[1]) == str:
                lst.append(z[1])
            elif z[1] > 0:
                lst.append(z[3])
        return lst

    def quick_check(self):
        b = len(self.egy_sents)
        c = b // 3
        d = c * 2
        for x in [c, d, -1]:
            p(f"""
            {self.egy_sents[x]}
            {self.eng_sents[x]}

            """)

    def print_sents(self):
        for x, y in zip(self.egy_sents, self.eng_sents):
            p(f"""
            {x}
            {y}
            """)

    def count_words(self):
        bk = to.from_txt2lst(hdir + 'bookmark.txt')
        self.start = int(bk[1])
        if str(bk[0]) != self.file_name:
            self.start = 0

        for x in self.txt.revised[self.start:]:
            for z in x:
                if len(z) > 2 and type(z[1]) == int and z[1] > 0:
                    c = z[2].count(" ") + 1
                    self.day_stats['words'] += c
                    self.total_words += c

        lst = [self.file_name, len(self.txt.revised), bk[2], bk[3]]
        p(f'last sentence read was '
          f'{self.egy_sents[-1]}')
        to.from_lst2txt(lst, hdir + 'bookmark.txt')
        self.calc_word_hr()
        if self.scores:
            self.save_stats()

    def score_loop(self):
        # self.update_scores()
        while True:
            try:
                self.update_scores()
                break
            except:
                str1 = input('adjust sheet for scores')
                self.get_lsts()
                break

    def reopen(self):
        if self.oc_eg or self.scores:
            self.close_txt("_divided.txt")
            lst = []
            for f, x in en(self.txt.revised):
                for e, z in en(x):
                    lst.append(z)
                    if not type(z) == list:
                        self.oc_eg = False
                        str1 = input('fix divided')
                        return

            lst += self.other_eg

            to.from_lst2txt_tab_delim(lst, self.file)
            if not self.debug:
                vgf.open_txt_file(self.file)

    def close_txt(self, str1):
        os.system(
            f'''/usr/bin/osascript -e 'tell app "TextEdit" to close (every window whose name is "{self.file_name}{str1}")' ''')

    def save_pickles(self):
        if self.oc_eg:
            pass
        pi.save_pickle(self.word2lemma, 'word2lemma', 'hi')
        pi.save_pickle(self.tle_dct, 'tle_dct6', 'hi')
        pi.save_pickle(self.txts, 'tle_txts5', 'hi')
        return


class fix_dictcl:
    def __init__(self):
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')

    def print_dct(self):

        lst = []
        # dct = sort_dct_key(tle_dct3)
        for k, v in tle_dct3.items():
            lemma = k
            if lemma > 999_999:
                word = v.word
                eng = v.eng_word
                ger = v.ger_word
                pos = v.pos
                source = v.main_source
                if not pos:
                    pos = 0
                lst1 = [lemma, pos, word, eng, ger, source]
                lst.append(lst1)

        file = hdirp + "tle_dct_new"
        to.from_lst2txt_tab_delim(lst, file)
        vgf.open_txt_file(file + '.txt')

    def temp18(self):
        lst = []
        # dct = sort_dct_key(tle_dct3)
        for k, v in tle_dct3.items():
            lemma = k
            if lemma > 999_999:
                word = v.word
                word2 = word.replace('.', '')
                obj = word2lemma.get(word2)
                if obj:
                    lst.append([""])
                    for lem in obj:
                        if lem < 1_000_000:
                            entry2 = tle_dct3.get(lem)
                            lst.append([entry2.word, entry2.eng_word])
                    lst.append([''])

                eng = v.eng_word
                ger = v.ger_word
                pos = v.pos
                source = v.main_source
                if not pos:
                    pos = 0
                lst1 = [lemma, pos, word, eng, ger, source]
                lst.append(lst1)
        file = hdirp + "tle_dct_new"
        to.from_lst2txt_tab_delim(lst, file)
        vgf.open_txt_file(file + '.txt')

    def get_dct(self):
        file = hdirp + 'tle_dct.txt'
        lst = to.from_txt2lst_tab_delim(file)
        for x in lst:
            lemma = x[0]
            if '*' in lemma:
                self.revise_entry(x)
            elif '#' in x[0]:
                self.new_entry(x)
                pos = x[1]
                word = x[2]
                eng = x[3]
                source = x[4]
                lemma = int(x[0][:-1])

    def revise_entry(self, x):
        lemma = int(x[0][:-1])
        entry = self.tle_dct[lemma]
        entry.pos = x[1]
        entry.eng_word = x[2]

    def new_entry(self, x):
        pass

        for x, y in tle_dct3.items():
            if x > 999_999:
                pass


"""
commas are marked with -10
periods with -11
u
sentences for which the translation is not satisfactory are marked with u
after the | on the english
?
misunderstood sentences are marked with ? after | in the english
t
sentences which end with |t in the english need to be tested for comprehension
by showing the egyptian first
d
are sentences which are too damaged to be considered further


sailor = 812 D
sinuhe (done)
peasant D
senworset = 369 D
herdsman = 790 D
loyalist = 943 (done)
ptahotep - 1081
ba - 872
kagemni - 939 D


"""
