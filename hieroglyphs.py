import add_path
from general import *
import random
import pyautogui
from PIL import Image
from global_hiero import *
from mine_tle import tle_entry, tle_file

'''
not in phon2num

no name
u29

check that d33 is named arms and oar

v1 has a weird phonogram

r5 is not the censer but the penis with fluid

## some sentences with two phonograms start with phonograms
## aa5 was not named
## a1 is missing

'''


def common_pdf_mistakes():
    pdf_mistakes = {
        339: 7717,
        230: 42786,  # 'Ꜣ' alif
        239: 7791,  # 'ṯ' second t
        235: 42789,  # 'ꜥ' ayn
        227: 7723,  # 'ḫ' third h
        245: 7830,  # 'ẖ' fourth h
        255: 7695,  # 'ḏ' second d
    }





class other_tests:
    def __init__(self):
        self.word = ""
        self.eng_word = ""
        self.nxt_tst = 0
        self.scores = []
        self.main_source = ""
        self.elit = ""
        self.recon = ""
        self.secondary_source = ""

    def __repr__(self):
        return self.word


class questions:
    def __init__(self):
        self.question = ""
        self.answer = ""
        self.nxt_tst = 0
        self.scores = []
        self.source = ""

    def __repr__(self):
        return self.question


class temp_word:
    def __init__(self):
        self.word = ""
        self.eng_word = ""
        self.main_source = ""
        self.secondary_source = ""
        self.notes = ""
        self.pos = ""

    def __repr__(self):
        return self.word


def all_my_words():
    dct_cls = pi.open_pickle('dictionary', 'hi')
    while True:
        obj = input('input: ')
        entry = dct_cls.get(obj)
        if entry:
            p(entry.eng_word)
        else:
            p('not have')


def add_single_lemma(tle_dct, word2lemma, word, ins=0):
    if ins:
        eng = ins.eng_word
        source = ins.source
        pos = ins.pos
        num = ins.lemma_no

    else:
        num = max([int(x.lemma_no) for x in tle_dct.values()]) + 1
        num = str(num)

        p("""
            input word (if not properly spelled) | english | source
            """)
        str1 = input('input: ')


        if '|' in str1:
            lst = vgf.strip_n_split(str1, "|")
        else:
            lst = [str1]

        if len(lst) == 3:
            word = lst[0]
            eng = lst[1]
            source = lst[2]
        elif len(lst) == 2:
            eng = lst[0]
            source = lst[1]
        else:
            eng = lst[0]
            source = 'Allen'

    ins = tle_entry()
    ins.lemma_no = num
    ins.word = word
    ins.eng_word = eng
    ins.source = source
    ins.nxt_tst = time.time()
    tle_dct[num] = ins
    word2lemma.setdefault(word, set()).add(num)
    pi.save_pickle(tle_dct, 'tle_dct6', 'hi')
    pi.save_pickle(word2lemma, 'word2lemma', 'hi')
    return ins




def add_single_lemma2(ins, dct_cls, lemma):
    entry = dct_cls.get(ins.word)
    lst = [lemma, ins.pos, 0, ins.eng_word]
    if entry:
        entry.word = ins.word
        entry.eng_word.append(lst)
    else:
        entry = tle_entry()
        entry.word = ins.word
        entry.eng_word = [lst]
    entry.nxt_tst = time.time()
    entry.lemma_no = [x[0] for x in entry.eng_word]
    dct_cls[ins.word] = entry


