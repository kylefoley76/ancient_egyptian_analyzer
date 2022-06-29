import add_path
from general import *
import random
import pyautogui, time, shutil
import webbrowser as wbb
import codecs
from google.cloud import translate
from global_hiero import *
from selenium import webdriver as wbs
import pyperclip


### 14500 files, 251859 words
### 19400 330,000


def scan_book_by_scroll():
    time.sleep(1.5)
    b = 1038
    # im = pyautogui.screenshot(hdir + f"faulkner_dct/{b}.png")
    # db()

    while b < 400 + 1038 and pi.open_pickle('bool2'):
        b += 1
        pyautogui.scroll(-15)
        time.sleep(.5)
        im = pyautogui.screenshot(hdir + f"faulkner_dct/{b}.png")
        time.sleep(1.5)
        # im = pyautogui.screenshot(hdir + f"faulkner_dct/{b}.png")
        #
        # time.sleep(1)




def scroll_down():
    b = 0
    time.sleep(1)
    while pi.open_pickle('bool1'):
        pyautogui.scroll(-3)
        time.sleep(3)
        b += 1
        vgf.print_intervals(b, 10)


class tle_file:
    def __init__(self):
        self.date = ""
        self.object_type = ""
        self.provenance = ""
        self.script = ""
        self.certainty = []
        self.bibliography = ""
        self.present_location = ""
        self.line_count = ""
        self.hierarchy = ""
        self.name = ""
        self.has_ending = False
        self.number = ""
        self.type_of_text = ""
        self.type_of_object = ""
        self.has_notes = False
        self.has_illustration = False
        self.lemmas = []
        self.translator = ""
        self.translit2german = []
        self.translit2english = []
        self.translit_n_info = []
        self.has_glyphs = False
        self.word_count = 0

    def __repr__(self):
        return self.number




def write_roman_numerals(num):
    roman = {}
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])


def translate_tle_txt():
    # texts = pi.open_pickle('texts', 'hi')
    str1 = hdir + 'My First Project-7a3577f30498.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str1
    trans_client = translate.Client()

    tle_dct = pi.open_pickle('tle_dictionary3', 'hi')

    dct1 = pi.open_pickle('abb2english', 'hi')
    del dct1['m.']
    dct1['L.H.G'] = 'life, salvation, and health'
    abb2english = {}
    for k, v in dct1.items():
        if v not in ['-1', 'ignore', 'delete']:
            abb2english[k] = v
        elif 'soemone' in v:
            v = v.replace('soemone', 'someone')

    abb = {
        'o.äg': 'upper egypt',
        'o. Ä.': 'upper egypt',
        'u.äg': 'lower egypt',
        'Bez.': "district",
        'temp.': 'temporal',
        'jmdm': 'someone',
        'jmd.': 'someone',
        'lok.': 'regional',
        'Konj.': 'conjunctive',
        'Präs': 'present',
        'u. Ä': 'lower egypt',
        'u. a.': 'lower egypt',
        'O. Äg.': 'upper egypt',
    }

    abb2english = merge_2dicts(abb, abb2english)

    ro_num = [write_roman_numerals(x) for x in range(1, 50)]
    ro_num_abb = {x + ".": str(800 + e) for e, x in en(ro_num)}

    abb2english = vgf.sort_dct_keys_by_len(abb2english)
    ro_num_abb = vgf.sort_dct_keys_by_len(ro_num_abb)

    ger2lemma = {}
    for k, v in tle_dct.items():
        ger2lemma.setdefault(v['ger_word'], []).append(v['lemma_no'])

    old2new = {k: k for k, v in ger2lemma.items()}

    for k, v in old2new.items():
        for x, y in ro_num_abb.items():
            v = v.replace(x, y)
        for x, y in abb2english.items():
            v = v.replace(x, y)

        b = re.findall(r'\d\.', v)
        if b:
            for z in b:
                c = z.replace(".", "")
                v = v.replace(z, c)

        old2new[k] = v

    lsts = []
    total = 0
    dct9 = {}
    for x, y in old2new.items():
        total += len(y)
        if total > 1700:
            lsts.append(jsonc(dct9))
            dct9 = {}
            total = 0
        else:
            dct9[x] = y

    all_mistakes = pi.open_pickle('wrong_trans3', 'hi')
    old2new2 = pi.open_pickle('words_trans7', 'hi')

    remainder = set(old2new.keys()) - set(old2new2.keys())
    remainder = {k: old2new[k] for k in remainder}
    pi.save_pickle(remainder, 'to_be_translated')

    failed_translation = set()
    b = 0
    for k, v in remainder.items():
        try:
            eng = trans_client.translate(v, target_language='en', source_language='de')
            translated = eng['translatedText']
            old2new2[k] = translated
        except:
            p(f'{k} did not translation')
            failed_translation.add(k)
        b += 1
        vgf.print_intervals(b, 50, 0, len(remainder))
        time.sleep(.33)

    pi.save_pickle(old2new2, 'words_trans7', 'hi')
    pi.save_pickle(failed_translation, 'failed_translation', 'hi')

    for k, v in old2new2.items():
        for x, y in ro_num_abb.items():
            v = v.replace(y, x)
            old2new2[k] = v

    for k, v in tle_dct.items():
        if not v['eng_word']:
            obj = old2new2.get(v['ger_word'])
            if obj:
                v['eng_word'] = obj
            else:
                p(f'the word {v["ger_word"]} was not translated')
                if v['ger_word'] not in failed_translation:
                    failed_translation.add(v['ger_word'])

    pi.save_pickle(tle_dct, 'tle_dictionary4', 'hi')
    pi.save_pickle(failed_translation, 'failed_translation', 'hi')

    bb = 8


class short_test:
    def __init__(self):
        self.freq = 0
        self.pos = ""
        self.ger_word = ""


class tle_entry:
    #atts = ['first_read', 'original', 'recon', 'word_recon',
     #       'pg', 'alt_spellings', 'encount_alt_spellings']
    def __init__(self):
        self.word = ""
        self.abb_english = set()
        self.eng_word = ""
        self.first_read = ""
        self.lemma_no = ""
        self.lemma_n_word = ""
        self.ger_word = ""
        self.frequency = 0
        self.kind = ''
        self.pos = ""
        self.original = ''
        self.nxt_tst = -2
        self.scores = []
        self.secondary_source = ''
        self.recon = ""
        self.minimal_context = []
        self.word_recon = ""
        self.notes = ""
        self.rank = 0
        self.main_source = ''
        self.pg = 0
        self.elit = ""
        self.sub_terms = []
        self.super_terms = []
        self.alt_spellings = {}
        self.encount_alt_spelling = []

    def __repr__(self):
        return self.lemma_n_word


def has_middle():
    middles = []
    files = pi.open_pickle('raw_files', 'hi')
    ftxts = pi.open_pickle('finished_texts2', 'hi')
    processed_files = ftxts[0]
    non_middles = []

    for x, y in files.items():
        if x[-1] == 'l':
            num = x[:-1]
            if num == '19038':
                bb = 8

            orig_file = processed_files[num]
            for line in y:
                if '</td><td>' in line:
                    line = vgf.use_beautiful_soup(line, 1)
                    all_german = set(orig_file.translit2german.values())
                    if line not in all_german:
                        middles.append(x[:-1])
                    else:
                        non_middles.append(x[:-1])
                    break

    p(len(middles))
    pi.save_pickle(middles, 'middles', 'hi')

    return


def eliminate_bad_middle():
    st = set()
    bad_files = pi.open_pickle('bad_files', 'hi')
    for x in bad_files:
        idx = x.index('m')
        st.add(x[:idx])

    b = 0
    dir1 = hdir + 'tle/texts/'
    for num in st:
        for file in os.listdir(dir1):
            if file.startswith(num) and reg(r'm(\d)+\.html', file):
                full_name = dir1 + file
                os.remove(full_name)
                prefix = file[:-5]
                folder = dir1 + prefix + '_files'
                shutil.rmtree(folder)
                b += 1

    return


def test_middle():
    parsed_files = pi.open_pickle('parsed_files', 'hi')
    dct1 = {}
    b = 0
    for x in parsed_files.keys():
        if 'm' in x:
            idx = x.index('m')
            first = x[:idx]
            last = x[idx + 1:]
            dct1.setdefault(first, []).append(int(last))
            b += 1

    bad_files = {}
    good_files = {}
    for x, y in dct1.items():
        num = max(y)
        name = x + "m" + str(num)
        file = parsed_files[name]
        if all('display at beginning' not in z for z in file):
            bad_files[name] = file
        else:
            good_files[name] = file

    return


