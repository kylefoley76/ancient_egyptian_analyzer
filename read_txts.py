import add_path
from general import *
import random
from global_hiero import *
from mine_tle import tle_entry
import hieroglyphs as hi
from hieroglyphs import temp_word
from get_roots import split_infixes


def count_words2():
    txts = pi.open_pickle('tle_txts5', 'hi')


def count_words(txt, total, start=0, stop=0):
    if stop == 0:
        pass
        # stop = len(txt.translit)

    b = 0
    for x in txt.revised:
        # for x in txt.translit[start:stop]:
        for z in x:
            if z[1] > 0:
                # if z[0] > 0:
                b += 1
    total += b
    p(b, total)

    return total


def get_all_sents():
    """
    85216 sentences
    69824 unique sentences
    """

    texts = pi.open_pickle('tle_txts5', 'hi')
    all_sents = []
    for txt in texts.values():
        for z in txt.trust:
            z = re.sub(r'\.{2,}', '#', z)

            z = re.sub(r'[\-\.]', "", z)
            all_sents.append(z)
    st = set(all_sents)
    p(len(all_sents))
    p(len(st))


def comp_lsts(lst1, lst2):
    for x, y in zip(lst1, lst2):
        if type(x) == list:
            x = " ".join(x)
        if type(y) == list:
            y = " ".join(y)
        p(x)
        p(y)
        p('')


class parent:
    def __init__(self, args):
        self.start = 0
        self.day = args.get("day", 0)
        self.tar_day = args.get("tar_day", 0)
        self.debug = args.get('debug')
        self.kind = args.get('kind')
        self.print_test = args.get('print_test')
        self.print_section = args.get('print_section')
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')
        self.word2lemma = pi.open_pickle('word2lemma', 'hi')
        self.total_words = 0
        self.corpus_syn = ['812', 'sinuhe', '943', '939', '369', 'peasant', '790', '1081', '872']
        self.corpus = ['812', '848', '842', '943', '939', '369', '863', '858', '860', '790', '1081', '872']
        self.corpus2 = ['354', '619', '1382', '1589']
        # get thoth's 1589 from backup
        parkinson = [
            "610",
            "659",
            "797",
            "799",
            "805",
            "825",
            "852",
            "852",
            "866",
            "875",
            "895",
            "935",
            "1047",
            "1093",
            "1093",
            "1589",
            "15687",
            "18491",
            "18523",
            "18525",
            "18527",
            "18529",
            "18709",
            "18721",
            "18722",
            "18734",
        ]
        self.corpus2 += parkinson

    def get_txts(self):
        self.txts = pi.open_pickle('tle_txts5', 'hi')

    def get_date(self):
        self.start_time = time.time() - (7 * 60 * 60)
        if type(self.day) == str:
            self.dat = self.day
        else:
            b = self.start_time - (24 * 60 * 60 * self.day)
            self.dat = tf.from_unix2str_yr_day(b)
            self.dat = self.dat.replace('/', "_")
        if type(self.tar_day) == str:
            pass
        else:
            b = self.start_time - (24 * 60 * 60 * self.tar_day)
            self.tar_day = tf.from_unix2str_yr_day(b)
            self.tar_day = self.tar_day.replace('/', "_")

    def fix_apostrophe2(self, lst):
        for x in lst:
            self.fix_apostrophe(x)

    def fix_apostrophe(self, lst):
        str1 = lst[0]
        str1 = str1.replace("'", '')
        str1 = str1.replace('"', '')
        for num in range(2, len(lst), 3):
            word = lst[num + 1]
            if word not in str1:
                p(f"the word {word} was not in the sentence "
                  f"{str1}")
            str1 = str1.replace(word, f"'{word}'")
        lst[0] = str1
        return

    def for_review(self):
        self.get_new()
        eng_words = []
        eng_answers = []
        w_meaning = []
        prepo = []

        for x in self.future_study:
            if not x[0].startswith('tested'):
                eg_sent = x[1]
                en_sent = x[0]
                once = False
                for num in range(2, len(x), 3):
                    en_word = x[num + 1]
                    eg_word = x[num]
                    lemma = x[num + 2]
                    entry = self.tle_dct[lemma]
                    pos = entry.pos
                    if not is_prep(pos, eg_word, lemma):
                        eng_words.append(en_word)
                        eng_answers.append(f"{en_word} {eg_word}")
                        if not once:
                            once = True
                            w_meaning.append(en_sent)
                            w_meaning.append(eg_sent)
                    elif reg(r'_\d_', eg_sent):
                        prepo.append(en_sent)
                        prepo.append(eg_sent)
                        prepo.append(eg_word)
                    else:
                        self.print_prep(prepo, en_sent, eg_sent, eg_word)

        lst = [eng_words, eng_answers, prepo, w_meaning, ]
        str1 = input('pdf or text? return for pdf')
        if not str1:
            self.make_pdf(lst)
        else:
            self.make_txt(lst)
        return

    def print_prep(self, prepo, en_sent, eg_sent, eg_word):
        blank = eg_sent.replace(f' {eg_word} ', " __ ")
        prepo.append(en_sent)
        prepo.append(blank)
        prepo.append(eg_word)

    def make_txt(self, lst):
        lst1 = []
        for x in lst:
            lst1 += x
            lst1 += [''] * 5
        to.from_lst2txt(lst1, hdir + 'temp/temp_vocab')
        vgf.open_txt_file(hdir + 'temp/temp_vocab')

    def make_pdf(self, lst):
        all_pdfs = []
        b = 0
        for e, x in en(lst):
            lst2 = vgf.make_columns().main(x)
            for lst3 in lst2:
                to.from_lst2pdf(lst3, hdir + f'temp2/temp{b}.pdf')
                all_pdfs.append(f'temp{b}.pdf')
                b += 1

        vgf.merge_pdfs(all_pdfs, hdir + 'temp2/')
        while 1:
            try:
                shutil.copy(hdir + 'temp2/result.pdf', '//volumes/photos/result.pdf')
                break
            except:
                str1 = input('input zip drive, return to give up')
                if not str1:
                    vgf.open_txt_file(hdir + 'temp2/result.pdf')
                    break

    def get_new(self):
        p('choose what to print, return for all')
        for e, x in en(self.future_study):
            p(f'{e}  {x[0]}')

        str1 = input('input range delim by space ')
        if not str1:
            return
        else:
            lst = str1.split()
            start = int(lst[0])
            stop = int(lst[1])
            self.future_study = self.future_study[start:stop]

        return

    def get_to_study(self, dat):
        try:
            return to.from_txt2lst_tab_delim(fcdir + f'to_study_{dat}.txt')
        except:
            return []