class transfer_notes:
    def __init__(self):
        """
        questions are surround by {}
        a semicolon separates the question, with the answer coming 2nd,
        a third semicolon, indicates the importance level of the question
        with nothing being high importance, 2 being low iportance, 3 even lower.
        
        if you get lazy and just want a note then do not put a ; within the {}
        
        to pick out words to put in the dictionary put { in front of the
        word then .. then the english then .. then the source if any  }
        
        to add a note to a word place it after a ;

        notes: question ; answer
        words: egy word .. english word .. source .. note ..
        sentences: egy sent;; eng sent;; literal ;; source ;;

        to pick out sentences to put in the dictionary put { in
        front of the sentence, then ;; then the english then ;; then
        the literal. if there is no literal then just put an empty
        space then ;;  then the source }
        """

        self.open_files()
        self.get_atts()
        self.main_loop()
        self.add2questions()
        self.handle_particles()
        self.add_words()
        assert not self.mistakes
        self.save_files()


    def get_atts(self):
        self.questions = []
        self.mistakes = False
        self.new_words = []
        self.temp_grammar_test = []
        self.sents = []
        self.extraction = []
        self.remainder = ""
        self.temporary_sentences = []
        self.txt = hdir + 'grammar books/allen/allen_grammar.txt'
        self.main_source = 'allen'
        self.semantics_st = set(self.semantic_notes)

    def open_files(self):
        self.grammar_test = pi.open_pickle('grammar_test', 'hi')
        self.done_notes = set(to.from_txt2lst(fcdir + 'done_notes'))
        try:
            self.particles = pi.open_pickle('particles', 'hi')
        except:
            self.particles = {}

        try:
            self.semantic_notes = to.from_txt2lst(hdir + 'grammar notes/semantic_notes.txt')
        except:
            self.semantic_notes = []


    def save_files(self):
        str2 = 'temp_grammar_test'
        num = vgf.get_num_series(fcdir, str2)
        to.from_lst2txt(self.words2study, fcdir + 'words2study')
        pi.save_pickle(self.grammar_test, 'grammar_test', 'hi')
        pi.save_pickle(self.particles, 'particles', 'hi')
        to.from_lst2txt(self.temp_grammar_test, fcdir + f'temp_grammar_test{num}', 0)
        to.from_lst2txt(self.done_notes, fcdir + 'done_notes')
        to.from_lst2txt(self.temporary_sentences, fcdir + 'temporary_sentences', 0)
        to.from_lst2txt(self.semantic_notes, hdir +  'grammar notes/semantic_notes')


    def main_loop(self):
        f = open(self.txt, 'r+')
        self.all_lines = [x for x in f]
        f.close()
        self.semantics = False
        question = False
        e = 0

        while e < len(self.all_lines):
            self.line = self.all_lines[e]

            if '!!{' in self.line:
                bb = 8

            if question and "}" in self.line:
                e = self.handle_closed_paren(e)
                question = False

            elif question and not "}" in self.line:
                self.sents.append(self.line)

            elif not question and "{" in self.line:
                self.oidx = self.line.index('{') + 1
                self.is_semantic()
                question = True

                if '}' not in self.line:
                    half = self.line[self.oidx:]
                    self.oidx = 0
                    self.sents.append(half)
                else:
                    e = self.handle_closed_paren(e)
                    question = False

            e += 1

        return

    def is_semantic(self):
        if self.oidx > 1:
            if self.line[self.oidx -3:self.oidx-1] == '!!':
                self.semantics = True

    def handle_closed_paren(self, e):
        cidx = self.line.index("}")
        sent = self.line[self.oidx:cidx]
        if "{" in self.line[self.oidx:]:
            self.all_lines[e] = self.line[cidx + 1:]
            e -= 1

        self.sents.append(sent)
        str1 = "".join(self.sents)
        self.sents = []



        if str1 in self.done_notes:
            if self.semantics and str1 not in self.semantics_st:
                self.semantic_notes.append(str1)

        else:
            if ";;" in str1:
                if ".." in str1 or reg(r'[^;];[^;]', str1):
                    p(f'{str1} in wrong')
                    self.mistakes = True
                self.done_notes.add(str1)
                str1 = str1.replace(",", "")
                self.temporary_sentences.append(str1)
                oparen = str1.count("(")
                cparen = str1.count(")")
                if oparen != cparen:
                    self.mistakes = True
                    p (f"""
                    {str1}

                    does not have the right number of paren
                    """)


            elif ";" in str1:
                if str1.count(';') > 1:
                    p(f'{str1} in wrong')
                    self.mistakes = True
                self.questions.append(str1)
                self.done_notes.add(str1)



            elif "@" in str1 or " !" in str1 or \
                    "?" in str1:
                self.new_words.append(str1)
                self.done_notes.add(str1)

            elif str1[-2:] == '::':
                self.done_notes.add(str1)
                self.extraction.append(str1[:-2])

            elif self.semantics:
                self.semantic_notes.append(str1)
                self.done_notes.add(str1)

            else:
                p(f"""
                {str1} 
                IS WRONG
                """)
                self.mistakes = True
        self.semantics = False

        return e


    def add2questions(self):
        for e, str1 in en(self.questions):
            lst = str1.split(";")
            question = lst[0].strip()
            answer = lst[1].strip()
            if not reg(r'[a-zA-Z]', answer):
                p(f'{str1} has no answer')
                self.mistakes = True

            ins = other_tests()
            ins.word = question
            ins.eng_word = answer
            ins.nxt_tst = time.time()
            ins.source = self.main_source
            self.grammar_test[question] = ins
            self.temp_grammar_test.append(question)
        p(f'{len(self.questions)} grammar questions added')
        p(f'{len(self.temporary_sentences)} sentences added')


    def handle_particles(self):
        for line in self.extraction:
            idx = line.index('\n')
            question = line[:idx]
            question = question.strip()
            answer = line[idx+1:].strip()
            ins = other_tests()
            ins.word = question
            ins.eng_word = answer
            ins.nxt_tst = time.time()
            self.particles[question] = ins
        p (f'{len(self.extraction)} particles added')




    def add_words(self):
        #        words: egy word .. english word ..
        #        .. secondary source .. note .. main_source
        self.words2study = []
        self.new_meanings = []

        for e, line in en(self.new_words):
            ins = temp_word()
            ins.main_source = self.main_source
            if '@' in line:
                lst = vgf.strip_n_split(line, "@")
                ins.word = lst[0]
                ins.eng_word = lst[1]
                if not len(lst) == 4:
                    p('')
                    p(f'{ins.word} must have 4 categories')
                    p('')
                ins.source = lst[2]
                ins.pos = lst[3]
                self.new_meanings.append(ins)
        if self.new_meanings:
            self.add_new_meanings2(self.new_meanings)
        return

    def add_new_meanings2(self, lst):
        tle_dct = pi.open_pickle('tle_dct6', 'hi')
        word2lemma = pi.open_pickle('word2lemma', 'hi')
        for x in lst:
            lemma = handle_new_meanings(tle_dct, x)
            if lemma:
                x.lemma_no = lemma
                add_single_lemma(tle_dct, word2lemma,  x.word, x)
                p(f'added {x.word}')
        pi.save_pickle(tle_dct, 'tle_dct6', 'hi')