class process_tle:
    def __init__(self):
        ## types 22701, tokens 2323462
        self.files = {}
        self.total = 0
        self.total_german = 0
        self.total_empty = 0
        self.all_words = 0
        self.parsed_files = {}
        self.full = {}
        self.kind = ""
        self.words2entry = {}

    def check_version(self):
        self.parsed_files = pi.open_pickle('parsed_files', 'hi')
        # self.raw_files = pi.open_pickle('raw_files','hi')
        self.check_headers()

    def process_dct_entries(self):
        self.parsed_files = pi.open_pickle('parsed_def', 'hi')
        self.files = pi.open_pickle('raw_dct_entries', 'hi')
        self.get_files('dict_entries')
        pi.save_pickle(self.parsed_files, 'parsed_def', 'hi')
        pi.save_pickle(self.files, 'raw_files', 'hi')

    def get_gerpos2engpos(self):
        f = open(hdir + 'germ_pos2eng_pos.txt', 'r+')
        self.gp2ep = {}
        for line in f:
            if "#" in line:
                x, y = line.split('#')
                self.gp2ep[x.strip()] = y.strip()
        f.close()

    def parse_dct_entries(self):
        self.parsed_files = pi.open_pickle('parsed_def', 'hi')
        self.raw_files = pi.open_pickle('raw_dct_entries', 'hi')
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')
        self.get_gerpos2engpos()
        self.changed = set()
        p('num parsed files')
        p(len(self.parsed_files))
        st_pos = set()
        self.untranslated = {}
        lemma_not_match = set()
        b = 0
        self.subs_found = 0
        self.sub_not_found = 0
        ndef = 0
        for file_name, self.file in self.parsed_files.items():
            found = False
            t = int(file_name)
            if t < 1_000_000:
                b += 1
                tle_entry = self.tle_dct[file_name]
                self.e = 0
                while self.e < len(self.file):
                    self.line = self.file[self.e]
                    if self.line:
                        if "lemma-no" in self.line:
                            line = self.line[1:-1]
                            idx = line.index(' ')
                            lemma = line[idx:].strip()
                            self.changed.add(lemma)
                            if lemma != file_name:
                                lemma_not_match.add(file_name)
                                lemma_not_match.add(lemma)
                                break
                            else:
                                found = True

                        if 'information for lemma' in self.line:
                            self.cut_line_left('information for lemma')
                            self.line = self.line.strip()
                            if self.line != tle_entry.word:
                                pass
                                # p ('')
                                # p(f'changed word in {file_name}')
                                # p (f'new word {self.line}')
                                # p (f'old word {tle_entry.word}')
                                # p ("")

                        if 'translation' == self.line:
                            if not found:
                                p(f'error in file {lemma}')
                            self.increase_one()
                            self.loop_until_txt()
                            tle_entry.ger_word = self.line
                            self.increase_one()
                            while not self.line and not self.line.startswith('short ref'):
                                self.e += 1
                                self.line = self.file[self.e]

                            if not self.line.startswith('short ref'):
                                ndef += 1
                                if self.line[0] == "(":
                                    self.line = self.line[1:]
                                if self.line[-1] == ")":
                                    self.line = self.line[:-1]

                                tle_entry.eng_word = self.line
                                # p (f"""
                                #
                                # {self.line}
                                #
                                # """)
                            else:
                                self.untranslated[tle_entry.lemma_no] = [tle_entry.ger_word, tle_entry.eng_word]

                                tle_entry.eng_word += '*'
                                tle_entry.main_source = self.line

                        if self.line.startswith('short refe'):
                            self.increase_one()
                            self.loop_until_txt()
                            tle_entry.main_source = self.line

                        if 'hierarchically subordinate' in self.line:
                            lst = []
                            self.increase_one()
                            while self.line and 'for this word' not in self.line:
                                slemma = self.get_subordinates(file_name)
                                if slemma:
                                    lst.append(slemma)

                                self.e += 1
                                self.line = self.file[self.e]
                            tle_entry.super_terms = lst

                        if self.line.startswith('word class'):
                            self.increase_one()
                            self.loop_until_txt()
                            try:
                                tle_entry.pos = self.gp2ep[self.line.strip()]
                            except:
                                p("")
                                p(f'new pos {self.line}')
                                p("")
                            st_pos.add(self.line)

                        if 'attestation' in self.line and \
                                self.line[0].isdigit():
                            idx = self.line.index(" ")
                            num = self.line[:idx]
                            if tle_entry.frequency != int(num):
                                pass
                            tle_entry.frequency = int(num)

                    self.e += 1

        p(f'{ndef} translations')
        p(lemma_not_match)
        self.handle_non_tran()

        pi.save_pickle(self.tle_dct, 'tle_dct6', 'hi')
        return

    def handle_non_tran(self):
        lst = []
        dct1 = {}
        for x, y in self.untranslated.items():
            entry = self.tle_dct[x]
            freq = entry.frequency
            str1 = [x] + y
            str1 = " | ".join(str1)
            dct1[str1] = freq
        dct1 = sort_dict_by_val_rev_dct(dct1)
        for x, y in dct1.items():
            str1 = x + " | " + str(y)
            lst.append(str1)
        to.from_lst2txt(lst, hdir + 'untranslated.txt')
        vgf.open_txt_file(hdir + 'untranslated.txt')

    def get_subordinates(self, file_name):
        if '"' not in self.line:

            # p (f'{file_name} not a true subordinate')
            return False
        else:
            idx = self.line.index('"')
            egyptian = self.line[:idx]
            german = self.line[idx + 1:]
            idx = german.index('"')
            german = german[:idx].strip()
            egyptian = egyptian.strip()

            for x, y in self.tle_dct.items():
                if y.word == egyptian:
                    first_half = len(y.ger_word)
                    c = first_half // 2
                    tle_ger = y.ger_word

                    if german.startswith(tle_ger[:c]):
                        self.subs_found += 1
                        return y.lemma_no

            self.sub_not_found += 1

            return 0


    def temp11(self):
        self.bad_files3 = []
        for x in self.bad_files2:
            for y in self.parsed_files.keys():
                b = r"^" + re.escape(x) + r'm\d'
                if re.search(b, y, re.IGNORECASE):
                    p(y)
                    self.bad_files3.append(y)
        to.from_lst2txt(self.bad_files3, hdirp + 'bad_files9')

    def temp13(self):
        st = set(self.parsed_files.keys()) - set(self.files.keys())
        raw_files3 = pi.open_pickle('raw_files3', 'hi')
        for x in st:
            self.files[x] = raw_files3[x]
            raw = raw_files3[x]
            # parsed = self.parsed_files[x]
            # p (len(raw), len(parsed))


    def main_text(self):
        kind = ''
        self.destroyed = ['détruit',
                          'destroyed',
                          "Zerstört",
                          'Lücke',
                          'Zerstörung',
                          'zerstört',
                          'Zeichenrest',
                          'Zerstsörung'
                          'fehlt',
                          'unklar',
                          'lacune',
                          'lacuna',
                          'verloren',
                          'Zeichenspur',
                          'detruite',
                          'unleserlich',
                          'Spur',
                          'perdu',
                          'getilgt',
                          'abgebrochen',
                          'Zerstörurng',
                          ]

        self.interspersed = set()
        self.translators = set()


        self.bad_files = []
        self.no_name = []
        self.empty_middle = {}
        self.no_name = []
        # self.bad_files = pi.open_pickle('bad_files', 'hi')
        # self.bad_files = []
        self.destroyed_lines = set()
        self.get_tle_translators()
        if kind == 'gapped':
            self.parsed_files = pi.open_pickle('gapped_files', 'hi')
            self.files = pi.open_pickle('raw_gaps', 'hi')
        else:
            self.parsed_files = pi.open_pickle('parsed_files2', 'hi')
            self.files = pi.open_pickle('raw_files2', 'hi')
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')


        if kind == 'gapped':
            self.processed = {}
            self.empty = {}
            finished = []
        else:
            finished = []

            finished = pi.open_pickle('finished_texts7', 'hi')

            self.processed = finished[0]
            self.empty = finished[1]
        # if kind == '':
        #     del self.parsed_files['6733l']

        self.first()
        # p(self.all_words)
        # p(self.total_german)
        b = len(self.parsed_files)
        c = len(self.empty) + len(self.processed)
        # p(b - c)
        # p (len(self.empty))
        pp (self.empty.keys())

        if kind == 'gapped':
            pi.save_pickle(self.processed, 'processed_gaps3', 'hi')
            # pi.save_pickle(self.bad_files, 'bad_files', 'hi')

        else:
            pass
            pi.save_pickle([self.processed, self.empty], 'finished_texts7', 'hi')
            # pi.save_pickle(self.bad_files, 'bad_files', 'hi')
            # pi.save_pickle(self.no_name, 'no_name', 'hi')

    def count_words2(self, second = False):
        b = 0
        for x, y in self.processed.items():
            if not second or 'l' not in x and 'm' not in x:
                for z in y.translit_n_info:
                    try:
                        for rw in z:
                            num = rw[0]
                            c = int(num)
                            if c > 0:
                                b += 1
                    except:
                        pass
        p(f'words {b}')

    def temp27(self):
        b = 0
        for x, y in txts.items():
            for z in y.translit_n_info:
                try:
                    for rw in z:
                        num = rw[0]
                        c = int(num)
                        if c > 0:
                            b += 1
                except:
                    pass
        p(f'words {b}')




    def link_info2translit(self):
        b = 0
        c = 0
        for x, y in self.processed.items():
            if len(y.translit2german) > 1:
                c += 1
                info, space_word = self.info_tpl(y.translit_n_info2)

                translit = self.translit_tpl(space_word, y.translit2german2)

        p(b / c)
        return

    def elim_bold(self, str1):
        if str1 not in self.bwords and reg(r'^b.*b$', str1):
            return str1[1:-1]

        if reg(r'\[b.*b\]', str1):
            str1 = str1.replace("[b", "")
            str1 = str1.replace("b]", "")

        return str1

    def elim_bold2(self):
        for x, y in self.processed.items():
            if x == '8139':
                bb = 8

            y.translit_n_info2 = jsonc(y.translit_n_info)
            y.translit2german2 = jsonc(y.translit2german)

            self.elim_bold3(y.translit2german2, 0)
            self.elim_bold3(y.translit_n_info2, 1)

            bb = 8

        return

    def elim_bold3(self, lst5, col):

        for e, lst in en(lst5):
            word = lst[col]
            if e == 10:
                bb = 8

            if col == 1 and int(lst[0]) > 0 or col == 0:

                if type(word) == str:
                    word = self.elim_bold(word)
                    word = re.sub(r'[^a-zA-Z0-9\s]', "", word)

                    if word:
                        word = word.strip()

                        # if word != lst[1]:
                        #     bb = 8

            lst[col] = word

    def check_repeats(self, info, d):
        done = info[:d]
        done = [x[0] for x in done]
        done = " ".join(done)
        not_done = info[d:]
        str1 = not_done[0][0]
        f = d

        if str1 not in done:
            return f
        else:
            for x in not_done[1:]:
                str1 += " " + x[0]
                if str1 in done:
                    f += 1
                else:
                    return f + 1

        return f + 1

    def info_tpl(self, translit_n_info):
        lst1 = []
        space_word = set()
        for e, word in en(translit_n_info):
            lemma = word[0]
            if int(lemma) > 0:
                word = word[1]
                word = re.sub(r'[^a-zA-Z0-9]', "", word)
                if " " in word:
                    space_word.add(word)
                lst1.append([word, e])
        return lst1, space_word

    def translit_tpl(self, space_word, translit2german):
        lst1 = []
        e = 0
        for so_word in space_word:
            so_word2 = so_word.replace(' ', "%")
            translit2german = translit2german.replace(so_word, so_word2)

        for str1, _ in translit2german:
            if str1 != 0:
                lst = str1.split()
                for word in lst:
                    if word not in ['..', '...']:
                        if "%" in word:
                            word = word.replace(" ", "%")
                        lst1.append([word, e])
            e += 1
        return lst1

    def get_b_words(self):
        self.tle = pi.open_pickle('tle_dct6', 'hi')
        self.bwords = set()
        for y in self.tle.values():
            if reg(r'^b.*b$', y.word):
                word = re.sub(r'[^a-zA-Z0-9]', "", y.word)
                self.bwords.add(word)

    def link_middles(self):
        finished2 = pi.open_pickle('finished_texts7', 'hi')
        finished = pi.open_pickle('finished_texts6', 'hi')
        self.processed_gaps = pi.open_pickle('processed_gaps3', 'hi')
        self.processed = finished[0]
        for x, y in finished2[0].items():
            self.processed[x] = y

        self.all_spaces = set()
        # start = time.time()
        # self.get_b_words()
        # self.elim_bold2()
        # p (time.time()- start)
        # self.link_info2translit()
        self.count_words2()
        # self.parsed_files = pi.open_pickle('parsed_files', 'hi')
        self.empty = finished2[1]
        self.link_gaps()
        dct1 = {}
        self.missing_gaps = set()
        self.missing_gap_files = set()
        self.has_gaps = set()
        self.repeats = 0
        self.gaps = 0
        self.plugged_gaps = 0
        self.bad_info = 0
        self.vbad_info = 0
        self.bad_ger_beg = 0
        self.bad_names = []
        self.done_gaps = []
        self.total_parents = {k: v for k, v in self.processed.items() if 'l' not in k and 'm' not in k}
        # self.done_gaps = set(to.from_txt2lst(hdir + 'temp/done_gaps'))
        # self.done_gaps = [x.strip() for x in self.done_gaps]

        for x, y in self.processed.items():
            if x[-1] == '.':
                dct1[x[:-1]] = y
            else:
                dct1[x] = y

        self.processed = dct1
        d = 0
        par = 0
        e = 0
        for x, y in self.processed.items():

            d += 1
            # vgf.print_intervals(d, 10)

            # if not x.endswith('l'):
            if not x == '1081l':
                e += 1

            else:
                e += 1
                num = x[:-1]
                p (num)
                if num == '15372': # 159
                    bb = 8

                self.file_name = num

                self.parent = self.processed.get(num)
                if not self.parent:
                    p (f'{num} missing')
                else:
                    # self.check_lst_word()
                    self.gapped = False
                    self.children = [y]
                    c = 1
                    par += 1
                    obj = 1
                    while obj:
                        obj = self.processed.get(num + "m" + str(c))
                        if obj:
                            self.children.insert(0, obj)
                        else:
                            if num + "m"+ str(c) in self.empty:
                                obj = 1
                        c += 1
                        e += 1

                    self.children.insert(0, self.parent)
                    self.patch1()
                    # self.print_original()
                    self.get_child_sets()
                    self.link_children2()
                    self.total_parents[x] = self.parent
                    # if self.gapped:
                    #     self.print_second()

        p(f"{e} files out of {len(self.processed)}")
        p (self.gaps)
        p (self.plugged_gaps)
        # to.from_lst2txt(self.missing_gap_files, 'missing_gap_files')
        # to.from_lst2txt(self.missing_gaps, 'missing_gaps')
        self.count_words2(True)

        dct1 = {k:v for k, v in self.processed.items()
                if not reg(r'[lm]', k)}

        bb = 8

        # pi.save_pickle(dct, 'tle_txts4', 'hi')
        # p (self.bad_info)
        # p (self.vbad_info)
        # p (f'total {e}')
        # p (self.bad_ger_beg)
        return


    def patch1(self):
        for x in self.children:
            for e, z in en(x.translit_n_info):
                if not z:
                    x.translit_n_info[e] = [[-1,""]]


    def get_child_sets(self):
        self.child_sets = []
        for child in self.children:
            self.child_sets.append(set(child.translit2german))

    def link_children2(self):
        c = 1
        self.all_sents = set(self.parent.translit2german)
        self.all_info = [z[1] for x in self.parent.translit_n_info for z in x]


        for x, y in zip(self.child_sets[:-1], self.child_sets[1:]):
            child = self.children[c]
            if y <= self.all_sents:
                pass
            elif child.translit2german[0] in self.all_sents:
                sz = self.get_size(child)
                self.add2parent(child, sz)


            else:
                st1 = y & self.all_sents
                if st1:
                    self.strategy2(child)
                else:

                    found = False
                    gaps = self.gap_dct.get(self.file_name)
                    if not gaps:
                        self.gaps += 1
                        self.missing_gap_files.add(self.file_name)
                        self.add2parent(child, 0, True)
                        self.gapped = True
                    else:


                        to_delete = []
                        for f, child2 in en(gaps):
                            st = set(child2.translit2german)
                            if st < self.all_sents:
                                to_delete.append(f)
                            elif child2.translit2german[0] in self.all_sents:
                                sz = self.get_size(child2)
                                self.add2parent(child2, sz)
                                to_delete.append(f)
                                self.plugged_gaps += 1
                                found = True
                                break
                            elif st & self.all_sents:
                                self.plugged_gaps += 1
                                to_delete.append(f)
                                self.strategy2(child2)
                                found = True
                                break

                        for z in reversed(to_delete):
                            del gaps[z]



                        if not found:
                            self.gaps += 1
                            self.missing_gaps.add(self.file_name)
                            self.gapped = True


            c += 1

    def get_size(self, child):
        for sz, ger in en(child.translit2german):
            if not ger in self.all_sents:
                break
        return sz

    def strategy2(self, child):
        on = False
        for sz, sent in en(child.translit2german):
            if on:
                if sent not in self.all_sents:
                    self.add2parent(child, sz)
                    return

            if sent in self.all_sents:
                on = True

    def link_gaps(self):
        self.gap_dct = {}
        for x, y in self.processed_gaps.items():

            if y.translit2german:
                if "m" in x:
                    idx = x.index('m')
                elif 'n' in x:
                    idx = x.index('n')
                num = x[:idx]
                self.gap_dct.setdefault(num, []).append(y)

    def add2parent(self, child, sz, gapped=False):
        if gapped:
            child.translit_n_info.insert(0, [-6, ".."])
            child.translit2german.insert(0, "[gap]")
        new_sents = child.translit2german[sz:]
        self.parent.translit_n_info += child.translit_n_info[sz:]
        # for x in new_sents:

        self.parent.translit2german += new_sents
        self.all_sents |= set(new_sents)
        #
        # if gapped:
        #     e = 0
        #     child.translit_n_info.insert(0, [-6, ".."])
        #     child.translit2german.insert(0, "[gap]")
        #     lst = child.translit_n_info
        # else:
        #     otranslit = " ".join(self.all_info)
        #     # for x in self.all_info:
        #     #     for z in x:
        #     #         otranslit += " " + z[1]
        #
        #
        #     str1 = ""
        #     d = 0
        #     lst = child.translit_n_info
        #
        #     while True:
        #
        #         for e, x in en(lst):
        #             for z in x:
        #                 str1 += " " + str(z[1])
        #                 if str1 not in otranslit:
        #                     break
        #         if d > 0:
        #             break
        #         elif e < 4:
        #             lst = self.prev_child.translit_n_info + \
        #                   child.translit_n_info
        #             d += 1
        #             str1 = ""
        #
        #         else:
        #             break
        #
        # new_info = lst[e:]
        # self.parent.translit_n_info += new_info
        # self.all_info += [str(x) for x in new_info]

        return

    def false_ending(self, x, y):
        num = x[:-1]
        parent = self.processed.get(num)
        if y.translit2german == parent.translit2german:
            return True

    def print_original(self):
        p(f"""
               {self.file_name}
               """)

        self.main_lst = self.children[0].translit2german

        for v in self.main_lst:
            p(v)

        for e, child in en(self.children[1:]):
            p(f"""
                   page {e + 1}
                   """)
            for ger in child.translit2german:
                p(ger)

        return

    def print_second(self):

        p(f"""
        changed
        """)

        for x in self.parent.translit2german:
            p(x)

    def move_gaps(self):
        dir1 = hdir + "tle/texts/"
        dir2 = hdir + "tle/has_gaps/"
        folder = os.listdir(dir1)
        self.has_gaps2 = to.from_txt2lst(hdir + 'bad_middles.txt')

        for x in self.has_gaps2:
            b = 1
            while True:
                file = f"{x}m{b}"
                full_path = f"{dir1}{x}m{b}"
                full_path_new = f"{dir2}{x}m{b}"

                file1 = file + '_files'
                if file1 not in folder and b == 1:
                    break

                elif not file1 in folder:
                    break
                else:
                    file1_new = full_path_new + "_files"
                    file1 = full_path + "_files"
                    try:
                        shutil.copytree(file1, file1_new)
                    except:
                        pass
                    file2 = file + '.html'
                    file3 = file + '.htm'
                    if file2 in folder:
                        file2 = full_path + '.html'
                        file2_new = full_path_new + '.html'
                        shutil.copy(file2, file2_new)
                    elif file3 in folder:
                        file3 = full_path + '.htm'
                        file3_new = full_path_new + '.htm'
                        shutil.copy(file3, file3_new)
                    else:
                        assert False

                b += 1

    # def penultimate(self, e):
    #     if len(self.children)
    #
    #     pen_ul = self.children


    def cut_off_top(self):
        self.parsed_files = pi.open_pickle('parsed_files', 'hi')
        self.files = pi.open_pickle('raw_files', 'hi')
        bad_files = []
        b = 0
        for name, file in self.parsed_files.items():
            if name in self.files:
                for e, line in en(file):
                    if '[Version]' in line and '[Impressum]' in line:
                        if e < 2:
                            break
                        else:
                            b += 1
                            self.parsed_files[name] = file[e + 1:]
                            raw_file = self.files[name]
                            self.files[name] = raw_file[e + 1:]
                            break
                else:
                    p(f'{name} bad file')

        p(b)
        str1 = input('continue?: ')
        pi.save_pickle(self.files, 'raw_files', 'hi')
        pi.save_pickle(self.parsed_files, 'parsed_files', 'hi')

    def html_parse_files(self):
        self.parsed_files = pi.open_pickle('parsed_files2', 'hi')
        self.files = pi.open_pickle('raw_files2', 'hi')
        self.get_files('special')
        # assert len(self.files) == len(self.parsed_files)
        p(f'{len(self.parsed_files)} files')
        p(f'raw files {len(self.files)}')
        pi.save_pickle(self.files, 'raw_files2', 'hi')
        pi.save_pickle(self.parsed_files, 'parsed_files2', 'hi')

    def parse_gaps(self):
        self.gapped_files = {}
        self.raw_gaps = {}
        self.get_files_gapped('new_texts')
        pi.save_pickle(self.gapped_files, 'gapped_files', 'hi')
        pi.save_pickle(self.raw_gaps, 'raw_gaps', 'hi')

    def check_all_dct_words(self):
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')
        self.all_words = pi.open_pickle('all_words', 'hi')
        self.file = self.parsed_files['prepositions']
        self.tle_dct = merge_2dicts(self.tle_dct, self.words2entry)
        missing = set(self.all_words.keys()) - set(self.tle_dct.keys())

    # super categories, + 22701
    ## combine 87 and 88 with 86 delete 87 88
    def main_dct(self):
        # self.get_files('dictionary')
        self.parsed_files = pi.open_pickle('parsed_tle_dct', 'hi')
        b = 0
        for k, self.file in self.parsed_files.items():
            found = False
            self.kind = k
            temp_freq = []
            vgf.print_intervals(b, 100)
            for self.line in self.file:
                if found and reg(r'\S', self.line):
                    self.line = self.line.strip()
                    if 'top of page' in self.line:
                        self.fix_frequency(temp_freq)
                        break
                    elif reg(r'[a-zA-Z]', self.line):
                        ins = tle_entry()
                        self.parse_definition(ins)
                    elif not reg(r'[^0-9\.]', self.line):
                        temp_freq.append([ins.lemma_n_word, self.line])
                        self.words2entry[ins.lemma_n_word] = ins

                elif 'lemmafrequencypercent' in self.line:
                    found = True
            b += 1

        self.count_words()
        self.convert2dct()

    def count_words(self):
        total = 0
        for x, y in self.words2entry.items():
            total += y.frequency
        p(f'types: {len(self.words2entry)}')
        p(f'tokens: {total}')

    def convert2dct(self):
        words2entry_dct = {}
        for x, y in self.words2entry.items():
            dct = to.from_cls2dict(y)
            words2entry_dct[x] = dct
        pi.save_pickle(words2entry_dct, 'tle_dictionary2', 'hi')

    def parse_definition(self, ins):
        try:
            ins.original = self.line
            def_start = self.line.index('"')
            egy_word = self.line[:def_start]
            egy_word = egy_word.strip()
            ins.word = egy_word
            self.line = self.line[def_start + 1:]
            str1 = "(" if '"' not in self.line else '"'
            def_end = self.line.index(str1)
            ins.ger_word = self.line[:def_end]
            self.line = self.line[def_end + 1:]
            src_end = self.line.index(")")
            ins.source = self.line[:src_end]
            self.line = self.line[src_end + 1:]
            b = self.line.rindex(' ')
            ins.lemma_no = self.line[b + 1:-1]
            ins.lemma_n_word = f"{egy_word}  {ins.lemma_no}"
            ins.kind = self.kind
        except:
            pass

    def fix_frequency(self, temp_freq):
        test = []
        last_num = 0
        e = 0
        for tpl in reversed(temp_freq):
            if e == 682:
                bb = 8
            num = tpl[1]
            idx = num.index('.')
            word_n_lemma = tpl[0]
            first = int(num[idx - 1])
            if last_num > 6 and first < 2:
                num = num[:idx - 2]
            else:
                num = num[:idx - 1]
            num = int(num)
            last_num = first
            self.words2entry[word_n_lemma].frequency = num
            test.append(num)
            e += 1

        for x, y in zip(test[:-1], test[1:]):
            assert x <= y

        return

    def get_files_gapped(self, folder):

        str1 = hdir + f"tle/{folder}/"
        b = 0
        for e, x in en(os.listdir(str1)):
            # if not reg(r'm(\d)+\.htm',x):
            if x.endswith('html') or x.endswith('htm'):
                num = x[:-5] if x.endswith('html') else x[:-4]
                str6 = hdir + f'tle/{folder}/{x}'
                with codecs.open(str6, 'rb') as g:
                    lst = [y.decode("latin-1") for y in g]
                    self.raw_gaps[num] = lst
                    y = [vgf.use_beautiful_soup(z, 1) for z in lst]
                    self.gapped_files[num] = y
                    vgf.print_intervals(b, 50)
                    b += 1
        p(f'{b} new files')
        p(f'{len(self.gapped_files)} total files')
        return

    def get_files(self, folder):

        str1 = hdir + f"tle/{folder}/"
        b = 0
        for e, x in en(os.listdir(str1)):
            # if not reg(r'm(\d)+\.htm',x):



            if (x.endswith('html') or x.endswith('htm')) and \
                 not 'has_gaps' in x and not 'n' in x:

                num = x[:-5] if x.endswith('html') else x[:-4]
                # if num not in self.files:
                    # if num in ['13023', '20118']:
                if not num in [99]:
                    bb = 8
                    str6 = hdir + f'tle/{folder}/{x}'
                    with codecs.open(str6, 'rb') as g:
                        lst = [y.decode("latin-1") for y in g]



                        y = [vgf.use_beautiful_soup(z, 1) for z in lst]


                        self.files[num] = lst

                        self.parsed_files[num] = y
                        vgf.print_intervals(b, 50)
                        b += 1
        p(f'{b} new files')
        # p(f'{len(self.parsed_files)} total files')
        return

    def check_headers(self):
        self.get_headers()
        for name, file in self.parsed_files.items():
            for line in file:
                for line_header in self.line_header:
                    if line.startswith(line_header) \
                            and len(line) == len(line_header):
                        p(name, line)

                for header in self.headers:
                    if line.startswith(header) \
                            and len(line) != len(header):
                        p(name, line)

    def get_tle_translators(self):
        self.tle_translators = set(pi.open_pickle("tle_translators", 'hi'))
        self.tle_translators.add('F. Feder')
        self.translators |= self.tle_translators

    def get_headers(self):
        self.headers = [
            'date',
            'present location',
            'provenance',
            'type of object',
            'script',
            'type of text',
        ]

        self.line_headers = [
            'bibliography',
            'line count according to',
            'definition'
        ]

        self.header_dct = {}
        self.header_dct['line count according to'] = 'line_count'
        for x in self.headers + self.line_headers:
            self.header_dct[x] = x.replace(' ', '_')

        self.all_headers = self.headers + self.line_headers + ['tree of objects']

    def quick_test(self):
        self.used_headers = []
        for line in self.file:
            for y in self.headers + self.line_headers:
                if line.startswith(y):
                    self.used_headers.append(self.header_dct[y])
                    break

    def test_headers(self):
        for x in self.used_headers:
            val = getattr(self.ins, x)
            if not val:
                p(self.file_name)
                p(x)
                p('')

    def temp12(self):
        c = 0
        for k, self.file in self.parsed_files.items():
            b = len(self.file)
            self.raw_file = self.files[k]
            d = len(self.raw_file)
            c += 1
            if abs(len(self.file) - len(self.raw_file))>2:
                c += 1
                p (k)

            if c > 300:
                break



    def cut_off_detail(self):
        if '[detailed information for text]' in self.line:
            idx = self.line.index('[detai')
            self.line = self.line[:idx]

    def first(self):
        self.get_headers()
        # self.temp13()
        b = 0
        cc = 0
        # 19860, 5835

        for k, self.file in self.parsed_files.items():
            # if k == '3865':
            if reg(r'^1081(m|l)', k):
                found = False

                # if k not in self.processed and k in self.files:

                # if k not in self.processed and k not in self.empty:
                self.quick_test()
                cc += 1
                # if cc == 30500:
                #     pi.save_pickle([self.processed, self.empty], 'finished_texts5', 'hi')
                #     pi.save_pickle(self.bad_files, 'bad_files', 'hi')
                #     pi.save_pickle(self.no_name, 'no_name', 'hi')

                self.raw_file = self.files[k]
                self.file_name = k
                p (k)
                vgf.print_intervals(cc, 500)
                self.ins = tle_file()
                self.ins.number = k
                theader = ""
                self.e = 1
                while self.e < len(self.file):
                    self.line = self.file[self.e]
                    if self.e == 16:
                        bb = 8

                    if self.line:
                        self.cut_off_detail()

                        if self.line.startswith('ERROR:'):
                            self.ins.name = 'ERROR'
                            p('error')

                            self.empty[k] = self.ins
                            found = True
                            break

                        elif 'Thesaurus Linguae Aegyptiae' in self.line and not self.ins.script:
                            self.cut_line_left('Thesaurus Linguae Aegyptiae')
                            line2 = self.line[1:].strip()
                            if line2:
                                self.ins.name = line2
                            else:
                                self.e += 1
                                self.line = self.file[self.e]
                                self.cut_off_detail()
                                while self.line:
                                    if not self.ins.name:
                                        self.ins.name += self.line.strip()
                                    else:
                                        self.ins.name += self.line.strip()
                                    self.e += 1
                                    self.line = self.file[self.e]
                                    self.cut_off_detail()

                        elif 'Thesaurus Linguae' in self.line and not self.ins.script:
                            self.increase_one()
                            self.cut_line_left('Aegyptiae,')
                            self.ins.name = self.line[1:].strip()
                            theader = "name"

                        elif any(self.line.startswith(x) for x in self.line_headers):
                            for x in self.line_headers:
                                if self.line.startswith(x):
                                    self.cut_line_left(x)
                                    x = self.header_dct[x]
                                    setattr(self.ins, x, self.line)
                                    theader = x
                                    break

                        elif any(self.line.startswith(x) for x in self.headers):
                            for x in self.headers:
                                if self.line.startswith(x):
                                    self.loop_until_txt()
                                    if x == 'scrip': x = 'script'
                                    x = self.header_dct[x]
                                    setattr(self.ins, x, self.line)
                                    theader = x
                                    break

                        elif 'tree of objects' in self.line:
                            self.increase_one()
                            self.loop_until_txt()
                            if 'functions' in self.line:
                                # p(k)
                                # p ('tree of objects')
                                self.empty[k] = self.ins
                                found = True
                                break
                            else:
                                self.line = re.sub(r'\[.*\]', "", self.line)
                                self.ins.hierarchy = self.line
                                theader = 'hierarchy'

                        elif 'display at beginning of text' in self.line or \
                                '[first]' in self.line and '[prior]' in self.line:
                            # if 'm' in self.file_name or 'n' in self.file_name:
                            #     self.e -= 1
                            # else:
                            self.increase_one()
                            self.loop_until_txt()
                            self.parse_translit()
                            found = True
                            break

                        else:
                            if theader:
                                val = getattr(self.ins, theader)
                                setattr(self.ins, theader, val + " " + self.line)

                    self.e += 1
                self.test_headers()
                if not found:
                    p (k)
                    self.bad_files.append(k)
                    # sys.exit()
        b += 1

    def increase_one(self):
        self.e += 1
        self.line = self.file[self.e]

    def parse_translit(self):
        just_translit = []
        self.raw_start = 0
        first_prior = 0
        self.certainty_score = 0
        found = False
        words_found = False
        destroyed_words = {
            '850818': '[personal name]',
            '850830': '[name]',
            '850624': '[subst]',
            '850831': '[word]',
            '850625': '[subst]',
            '850626': '[subst]',
            '850627': '[subst]',
            '850628': '[subst]',
            '850836': '[verb]',
            '850630': '[subst]',
            '850631': '[subst]',
        }

        self.e += 1

        while self.e < len(self.raw_file):
            self.line = self.raw_file[self.e]
            self.has_bcar = False
            self.parsed = vgf.use_beautiful_soup(self.line, 1)
            self.parsed = self.parsed.strip()

            if "759m7" == self.file_name:
                bb = 8

            if self.e > 193:
                bb = 8

            # if '?' in self.parsed:
            #     self.certainty_score += 1
            # trustworthy2 = self.make_trustworthy(self.parsed)

            if '[first]' in self.parsed and '[prior]' in self.parsed or \
                    'display at beginning of text' in self.parsed:
                self.ins.has_ending = True
                first_prior += 1
                if first_prior == 2:
                    found = True

            if 'wn=' in self.line:
                words_found = True
                self.all_words += 1
                idx3 = self.line.index('wn=')
                line1 = self.line[idx3 + 3:]
                try:
                    idx2 = line1.index("&")
                except:
                    p(f'no & in {line1}')
                    idx2 = len(line1)
                    # 20530
                    # p (self.file_name)
                    # sys.exit()
                lemma = line1[:idx2]
                # if lemma == '850821' and not reg(r'[a-zA-Z]', self.parsed):
                #     self.parsed = '[title]'
                #
                # elif lemma in destroyed_words:
                #     self.parsed = destroyed_words[lemma]
                #     self.certainty_score += 1
                # else:
                #     self.parsed = self.hande_cartouche(self.parsed)

                # str7 = f'[{chr(191)}{chr(97)}?]'
                # self.parsed = self.parsed.replace(str7, "..")
                # just_translit.append(trustworthy2)
                # entry = self.tle_dct.get(lemma)
                # if not entry:
                #     p(f'lemma {lemma}  {self.parsed} is not in the dictionary')
                #     eng_word = ""
                # else:
                #     eng_word = entry.eng_word
                just_translit.append([lemma, self.parsed])
                # if self.has_bcar:
                #     self.ins.translit_n_info.append(['-3', 'BK', ""])

            elif not reg(r'\S', self.parsed):
                pass

            elif 'Illustration' in self.line:
                bb = 8
                p(self.line)



            elif self.parsed == '(H)':
                self.ins.has_glyphs = True

            elif self.parsed == '(C)':
                self.ins.has_notes = True

            # elif trustworthy2 in self.word2lemma:
            #     just_translit.append(trustworthy2)
            #     lemma = self.word2lemma.get(trustworthy2)
            #     entry = self.tle_dct[lemma[0]]
            #     self.ins.translit_n_info.append([lemma[0], trustworthy2, entry.eng_word])

            elif any(self.parsed.startswith(x) for x in self.tle_translators):
                if all(not x for x in self.ins.translit2german):
                    p(f'no translation {self.file_name} ')
                    self.empty[self.file_name] = self.ins
                    # p ('no translation')

                else:
                    self.processed[self.file_name] = self.ins
                self.ins.translator = self.parsed
                found = True
                break



            elif '(display at end' in self.parsed or \
                    'top of page' in self.parsed or \
                    '[first]' in self.parsed or '[prior]' in self.parsed:
                if not self.ins.name:
                    p(f'no name for {self.file_name}')
                    self.no_name.append(self.file_name)

                self.get_translator(self.e)

                found = True
                break

            elif '</td><td>' in self.line:
                # if len(self.processed) < 100:
                #     p (just_translit)
                #     p ('')
                #     p (self.parsed)
                #     p ('')

                if not words_found:
                    self.ins.translit2german.append('no translation')
                    self.ins.translit_n_info.append(just_translit)
                    just_translit = []
                else:
                    self.ins.translit_n_info.append(just_translit)
                    self.ins.translit2german.append(self.parsed)
                    if '(C)' in self.parsed:
                        self.ins.has_notes = True
                    just_translit = []

                    # c = self.parsed.count(" ")
                    # self.total_german += c
                    # just_translit = []
                    # self.certainty_score = self.parsed.count('...')
                    # self.certainty_score += self.parsed.count('(?)')
                    # if not self.parsed.count(' '):
                    #     score = 0
                    # else:
                    #     score = int((self.certainty_score / self.parsed.count(' ')) * 100)
                    # self.ins.certainty.append(score)
                    # self.ins.trustworthy.append(str1)
                    # self.certainty_score = 0



            # elif any(x in self.parsed for x in self.destroyed):
            #     self.ins.translit_n_info.append(['-4', "...", ""])
            #     just_translit.append('..')
            #     self.destroyed_lines.add(self.parsed)
            # self.certainty_score += 1

            elif not '</td><td>' in self.line:
                just_translit.append(["-1", self.parsed])
                if reg(r'[a-zA-Z]{2,}', self.parsed):
                    self.interspersed.add(self.parsed)
                if len(self.processed) > 1000:
                    bb = 8

            self.e += 1

        if not found:
            self.empty_middle[self.file_name] = self.ins

            p (f'bad file {self.file_name}')
            # sys.exit()

        if all(not x for x in self.ins.translit2german):
            self.empty[self.file_name] = self.ins

            if 'm' not in self.file_name and 'l' not in self.file_name:
                self.empty[self.file_name] = self.ins
            elif 'm' in self.file_name or 'l' in self.file_name:
                self.empty_middle[self.file_name] = self.ins


        else:
            self.processed[self.file_name] = self.ins

        # for x, y, z in self.ins.translit_n_info:
        #     p (f'{x}   {y}   {z}')
        #     p ('')
        #
        #
        #
        # for x, y in self.ins.translit2german.items():
        #     pp (x)
        #     p ('')
        #     pp (y)
        #     p ('')
        #
        #
        # p ("""
        # next
        # """)

        if len(self.ins.translit_n_info) != len(self.ins.translit2german):
            p(self.file_name)
            bb = 8

        return

    def get_translator(self, idx):
        try:
            if 'display at end' in self.parsed or \
                    '[first]' in self.parsed and '[prior]' in self.parsed:
                idx += 1
                self.parsed = self.file[idx]
                while not self.parsed:
                    idx += 1
                    self.parsed = self.file[idx]

            elif 'top of page' in self.parsed:
                idx -= 1
                self.parsed = self.file[idx]
                while not self.parsed:
                    idx -= 1
                    self.parsed = self.file[idx]

            # idx2 = self.parsed.index('Strukturen und Tran')
            # line = self.parsed[idx2:].strip()
            # if line[-1] == ',':
            #     line = line[:-1]

            for x in self.tle_translators:
                if self.parsed.startswith(x):
                    self.ins.translator = x
                    break
            else:
                self.translators.add(self.parsed)
                self.ins.translator = x
        except:
            pass

    def hande_cartouche(self, str1, trustworthy=False):
        front_car = ['cartouche|', 'Kartusche|']
        back_car = ['|Kartusche', '|cartouche']
        if any(x in self.line for x in front_car):
            for x in front_car:
                str1 = str1.replace(x, "")
            if not trustworthy:
                self.ins.translit_n_info.append(['-2', 'FK', ""])
        if any(x in self.line for x in front_car):
            if not trustworthy: self.has_bcar = True
            for x in back_car:
                str1 = str1.replace(x, "")

        return str1

    def make_trustworthy(self, str1):
        if "[b" in str1 and "b]" in str1:
            str1 = str1.replace('[b', '')
            str1 = str1.replace('b]', '')

        str1 = str1.replace(':', ".")

        str1 = re.sub(r'[\+_<>\{\}[\[\]\(\)\?]', '', str1)
        str1 = str1.replace("'", "")
        if reg(r'[a-zA-Z]=[a-z]{1,}\s', str1):
            e = 0
            while e < len(str1):
                y = str1[e]
                if str1[e - 1].isalpha and y == '=':
                    str1 = add_at_i(e, str1, " ")
                    e += 1
                e += 1

        str1 = str1.replace('=', '-')
        str1 = str1.replace(upside_down_q, "")
        if self != 0:
            str1 = self.hande_cartouche(str1, 1)

        return str1

    def loop_until(self, words):
        f = self.e
        while words not in self.line and f < len(self.line):
            f += 1
            self.line = self.file[f]
        self.e = f
        self.line = self.file[self.e]

    def loop_until2(self, word1, word2):
        f = self.e
        while word1 not in self.line and word2 not in self.line \
                and f < len(self.file):
            f += 1
            self.line = self.file[f]
        self.e = f
        self.line = self.file[self.e]

    def loop_until_txt(self):
        while not reg(r'\S', self.line):
            self.e += 1
            self.line = self.file[self.e]

    def cut_line(self, word, word2):
        idx = self.line.index(word) + len(word)
        self.line = self.line[idx:]
        idx1 = self.line.index(word2)
        self.line = self.line[:idx1]

    def cut_line_left(self, word):
        idx = self.line.index(word) + len(word)
        self.line = self.line[idx:].strip()

    def add_more_translators(self):
        pass
        # new_trans = []
        # for x in self.translators:
        #     if all(not x.startswith(y) for y in self.tle_translators):
        #         lst = x.split(',')
        #         new_trans.append(lst[0])
        # for e, x in en(new_trans):
        #     p (e, x)
        #
        # if new_trans:
        #     str1 = input('input false trans: ')
        #     lst = str1.split()
        #     lst = [int(x) for x in lst]
        #     for num in reversed(lst):
        #         del new_trans[num]
        #     new_trans = set(new_trans)
        #     self.tle_translators |= new_trans
        #     pi.save_pickle(self.tle_translators, 'tle_translators', 'hi')