class test_vocab(parent):
    def __init__(self, args):
        parent.__init__(self, args)
        parent.get_date(self)
        self.total_right = 0
        self.past_to_study = []
        self.temp_right = []

    def review_words(self):
        p(f'getting words from {self.dat}')
        p(f'putting wrong words into {self.tar_day}')
        self.to_study = self.get_to_study(self.dat)
        self.future_study = self.get_to_study(self.tar_day)
        self.to_study = self.to_study[1:]
        self.fix_apostrophe2(self.to_study)
        self.fix_apostrophe2(self.future_study)
        random.shuffle(self.to_study)
        self.main_loop()
        pi.save_pickle(self.tle_dct, "tle_dct6", 'hi')
        self.filter_sents()
        self.filter_sents2()
        self.save_vocab()
        str1 = input('print test? return for yes ')
        if not str1:
            self.fix_apostrophe2(self.future_study)
            self.for_review()
        return

    def main_loop(self):
        self.skipped = 1
        while self.skipped:
            if self.skipped == 1:
                lst = self.to_study
                self.skipped = []
            else:
                lst = self.skipped
                self.skipped = []

            for e, self.sent in en(lst):
                p(f'chunk {e} of {len(lst)}')
                self.wrong_lemmas = [self.sent[0], self.sent[1]]
                self.right_lemmas = [self.sent[0], self.sent[1]]
                self.loop_sent()

        b = self.total_words - self.total_right
        p(f'{b} words to review')

    def loop_sent(self):
        for i in range(2):
            prep = False if not i else True
            for num in range(2, len(self.sent), 3):
                self.egy_word = self.sent[num]
                self.eng_word = self.sent[num + 1]
                self.lemma = self.sent[num + 2]
                entry = self.tle_dct.get(self.lemma)
                if entry:
                    pos = entry.pos
                    lemma = self.lemma
                    if not prep and not is_prep(pos, self.egy_word, lemma) or \
                            prep and is_prep(pos, self.egy_word, lemma):

                        if not prep:
                            p(self.sent[0])
                            if len(self.sent) > 5:
                                p(self.eng_word)
                        elif prep:
                            p(self.sent[0])
                            if not reg(r'_\d_', self.sent[1]):
                                self.old_prep_print()
                            else:
                                p(self.sent[1])

                        str1 = input('see answer?')
                        if str1 == "h":
                            if self.egy_word[0] in ['(', "<", "["]:
                                p(self.egy_word[1])
                            else:
                                p(self.egy_word[0])
                            str1 = input('see answer?')
                            if str1 == 's':
                                self.skipped.append(self.sent)
                                return

                        elif str1 == 's':
                            self.skipped.append(self.sent)
                            return

                        self.total_words += 1
                        p(self.egy_word)
                        self.input_score()
                        entry.scores.append(self.score)
                        self.adjust_score(self.score)
        p(self.sent[1])
        self.add2wrong_lemmas()

    def old_prep_print(self):
        str1 = self.sent[1]
        str1 = str1.replace(f" {self.egy_word} ", " __ ")
        p(str1)

    def input_score(self):
        while True:
            try:
                str1 = input('score, return for right, / for 0, q to quit')

                if not str1:
                    self.score = 1
                    self.right_lemmas.append(self.egy_word)
                    self.right_lemmas.append(self.eng_word)
                    self.right_lemmas.append(self.lemma)

                elif str1 == 'q':
                    break
                else:
                    if str1 == '/':
                        self.score = 0
                    else:
                        self.score = float(str1)
                    self.wrong_lemmas.append(self.egy_word)
                    self.wrong_lemmas.append(self.eng_word)
                    self.wrong_lemmas.append(self.lemma)
                break
            except:
                p('wrong input')

    def add2wrong_lemmas(self):
        if len(self.right_lemmas) > 2:
            self.past_to_study.append(self.right_lemmas)
        if len(self.wrong_lemmas) > 2:
            self.future_study.append(self.wrong_lemmas)

    def adjust_score(self, score):
        self.total_right += score
        num = self.total_right / self.total_words
        p(f'right {self.total_right} of {self.total_words}')
        num = int((round(num, 2)) * 100)
        p(f'percent right {num}')
        p('')

    def filter_sents(self):
        dct1 = {}
        for x in self.past_to_study:
            en_sent = x[0]
            en_sent = en_sent.replace("'", "")
            en_sent = en_sent.strip()
            if en_sent not in dct1:
                dct1[en_sent] = x[1:]
            else:
                lst = dct1.get(en_sent)
                lst += x[2:]

        lst1 = []
        for x, y in dct1.items():
            lst2 = [x] + y
            lst1.append(lst2)
        self.past_to_study = lst1

    def filter_sents2(self):
        for e, x in en(self.past_to_study):
            st = set()
            for num in range(2, len(x), 3):
                tpl = (x[num], x[num + 1], x[num + 2])
                st.add(tpl)
            lst3 = list(st)
            lst1 = [x[0], x[1]]
            for tpl in lst3:
                lst1.append(tpl[0])
                lst1.append(tpl[1])
                lst1.append(tpl[2])
            self.past_to_study[e] = lst1

        self.past_to_study.insert(0, [f"tested_on_{self.tar_day}"])

    def save_vocab(self):
        for i in range(2):
            if not i:
                lst = self.future_study
                dat = self.tar_day
            else:
                dat = self.dat
                lst = self.past_to_study

            to.from_lst2txt_tab_delim(lst, fcdir + f'to_study_{dat}')