class vocab_tester(tle_entry):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return self.word


# 0 1 2 9 10 21
# 5 2 11 10 14 10 15 10 8 21
#

def print_entries(word, word2lemma, tle_dct):
    p("""
                """)
    lemmas = word2lemma.get(word)
    if not lemmas:
        p('not found')
    else:
        lemmas = list(lemmas)

        for e, lemma in en(lemmas):
            entry = tle_dct[lemma]
            pos = entry.pos
            word = entry.word
            rank = entry.rank
            p(e, lemma, pos, rank, word, entry.eng_word)
    p("""
            """)
    return lemmas



def look_up_word():
    p (f"""
    print 1 to input an egyptian word, 2 for an english word
    3 for alternative spellings of a specific lemma
    4 to update word2lemma and dictionary
    5 to print all idioms
    6 to look up by lemma
    q to quit
    """)


    word2lemma = pi.open_pickle('word2lemma', 'hi')
    tle_dct = pi.open_pickle('tle_dct6', 'hi')
    lemma2freq = pi.open_pickle('lemma2freq', 'hi')
    word2def = build_searchable_english(tle_dct)

    while True:
        new_word = input('word: ')
        try:
            if not reg(r'^(1|2|3|4|5|6|7|q)', new_word):
                p ('wrong input')
            else:
                word2lookup = new_word[2:]
                if new_word[0] == 'q':
                    return
                if new_word[0] == '1':
                    lemmas = print_entries(word2lookup, word2lemma, tle_dct)
                elif new_word[0] == '2':
                    search_by_english(word2def, tle_dct, word2lookup)
                elif new_word[0] == '3':
                    print_alt_spellings(lemmas, word2lookup, lemma2freq)
                elif new_word[0] == '4':
                    word2lemma = pi.open_pickle('word2lemma', 'hi')
                    tle_dct = pi.open_pickle('tle_dct6', 'hi')
                elif new_word[0] == '5':
                    for x in tle_dct.values():
                        if x.pos == 'x':
                            p (x.lemma_no, x.word)
                elif new_word[0] == '6':
                    lemma = int(new_word[2:])
                    entry = tle_dct[lemma]
                    p(entry.ger_word)
                    p (entry.word)
                    p (entry.eng_word)
                    p (entry.rank)
                    p (entry.pos)
                p(f"""

print 1 to input an egyptian word, 
2 for an english word
3 for alternative spellings of a specific lemma
4 to update word2lemma and dictionary
5 to print all idioms
6 to look up by lemma
q to quit
                """)

        except:
            p ('wrong input')