def build_lemma2freq():
    tle_dct = pi.open_pickle('tle_dct6', 'hi')
    lemma2freq = {}
    lemma_n_word2freq = {}
    for k, v in tle_dct.items():
        lemma2freq[k] = v.frequency
        lemma_n_word2freq[v.lemma_n_word] = v.frequency

    lemma2freq = sort_dict_by_val_rev_dct(lemma2freq)
    lemma_n_word2freq = sort_dict_by_val_rev_dct(lemma_n_word2freq)


def scrape_beginning():
    lst = pi.open_pickle('bad_original_files', 'hi')
    dir1 = hdir + 'tle/texts/'
    for x in lst:
        for y in os.listdir(dir1):
            if x + '.html' == y:
                os.remove(dir1 + y)
            elif x + '_files' == y:
                shutil.rmtree(dir1 + y)

    for e, k in en(lst):

        p(f'{e} of {len(lst)}')
        if not pi.open_pickle('bool2'):
            return

        str2 = f'http://aaew.bbaw.de/tla/servlet/GetTextDetails?u=guest&f=0&l=0&tc={k}&db=0'

        try:
            wbb.open_new_tab(str2)
            time.sleep(3)
            pyautogui.hotkey('command', 's')
            time.sleep(.5)
            pyautogui.typewrite(f"{k}")
            time.sleep(.3)
            pyautogui.hotkey('return')
            time.sleep(3)
            pyautogui.hotkey('command', 'w')
            time.sleep(.1)
        except:
            p(f'error with opening {k}')