class score_comprehension:
    def __init__(self):
        self.headers = [
            "words",
            "vocab",
            "clause%",
            "try2%",
        ]
        self.raw_headers = [
            "txt",
            "tot_clause",
            "corr_clause",
            "calc_words",
            "try2_corr",
            'corr_word',
        ]

    def score2(self):
        self.update_scores()

    def update_scores(self):
        ccl = self.day_stats['corr_clause']
        tcl = self.day_stats['tot_clause']
        t2cl = self.day_stats['try2_corr']
        cw = self.day_stats['corr_word']
        tw = self.day_stats['calc_words']
        found = False
        begin = 0
        self.scores = []
        lsts = []
        for f, x in en(self.txt.revised):
            lst = []
            for e, z in en(x):
                if type(z[0]) == str and z[0][0] == '/':
                    if not begin:
                        begin = f
                    self.scores.append([z[0], self.count_clause_words(x)])
                    if x[e + 1][2] not in ['.', ',']:
                        p(f"is in the wrong location {x[e + 1][0]}")
                        found = True
                else:
                    lst.append(z)
            lsts.append(lst)
        if found:
            assert False

        self.txt.revised = lsts
        for score in self.scores:
            self.get_scores(score[0].strip(), score[1])
        if self.scores:
            self.prepare_per(ccl, tcl, t2cl, cw, tw)
            str1 = input('continue')

    def temp_print(self, begin):
        for x in self.txt.revised[begin:]:
            for z in x:
                p(z)

    def count_clause_words(self, lem_sent):
        num_words = 0
        for x in lem_sent:
            if len(x) == 1 and x[0][0] != "/":
                num_words += x[0].count(' ') + 1
            elif len(x) == 1:
                pass
            elif type(x[1]) == int and x[1] > 0:
                num_words += x[2].count(' ') + 1
            elif type(x[1]) == str:
                num_words += x[1].count(' ') + 1

        return num_words

    def get_scores(self, str1, num_words):
        self.num_words = num_words
        self.day_stats['calc_words'] += num_words
        """
            if perfect input nothing, the default number of relations is 3
            the first digit is the number of relations correct
            the second digit is the number of possible relations
            if you decide to add words to your vocab test after all
            then end the string with an 'a'
            to add a lemma in retrospect end the string with l
            """
        if str1 == '//':
            self.score_relations([1, 1])
            self.score_vocab(0)
        else:
            lst = str1[2:].split()
            lst = [float(x) for x in lst]
            self.score_relations(lst)
            wrong = lst[2] if len(lst) > 2 else 0
            self.score_vocab(wrong)

    def score_relations(self, lst):
        try1 = lst[0]
        try2 = lst[1]
        self.day_stats['tot_clause'] += 1
        self.day_stats['corr_clause'] += try1
        self.day_stats['try2_corr'] += try2

    def prepare_per(self, ccl, tcl, t2cl, cw, tw):
        """
        ccl = self.day_stats['corr_clause']
        tcl = self.day_stats['tot_clause']
        t2cl = self.day_stats['try2_corr']
        cw = self.day_stats['corr_word']
        tw = self.day_stats['calc_words']
        """
        ccl2 = self.day_stats['corr_clause'] - ccl
        tcl2 = self.day_stats['tot_clause'] - tcl
        t2cl2 = self.day_stats['try2_corr'] - t2cl
        cw2 = self.day_stats['corr_word'] - cw
        tw2 = self.day_stats['calc_words'] - tw
        p("""
        temp scores:
        """)
        self.get_percents(ccl2, tcl2, t2cl2, cw2, tw2)
        p("""
        day scores
        """)
        ccl2 = self.day_stats['corr_clause']
        tcl2 = self.day_stats['tot_clause']
        t2cl2 = self.day_stats['try2_corr']
        cw2 = self.day_stats['corr_word']
        tw2 = self.day_stats['calc_words']
        self.get_percents(ccl2, tcl2, t2cl2, cw2, tw2)

    def get_percents(self, ccl, tcl, t2cl, cw, tw):
        per = int((ccl /
                   tcl) * 100)
        self.day_stats['clause%'] = per
        p(f'clauses: {per}%')
        p('')
        per2 = int((t2cl /
                    tcl) * 100)
        self.day_stats['try2%'] = per2
        self.day_stats['txt'] = self.file_name
        per = int((cw / tw) * 100)
        self.day_stats['vocab'] = per

        p(f'clauses second try: {per2}%')
        p('')
        p(f'vocab score: {per}%')

    def score_vocab(self, wrong):
        self.day_stats['corr_word'] += self.num_words
        self.day_stats['corr_word'] -= wrong

    def get_stats(self):
        os.system(
            f'''/usr/bin/osascript -e 'tell app "TextEdit" to save (every window whose name is "comp_stats.txt")' ''')
        os.system(
            f'''/usr/bin/osascript -e 'tell app "TextEdit" to close (every window whose name is "comp_stats_raw.txt")' ''')
        self.history = to.from_table2dct(hdir + 'temp/comp_stats')
        raw = to.from_table2dct(hdir + 'temp/comp_stats_raw')
        self.raw_stats = raw
        day1 = self.dat.replace('_', '/')
        self.day_stats = self.history.get(day1, {})
        raw_stats = raw.get(day1)
        if not self.day_stats:
            rw1 = list(self.history.values())[0]
            rw2 = list(raw.values())[0]
            self.headers = list(rw1.keys())
            self.raw_headers = list(rw2.keys())
            for header in self.headers + self.raw_headers:
                self.day_stats[header] = 0
        else:
            self.day_stats = merge_2dicts(self.day_stats, raw_stats)

        for x, y in self.day_stats.items():
            if y == '':
                self.day_stats[x] = 0

    def calc_word_hr(self):
        b = time.time() - (7 * 60 * 60)
        c = (b - self.start_time)
        hours = c / (60 * 60)
        p(f"words per hour: {self.total_words // hours}")
        p(f"total words today: {self.day_stats['words']}")
        self.save_stats()

    def save_stats(self):
        temp = self.dat.replace('_', "/")
        dct1 = {}
        dct2 = {}
        for h in self.headers:
            dct1[h] = self.day_stats[h]
            if dct1[h] == 0: dct1[h] = ''
        for h in self.raw_headers:
            dct2[h] = self.day_stats[h]

        self.history[temp] = dct1
        self.raw_stats[temp] = dct2
        if not self.debug:
            to.from_dct2table(self.history, hdir + 'temp/comp_stats')
            to.from_dct2table(self.raw_stats, hdir + 'temp/comp_stats_raw')