def print_alt_spellings(lemmas, word2lookup, lemma2freq):
    try:
        num = int(word2lookup)
        lemma = lemmas[num]
        dct = lemma2freq[lemma]
        for x, y in dct.items():
            p (x, y)
    except:
        p ('wrong input')



def search_by_english(word2def, tle_dct, word2lookup, pos = ""):
    lst = word2def.get(word2lookup)
    if not lst:
        p('not used')
    else:

        if not pos:
            for x in lst:
                p(x)
                p('')
        else:
            found = False
            for x in lst:
                entry = tle_dct[x[0]]
                pos1 = entry['pos']
                if pos1 == pos:
                    p(x)
                    p('')
                    found = True
            if not found:
                p('none with specific pos')


def build_searchable_english(tle_dct={}):
    if not tle_dct:
        tle_dct = pi.open_pickle('tle_dct6', 'hi')

    obj = r'[\(\);,\.:\{\}\[\]\?\/!<>]'
    word2def = {}

    all_words = set()
    for k, v in tle_dct.items():
        word = v.eng_word
        word = word.replace('&#39;', "'")
        word = word.replace('&amp;', 'or')
        oword = word
        word = re.sub(obj, " ", word)
        word = word.lower()
        words = word.split()
        words = [x for x in words if x]

        all_words |= set(words)
        for x in words:
            lemma = v.lemma_no
            rank = v.rank
            egy_word = v.word
            word2def.setdefault(x, []).append([lemma, egy_word, rank, oword])

    return word2def


def add_sent2dct():
    dct_cls = pi.open_pickle('dictionary', 'hi')
    p("write the egyptian, then the english separated by |"
      "then the literal if any separated by |")

    while True:
        str1 = input('sentence: ')
        lst = str1.split(' | ')
        ins = vocab_tester()
        ins.nxt_tst = time.time()
        ins.word = lst[0]
        ins.eng_word = lst[1]
        try:
            ins.elit = lst[2]
        except:
            pass
        v = to.from_cls2dict(ins)
        dct_cls[ins.word] = v
        pi.save_pickle('dictionary', 'hi')


def add_new_meanings():
    lst = pi.open_pickle('new_meanings', 'hi')
    tle_dct = pi.open_pickle('tle_dct6', 'hi')

    for x in lst:
        handle_new_meanings(tle_dct, x)
        p(f'added {x.word}')
    pi.save_pickle(tle_dct, 'tle_dct6', 'hi')


def handle_new_meanings(tle_dct, ins):
    st = {v.word + v.eng_word for k, v in tle_dct.items() if int(k) > 1_000_000}
    entry = tle_entry()
    entry.word = ins.word
    lemma = str(max([int(x) for x in tle_dct.keys()]) + 1)
    entry.lemma_no = lemma
    entry.eng_word = ins.eng_word
    entry.secondary_source = ins.secondary_source
    entry.pos = ins.pos
    entry.lemma_n_word = f"{entry.lemma_no} {ins.word}"
    str1 = entry.word + entry.eng_word
    if str1 not in st:
        tle_dct[lemma] = entry
        return lemma
    else:
        return 0