def download_demotic():
    dct5 = {
        # 11: 'adjectives',
        # 12: 'adjective_no_nisba',
        # 13: 'nisba_from_preposition',
        # 14: 'nisba_from_noun',
        # 16: "adverbs_from_prepositions",
        17: 'verbs',
        15: 'adverbs',
        # 18: 'prepositions',
        19: 'pronouns',
        20: 'demonstrative_pronouns',
        21: 'personal_pronouns',
        22: 'relative',
        23: 'interrogative',
        24: 'particles',
        25: 'enclitic_particles',
        26: 'nonenclitic_particles',
        27: 'numerals',
        28: 'cardinal_numbers',
        29: 'ordinal_numbers',
        30: 'interjections'
    }


def meets_cond4tle_dct(file_name):
    if not file_name: return False

    str6 = hdir + f'tle/dict_entries/'
    lst_files = os.listdir(str6)
    if not file_name + '.html' in lst_files and not \
            file_name + '.htm' in lst_files:
        return False

    str1 = '.htm'
    if file_name + ".html" in lst_files:
        str1 = '.html'

    with codecs.open(str6 + file_name + str1, 'rb') as g:
        txt_lst = [y.decode("latin-1") for y in g]
        for x in txt_lst:
            if 'top of page' in x:
                return True
        else:
            os.remove(str6 + file_name + str1)
            shutil.rmtree(str6 + file_name + '_files')
            p('file removed and tried again')
        return False