def put_pos():
    '''
    todo: pronouns need to be either demonstrative or personal
    particles need to be either enclitic or nonenclitic
    numbers need to be cardinal or ordinal
    nouns need to be either common or proper
    '''




    dct = {
        'adjective_no_nisba': 'jnn',
        'nisba_from_preposition': 'jp',
        'nisba_from_noun': 'jn',
        "adverbs_from_prepositions": "rp",
        'verbs': "v",
        'adverbs': "r",
        'prepositions': "i",
        'pronouns': "p",
        'demonstrative_pronouns': "pd",
        'personal_pronouns': "pp",
        'relative': "c",
        'interrogative': "q",
        'particles': "e",  # to be deleted
        'enclitic_particles': "ee",
        'nonenclitic_particles': "en",
        'numerals': "m",  # to be deleted
        'cardinal_numbers': "mc",
        'ordinal_numbers': "md",
        'interjections': "w",
        'animals_institutions': 'nc',
        'personal_names': 'npc',
        'titles_of_private_persons': 'npt',
        'epithets_of_kings': 'npke',
        'names of gods': 'npg',
        'nouns_no_names': 'nc',  # to be deleted
        'royal_names': 'npk',
        'toponyms': 'npp',
        'conjunctions': 'c',
        'other': 'o',
        'unknown': 'u',
        'relative pronoun': 'cp'
    }
    """
        

        Subst., m. # ncm
        Rel. Pron. # cp
        card. Zahl # mc
        Nisbe-Adj. (Subst.) # jn
        Titel # npt
        Name e. Tieres # npa
        Vb., 2rad # v2
        Vb., 3rad. # v3
        Personenname # npc
        Subst. # nc
        Vb., caus. 3rad. # vc3
        Vb., 3ae gem. # vg3
        Dem. Pron. # pd
        Ortsname # npp
        Vb., 5ae inf.
        Vb.
        Interr. Pron. # q
        Königsname # npk
        Vb., caus. 2ae gem.
        Nisbe-Adj. (Präp.) # jp
        Adj. # j
        Epitheton e. Gottheit # npge
        Vb., caus 4rad.
        Partikel # e
        Subst., f. # ncf
        Göttername # npg
        Präp.-Adv. # rp
        Adv. # r
        Zahl # m
        Präp. # i
        Vb., 5rad.
        Vb., anom.
        ord. Zahl # md
        Vb., 4rad.
        Vb., 4ae inf.
        Epitheton d. Königs # npke
        Interj. # w
        Name e. Sache o. Institution # ncnh
        Pers. Pron. # pp
        Vb., caus. 2rad.
        Pron. # p
        Vb., caus 4ae inf.
        Vb., 3ae inf.
        Vb., caus. 3ae inf.
        Vb., 2ae gem.
        Vb., 2rad # v2
        Vb., 3rad. # v3
        Vb., caus. 3rad. # vc3
        Vb., 3ae gem. # vg3
        Vb., 5ae inf. # vi5
        Vb. # v
        Vb., caus. 2ae gem. # vcg2
        Vb., caus 4rad. # vc4
        Vb., 5rad. # v5
        Vb., caus. 5rad. # vc5
        Vb., 6rad. # v6
        Vb., anom. # va
        Vb., 4rad. # v4
        Vb., 4ae inf. # vi4
        Vb., caus. 2rad. # vc2
        Vb., caus 4ae inf. # vci4
        Vb., 3ae inf. # vi3
        Vb., caus. 3ae inf. # vci3
        Vb., 2ae gem. # vg2
            
    """
    lst1 = []
    for x in allen2:
        if on:
            lst1.append(x)
        if 'tttt' in x:
            on = True
        elif 'ssss' in x:
            break


def add_braces2allen():
    allen = open(hdir + 'grammar books/allen/allen_grammar.txt', 'r+')
    lst = []
    found = False
    for x in allen:
        if found:
            if x and x[0].isdigit():
                idx = x.index(' ')
                idx1 = x.index(open_apost)
                num = x[:idx]
                question = x[idx:idx1]
                question = question.replace(',', '')
                x = num +  '{' + question + ";;" + x[idx1:-1] + "}\n"
                lst.append(x)
            else:
                lst.append(x)
        else:
            lst.append(x)

        if 'brace_start' in x:
            found = True
        if 'brace_end' in x:
            found = False
    allen.close()

    to.from_lst2txt(lst, hdir + 'grammar books/allen/allen_grammar', 1)
    vgf.open_txt_file(hdir + 'grammar books/allen/allen_grammar.txt')