def meets_conditions(file_name):
    if not file_name: return False

    str6 = hdir + f'tle/special/'
    lst_files = os.listdir(str6)
    if not file_name + '.html' in lst_files and not file_name + '.htm':
        return False

    str2 = '.html' if file_name + '.html' in lst_files else '.htm'

    with codecs.open(str6 + file_name + str2, 'rb') as g:
        txt_lst = [y.decode("latin-1") for y in g]
        priors = 0
        end = 0
        begin = 0
        for x in txt_lst:
            if '[prior]' in x:
                priors += 1
            elif 'display at beginning' in x:
                begin += 1
            elif 'display at end' in x:
                end += 1
        time.sleep(5)
    if priors == 2:
        return 'nxt_pg'
    if begin and end:
        return 'done_pg'
    if begin and priors:
        return 'done_pg'
    if priors and end:
        return 'nxt_pg'
    else:
        os.remove(str6 + file_name + str2)
        shutil.rmtree(str6 + file_name + '_files')
        pyautogui.hotkey('command', 's')
        time.sleep(1)
        pyautogui.typewrite(file_name)
        time.sleep(.3)
        pyautogui.hotkey('return')
        time.sleep(2)
        # pyautogui.hotkey('command', 'w')
        # time.sleep(.3)


def loop_til_orange():
    im = pyautogui.screenshot(base_dir + f"hieroglyphs/flash_cards/hey.png")
    j = 0
    while j < 4:
        for i in range(330, 380):
            rgb = im.getpixel((153 * 2, i * 2))
            b = tuple(rgb[:3])
            if b == (254, 203, 156):
                return i - 5
        time.sleep(3)
        j += 1
        p(f'find color attempt {j}')

    p('failed to find color')
    return 0