def save_tle_rank():
    tle_dct = pi.open_pickle('tle_dct6', 'hi')
    get_freq_by_rank(tle_dct)
    pi.save_pickle(tle_dct, 'tle_dct6', 'hi')


def get_freq_by_rank(tle_dct):
    dct1 = {k: v.frequency for k, v in tle_dct.items()}
    dct1 = sort_dict_by_val_rev_dct(dct1)
    dct2 = {e: k for e, k in en(list(dct1.keys()))}
    total = len(dct1)
    freq = 0
    last_num = 0
    for k, v in dct2.items():
        entry = tle_dct[v]
        freq = entry.frequency
        if freq == 1:
            rank = 1
        else:
            if freq != last_num:
                rank = 100 - int((k / total) * 100)
            else:
                rank = 100 - int((last_rank / total) * 100)

            last_num = freq
            last_rank = k
        tle_dct[v].rank = rank

    return


def use_new_definitions():
    dct_cls = pi.open_pickle('dictionary', 'hi')
    tle_dct = pi.open_pickle('tle_dct6', 'hi')
    get_freq_by_rank(tle_dct)

    for x, y in dct_cls.items():
        defins = []

        for lemma in y.lemma_no:

            entry = tle_dct.get(lemma)
            if entry:
                pos = entry.pos
                rank = entry.rank
                eng = entry.eng_word
                tpl = (lemma, pos, rank, eng)
                defins.append(tpl)

        y.eng_word = defins
        dct_cls[x] = y

    pi.save_pickle(dct_cls, 'dictionary', 'hi')

    return


def get_pro_spell(tle_dct):
    pro_spell = {}
    for x, v in tle_dct.items():
        pro_spell.setdefault(v.word, []).append(v.lemma_no)

    pi.save_pickle(pro_spell, 'pro_spell2lemma', 'hi')
    return pro_spell


def get_test_words_by_interval(start=0):
    temp_sentences_test = []
    dct_cls = pi.open_pickle('dictionary', 'hi')
    for x, y in dct_cls.items():
        if y.nxt_tst > time.time() - (34 * 60) and y.nxt_tst < time.time():
            temp_sentences_test.append(x)
            p(x)

    lst = pi.open_pickle('words2add', 'hi')
    for x in lst:
        if x in dct_cls:
            p(x)
            temp_sentences_test.append(x)

    pi.save_pickle(temp_sentences_test, 'temp_words_test7', 'hi')


def from_div2eng(english):
    english = [x for x in english if reg(r'\S', x)]
    long_str = " ".join(english)
    lst = vgf.strip_n_split(long_str, "|")
    return lst[:-1]






def fix_dct():
    dct_cls = pi.open_pickle('dictionary', 'hi')
    dct_cls['ntt']['eng_word'] += '\n f.s independent pronoun'
    dct_cls['twt']['eng_word'] += 'statue'

    dct2 = {
        'Hnqt': 'Hnq.t',
        'jAbtt': 'jAb.tjt',

    }
    dct3 = {
        'mnD': 'chest, breast, udder',
        'pXr.t': 'remedy'
    }
    for k, v in dct2.items():
        obj = dct_cls[k]
        obj['word'] = v
        del dct_cls[k]
        dct_cls[v] = obj

    for k, v in dct3.items():
        dct_cls[k]['eng_word'] = v

    del dct_cls['dpt']
    pi.save_pickle(dct_cls, 'dictionary', 'hi')


def change_interval():
    if ins.nxt_tst < time.time() \
            and ins.nxt_tst > time.time() - (6 * 60 * 60):
        ins.nxt_tst = time.time()
    elif ins.nxt_tst < time.time():
        ins.nxt_tst = time.time() + (3 * 60 * 60)


## n10 didn't get the phonogram of n9