##http://aaew.bbaw.de/tla/servlet/GetCtxt?u=guest&f=0&l=0&tc=21441&db=0&ws=92&mv=2
# page 5
# failed to load pg
# 254 203 156

def meets_col_cond():
    im = pyautogui.screenshot(base_dir + f"hieroglyphs/flash_cards/hey.png")
    rgb = im.getpixel((485 * 2, 880 * 2))
    if rgb == (178, 147, 110):
        return True
    return False


def scrape_tle_dct():
    # http://aaew.bbaw.de/tla/servlet/GetTextDetails?u=guest&f=0&l=0&tc=285&db=0
    # http://aaew.bbaw.de/tla/servlet/s0?f=0&l=0&ff=8&ex=1&db=0&wt=10&l1=1&mx=9000

    dir1 = hdir + "tle/dict_entries/"
    # all_lemmas = pi.open_pickle('tle_dct6', 'hi')

    lst = to.from_txt2lst(hdir + 'temp9.txt')

    # done = set()
    # for x in os.listdir(dir1):
    #     if x.endswith('html') or x.endswith('htm'):
    #         idx = x.index(".")
    #         done.add(x[:idx])

    # lst = [x for x in all_lemmas.keys() if x not in done]
    driver = wbs.Chrome()
    driver.get('http://aaew.bbaw.de/tla/servlet/TlaLogin')

    str5 = input('wait')
    time.sleep(1)
    str1 = driver.current_url
    e = 0
    while e < len(lst):
        file_name = lst[e]
        p(f'{e} of {len(lst)}')
        p(f'file name {file_name}')
        if not pi.open_pickle('bool2'):
            return

        str2 = f"http://aaew.bbaw.de/tla/servlet/GetWcnDetails?u=guest&f=0&l=0&wn={file_name}&db=0"
        driver.get(str2)

        dd = 0

        # while pi.open_pickle('bool2'):
        time.sleep(3)
        pyautogui.hotkey('command', 's')
        time.sleep(.5)

        col_attempt = 0
        while meets_col_cond():
            time.sleep(.2)
            col_attempt += 1
            p(f"{col_attempt} color_attempt")
            if col_attempt > 15:
                p('failed to get color')
                return

        pyautogui.typewrite(file_name)
        time.sleep(.3)
        pyautogui.hotkey('return')
        time.sleep(1.5)
        # action = meets_cond4tle_dct(file_name)
        # if action:
        #     break
        # elif not action:
        #     time.sleep(20)
        #     p(f'attempt {dd}')
        #
        # dd += 1
        # if dd > 15:
        #     p('failed to load pg')
        #     return

        p(driver.current_url)

        e += 1