## the second fence is not in my database
# sudo chmod -R a+rw /volumes/macintosh\ hd/applications/JSesh-7.3.2/
# sudo chown -R kylefoley /volumes/macintosh\ hd/applications/JSesh-7.3.2/
# chmod a+rw /volumes/macintosh\ hd/applications/JSesh-7.3.2/jsesh.app/contents/jre
def open_jsesh():
    import subprocess
    print('trying to open')
    str6 = "/users/kylefoley/downloads/hieroglyphs/biliterals.pdf"
    str1 = "/users/kylefoley/downloads/hieroglyphs/bod.gly"
    str2 = "JSesh-7.3.2"
    str3 = '/volumes/macintosh hd/applications/'
    str4 = '/volumes/macintosh hd/applications/JSesh-7.3.2/jsesh.app'
    str5 = '/volumes/macintosh hd/applications/preview.app'
    # p = subprocess.Popen([str5, str6])
    p = subprocess.call(['open', str1])
    time.sleep(10)
    returncode = p.wait()
    return


def temp17():
    tle_dct = pi.open_pickle('tle_dct6', 'hi')
    dct_cls = pi.open_pickle('dct_cls', 'hi')
    done = False
    del tle_dct['1000023']
    del tle_dct['1000003']
    tle_dct['1000019'].word = 'Xr-HA.t'
    pi.save_pickle(tle_dct, 'tle_dct6', 'hi')
    obj = dct_cls['rkH-nDs']

    for k, v in dct_cls.items():
        lst = v.eng_word

        if not lst:
            p(f"""

            {k, v.ger_word}
            """)


    pi.save_pickle(dct_cls, 'dictionary', 'hi')
    return


def use_tle_index():
    p ("""
    1 to search up to three words in a row in name
    2 to search up to three words in a row in bibliography
    3 to search any set of words in name
    4 to search any set of words in bibliography
    5 names of txt
    """)

    idx = pi.open_pickle('tle_index', 'hi')
    texts = pi.open_pickle('tle_txts5', 'hi')
    empty_txts = pi.open_pickle('finished_texts6','hi')[1]

    by_name = idx[0]
    by_bib = idx[1]
    while True:
        # try:
        str1 = input('input: ')
        if str1 == 'q':
            return
        assert str1[0] in ['1', '2']
        kind = str1[0]
        word = str1[2:]
        if kind == '1':
            dct = by_name
        elif kind == '2':
            dct = by_bib
        elif kind == '5':
            pass

        lst = dct.get(word)
        if lst:
            for x in lst:

                if x in empty_txts:
                    dct = empty_txts
                    str1 = 'empty'
                else:
                    str1 = ""
                    dct = texts

                obj = dct.get(x)

                if kind == '1':
                    p(obj.number, str1, obj.name)

                elif kind == '2':
                    p(obj.number,str1, obj.bibliography)
        # except:
        #     p('wrong input')


class digitize_books:
    def __init__(self):
        dir1 = "/users/kylefoley/downloads/hieroglyphs/st_andrews/"
        file = dir1 + "seni_viceroy_of_cush.pdf"
        lst = to.from_pdf2list(file)
        bb = 8


# delete jp.t from new lemmas, add meaning 'select'
# delete 1_000_014, 1_000_016, make 74300 rewrite def as measuring device
# figure out what's wrong with wA.t
"""
rnp.t-Hsb : regnal year
delete: 1_000_038
delete: 1_000_009
1_000_059 pos is ep not pn
1_000_048 is alt spelling for sr

bjAw does not need new entry, it is 54340

delete xt as meaning future replace with
m-x.t meaning 'the future, or 'wake'

1,000,105 is probably 854561
nswty - does not have an english meaning
"""

if eval(not_execute_on_import):

    args = vgf.get_arguments()

    if 'tn' in args:
        transfer_notes()

    elif 'anm' in args:
        add_new_meanings()

    elif 'aba' in args:
        add_braces2allen()

    elif 'ti' in args:
        use_tle_index()

    elif 'gbi' in args:
        get_test_words_by_interval()

    elif 'und' in args:
        use_new_definitions()

    elif 'amw' in args:
        all_my_words()

    elif 'sr' in args:
        save_tle_rank()

    elif 'lu' in args:
        look_up_word()

    elif 'db' in args:
        digitize_books()