def scrape_tle():
    # http://aaew.bbaw.de/tla/servlet/GetTextDetails?u=guest&f=0&l=0&tc=285&db=0
    # http://aaew.bbaw.de/tla/servlet/s0?f=0&l=0&ff=8&ex=1&db=0&wt=10&l1=1&mx=9000

    dir1 = hdir + "tle/special/"
    # middles = to.from_txt2lst(hdir + 'temp/not_done.txt')
    # middles = set(x[:-1] for x in middles)
    # middles = pi.open_pickle('middles', 'hi')
    # done = set()
    # for x in os.listdir(dir1):
    #     if reg(r'm(\d)+\.htm', x):
    #         idx = x.index('m')
    #         num = x[:idx]
    #         done.add(num)

    # tstr = input('is dark browser off? ')
    # to_do = set(middles) - set(done)
    # lst = list(to_do)

    # random.shuffle(lst)
    # lst.insert(0, '19947')
    lst = ['1081']
    driver = wbs.Chrome()
    driver.get('http://aaew.bbaw.de/tla/servlet/TlaLogin')

    str5 = input('wait')
    mid_num = 1
    # px = loop_til_orange()
    str1 = driver.current_url
    e = 0
    while e < len(lst):
        file_name = lst[e]
        p(f'{e} of {len(lst)}')
        p(f'file name {file_name}')
        if not pi.open_pickle('bool1'):
            return

        # if e == 0:
        #     str2 = "http://aaew.bbaw.de/tla/servlet/GetCtxt?u=guest&f=0&l=0&tc=19947&db=0&ws=3477&mv=2"
        # else:
        str2 = f'http://aaew.bbaw.de/tla/servlet/GetCtxt?u=guest&f=0&l=0&tc={file_name}&db=0&ws=0&mv=5'
        nxt_pg = False
        # wbb.open(str2)

        q = 0
        skip = False
        while str2[-1] == '5':
            driver.get(str2)
            time.sleep(2)
            px = loop_til_orange()
            if not px:
                skip = True
                break
            pyautogui.moveTo(159, px)
            # pyautogui.moveTo(159, 336)
            pyautogui.click(159, px)
            # pyautogui.click(159, 336)
            time.sleep(1)
            try:
                str2 = driver.current_url
                p(str2)
            except:
                time.sleep(5)
            q += 1
            if q > 3:
                skip = True
                break

        if not skip:
            while pi.open_pickle('bool1'):
                full_file_name = f"{file_name}m{mid_num}"
                time.sleep(3)
                pyautogui.hotkey('command', 's')
                time.sleep(1)
                pyautogui.typewrite(full_file_name)
                time.sleep(.3)
                pyautogui.hotkey('return')
                time.sleep(3)

                action = 0
                dd = 0
                while not action:

                    action = meets_conditions(full_file_name)
                    if action == 'done_pg':
                        nxt_pg = True
                    elif not action:
                        time.sleep(20)
                        p(f'attempt {dd}')

                    dd += 1
                    if dd > 15:
                        p('failed to load pg')
                        return

                if not nxt_pg:
                    mid_num += 1
                    pyautogui.moveTo(159, px)
                    pyautogui.click(159, px)
                    # pyautogui.click(159, 336)
                    time.sleep(1.5)
                else:
                    p('done pg')
                    break

                p(driver.current_url)
                # pyautogui.hotkey('command', 'w')
                # time.sleep(.3)
                p(f'page {mid_num}')

        e += 1
        mid_num = 1


class analyze_text:
    def __init__(self):
        lst = pi.open_pickle('finished_texts', 'hi')
        self.texts = lst[0]
        self.word2freq = defaultdict(int)
        self.lemma2spelling = {}
        self.period2number = defaultdict(int)
        self.century2number = defaultdict(int)
        self.has_ending = set()
        self.count_all_words()
        pi.save_pickle(self.word2freq, 'word_freq', 'hi')
        pi.save_pickle(self.period2number, 'period2number', 'hi')
        pi.save_pickle(self.century2number, 'century2number', 'hi')
        pi.save_pickle(self.lemma2spelling, 'lemma2spelling', 'hi')
        pi.save_pickle(self.has_ending, 'has_ending', 'hi')

        for x, y in self.period2number.items():
            p(x, y)
        p("")

        for x, y in self.century2number.items():
            p(x, y)
        p('all_words')
        p(sum(self.word2freq.values()))
        pi.save_pickle(lst, 'finished_texts2', 'hi')

    def count_all_words(self):
        b = 0
        for x, y in self.texts.items():
            b += 1
            vgf.print_intervals(b, 100)
            y.word_count = 0
            word_count = 0
            if y.has_ending:
                self.has_ending.add(x)

            for rw in y.translit_n_info:
                lemma = rw[0]
                if not reg(r'[^\d]', lemma):
                    if int(lemma) > -1:
                        word_count += 1
                        word = rw[1]
                        word = process_tle.make_trustworthy(0, word)

                        self.word2freq[lemma] += 1
                        self.lemma2spelling.setdefault(lemma, set()).add(word)

            y.word_count = word_count
            if y.date:
                self.period2number[y.phase] += word_count
                self.century2number[y.century] += word_count

        return


def get_spelling2lemma():
    dct = pi.open_pickle('lemma2spelling', 'hi')
    spelling2lemma = {}
    for x, y in dct.items():
        for z in y:
            spelling2lemma.setdefault(z, []).append(x)


def build_tle_contents():
    lst = pi.open_pickle('finished_texts', 'hi')
    texts = lst[0]
    empty = lst[1]
    bb = 8


def fix_dates():
    all_dates = pi.open_pickle('get_egyptian_dates/egyptian_dates', 'hi')

    # 2600-2000 early, 2000 - 1400 Middle, 1400 - 400 late,
    # roman

    ger_king2eng_king = pi.open_pickle("get_egyptian_dates/ger_king2eng_king", 'hi')
    king2year = pi.open_pickle("get_egyptian_dates/king2year", 'hi')

    ger_king2eng_king = vgf.sort_dct_keys_by_len(ger_king2eng_king)

    texts = pi.open_pickle('tle_txts5', 'hi')

    dct1 = {
        "Ptolemaic": 'Ptol',
        'Mittleres Reich': 'Mittleres Reich',
        'Pepi II': "Pepi II",
        'Pepis': 'Pepi I',
        'Pepi-anchu': 'Pepi I',
        'Amarna-Periode': 'Amenhotep IV',
        '26. Dyn': '26 Dyn',
        "Unas": "Unas",
        "Grab des Tjy": 'Amenhotep III',
        "Ptah-hetepu": "Djedkare Isesi",
    }

    for x, y in texts.items():
        if not y.date:
            for k, v in dct1.items():
                if k in y.name:
                    y.date = v

    not_have_dynastie = []
    date2year = {}
    olddate2newdate = {}
    for x, y in texts.items():
        if y.date.startswith('date'):
            y.date = y.date[4:].strip()
        all_dates.add(y.date)

    year2century = {}
    for king, year1 in king2year.items():
        year = year1
        try:
            if year == 'römische Zeit':
                year2century[year1] = 2
            elif year == '100AD':
                year2century[year1] = 1
            elif year == '(30BC - 400AD)':
                year2century[year1] = 2


            else:
                if 'Shepses' in year:
                    year = '2477 - 2467'
                elif 'Tuthmosis III' in year:
                    year = '1498 - 1483'
                elif '1350 - 1334' in year:
                    year = '1350 - 1334'
                elif year1 == '(1291 1278 BC)':
                    year = '1291 - 1278'

                year = re.sub(r'[\.:]', "", year)
                year = year.replace('.', "")
                year = year.replace("BC", "")
                year = year.strip()
                if " " not in year and "-" not in year and chr(8211) not in year:

                    year = int(year)

                else:
                    if reg(r'\(.*\)', year):
                        year = year[1:-1]
                    year = re.sub(r'[\(\)]', "", year)

                    if chr(8211) in year:
                        lst = year.split(chr(8211))
                    elif "-" in year:
                        lst = year.split("-")
                    lst = [int(x.strip()) for x in lst]

                    year = (lst[0] + lst[1]) // 2

                century = int((round(year, -2)) / 100)
                year2century[year1] = century * -1
        except:
            p(year1)

    date2century = {}
    all_dates |= {'25 Dyn', '18 Dyn', 'Ptol'}

    for date in all_dates:
        date1 = date
        date = date.replace('.', "")

        for k, v in ger_king2eng_king.items():
            date = date.replace(k, v)

        for k, v in king2year.items():
            if k in date:
                date2year[date] = v
                try:
                    date2century[date] = year2century[v]
                except:
                    p(f'bad century {v}')
                olddate2newdate[date1] = date
                break
        else:
            not_have_dynastie.append(date)

    for name, ins in texts.items():
        if ins.date:
            new_date = olddate2newdate.get(ins.date)
            if not new_date:
                p(f'no new date for {ins.date}')
            else:

                year = date2year.get(new_date)
                if year:
                    century = date2century[new_date]
                    ins.century = century
                    ins.year = year
                    if -19 > century:
                        period = 'early'
                    elif century < -13:
                        period = 'middle'
                    elif century < -5:
                        period = 'late'
                    else:
                        period = 'final'
                    ins.phase = period

                else:
                    p(ins.date)
    pi.save_pickle(texts, 'tle_txts5','hi')

    return



if eval(not_execute_on_import):

    args = vgf.get_arguments()

    if 'sc' in args:
        scrape_tle()

    elif 'pg' in args:
        ins = process_tle()
        ins.parse_gaps()

    elif 'fd' in args:
        fix_dates()


    elif 'pd' in args:
        ins = process_tle()
        ins.process_dct_entries()

    elif 'pde' in args:
        ins = process_tle()
        ins.parse_dct_entries()

    elif 'html' in args:
        ins = process_tle()
        ins.html_parse_files()

    elif 'ct' in args:
        ins = process_tle()
        ins.cut_off_top()

    elif "hm" in args:
        has_middle()

    elif 'dct' in args:
        ins = process_tle()
        ins.main_dct()

    elif 'mg' in args:
        ins = process_tle()
        ins.move_gaps()

    elif 'xx' in args:
        ins = process_tle()
        ins.check_all_dct_words()

    elif 'lm' in args:
        ins = process_tle()
        ins.link_middles()


    elif 'pt' in args:
        ins = process_tle()
        ins.main_text()

    elif 'tr' in args:
        translate_tle_txt()

# 23131,20157
