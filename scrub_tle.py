import add_path
from general import *
from global_hiero import *
from mine_tle import tle_entry, tle_file, process_tle


def get_word_count(obj):
    b = 0
    for x in obj.translit_n_info:
        if int(x[0]) > 0:
            b += 1
    obj.word_count = b


def get_object_types():
    dct = {}
    b = 0
    for v in texts.values():
        str1 = v.type_of_object
        if str1:
            str2 = re.sub(r'[\.,;]', '', str1)
            lst1 = vgf.strip_n_split(str2, " ")
            dct.setdefault(lst1[0], set()).add(str1)
        else:
            b += 1


class tle_bibl:
    def __init__(self):
        pass

    def by_length(self):
        lst = to.from_txt2lst(hdir + 'temp/bib2.txt')
        lst1 = []
        dct = {}
        dct2 = {}
        on = False
        for e, x in en(lst):
            if on and "|" in x:
                try:
                    dct[x] = lst[e + 1]
                except:
                    pass


            elif 'zzz' in x:
                on = True

        dct = vgf.sort_dct_keys_by_len(dct)
        for k, v in dct.items():
            lst1.append(k)
            lst1.append(v)
            lst1.append('')

        to.from_lst2txt(lst1, hdir + 'temp/bib3.txt')
        vgf.open_txt_file(hdir + 'temp/bib3.txt')

    def read_tle(self):
        self.texts = pi.open_pickle('tle_txts5', 'hi')
        self.st = set()
        found = False
        lst1 = []
        b = 0

        for e, txt in en(self.texts.values()):
            # vgf.print_intervals(e, 50)
            str1 = txt.bibliography
            if str1.startswith('bibliography'):
                str1 = str1[len('bibliography'):].strip()
            txt.bibliography = str1

            str1 = str1.replace('] -', ']-')
            str1 = str1.replace(']. -', '].-')
            str1 = str1.replace('].-', ']-')

            lst = vgf.strip_n_split(str1, ']-')

            for y in lst:
                z = vgf.strip_n_split(y, ';')
                self.st |= set(z)

        self.clip()
        self.clip_by_year()
        self.print_data()

    def print_data(self):
        lst2 = []

        for x in self.all_bibs:
            lst2.append(x + "|")
            lst2.append('')

        lst2.append('')
        lst2.append('done')
        lst2.append('')

        for x in self.not_found:
            lst2.append(x)
            lst2.append('')

        p(len(self.all_bibs))
        p(len(self.not_found))
        to.from_lst2txt(lst2, hdir + 'temp/bib.txt')
        vgf.open_txt_file(hdir + 'temp/bib.txt')

    def clip(self):
        self.not_found = set()
        for e, x in en(self.st):
            # vgf.print_intervals(e, 50, 0, len(self.st))
            found = False

            for bib in self.all_bibs:
                if bib in x:
                    found = True
                    break
            if not found:
                self.not_found.add(x)

    def clip_by_year(self):
        dct = {}
        for x in self.not_found:
            y = re.sub(r'[^\w\s]', "", x)
            lst = y.split()
            str2 = ""
            for z in lst:
                if reg(r'^\d{4}$', z):
                    if int(z) > 1835 and int(z) < 2020:
                        str2 = z
                        break
            if str2:
                try:
                    idx = x.index(str2) + 4
                    new = x[:idx]
                    if new[:2] == '- ':
                        new = new[2:]
                    dct[new] = x
                except:
                    pass
        lst1 = []
        for k, v in dct.items():
            lst1.append(k + "|")
            lst1.append(v)
            lst1.append("")
        p(len(dct))

        to.from_lst2txt(lst1, hdir + 'temp/bib2.txt')
        vgf.open_txt_file(hdir + 'temp/bib2.txt')
        sys.exit()

        return

    def process(self):
        lst = to.from_txt2lst(hdir + 'temp/bib.txt')
        self.all_bibs = set()
        for x in lst:
            if '|' in x and "***" not in x:
                x = x[:x.index("|")]
                self.all_bibs.add(x)

        self.read_tle()

        return


class build_tle_idx:
    def __init__(self):
        self.fin_txt = pi.open_pickle('finished_texts6', 'hi')[1]
        self.weed_out_middle()
        empty = set(self.fin_txt.keys())
        self.texts = pi.open_pickle('tle_txts5', 'hi')
        self.texts = merge_2dicts(self.texts, self.fin_txt)
        uniliterals = {}
        bib_uni = {}
        bigram = {}
        bib_bi = {}
        self.tri = {}
        self.btri = {}
        self.name2num = {}

        for x, y in self.texts.items():
            if ' EA ' in y.name:
                bb = 8
            if y.name == "pPrisse = pBN 186-194, Die Lehre des Ptahhotep":
                bb = 8
            self.number = y.number
            word = y.name.lower()
            bib = y.bibliography.lower()
            self.bib = bib
            word = re.sub(r'[^\w\s]', "", word)
            bib = re.sub(r'[^\w\s]', "", bib)
            bib = re.sub(r'\s{2,}', " ", bib)

            bibs = bib.split()
            words = word.split()
            word_st = set(words)
            bib_st = set(bibs)

            for i in range(2):
                if not i:
                    st = word_st
                    name = y.name
                    dct = uniliterals
                else:
                    st = bib_st
                    name = y.bibliography
                    dct = bib_uni

                for word in st:
                    dct.setdefault(word, []).append(self.number)

            for i in range(2):
                if i == 0:
                    lst = words
                    name = y.name
                    dct = bigram
                else:
                    lst = bibs
                    name = y.bibliography
                    dct = bib_bi

                bilits = set()
                for b, c in zip(lst[:-1], lst[1:]):
                    str1 = f'{b} {c}'
                    bilits.add(str1)
                for e in bilits:
                    dct.setdefault(e, []).append(self.number)

            self.get_trigrams(words, bibs)
            if '1998' in uniliterals:
                bb = 8

        total = merge_2dicts(uniliterals, bigram)
        total = merge_2dicts(total, self.tri)
        total2 = merge_2dicts(bib_uni, bib_bi)
        total2 = merge_2dicts(total2, self.btri)
        pi.save_pickle(empty, 'empty', 'hi')
        pi.save_pickle([total, total2], 'tle_index', 'hi')

    def weed_out_middle(self):
        self.fin_txt = {k: v for k, v in self.fin_txt.items()
                        if not reg(r'[mln]', k)}

    def get_trigrams(self, words, bibs):
        for i in range(2):
            if i == 0:
                lst = words
                dct = self.tri
            else:
                lst = bibs
                dct = self.btri

            trilits = set()
            for b, c, d in zip(lst[:-2], lst[1:-1], lst[2:]):
                str1 = f'{b} {c} {d}'
                trilits.add(str1)
            for e in trilits:
                dct.setdefault(e, []).append(self.number)

    def get_name2num(self):
        for k, v in self.texts.items():
            self.name2num.setdefault(v.name, []).append(v.number)


def analyze_texts():
    texts = pi.open_pickle('tle_txts5', 'hi')

    st2 = {'Bigge', 'Amarna-Periode', 'Assouan', 'Gisa',
           'Nubien', 'Sakkara', 'Dakka', 'el-Medina', 'Karnak',
           'Abydos'}

    st = {'Mastaba', 'Felsgrab',
          'Grabkomplex', 'Doppelgrab', 'Grab', 'Aton-Tempel',
          'Temple', 'Mastaba-Komplex', 'Tempel', 'Opettempel',
          'Pyramide', 'Stele',
          'Sarg', 'Dendour', 'chapelle', 'Privatgräber', 'Särge',
          'Liebeslied',
          'Brief', 'Lehre', 'hymne', 'Hymnus', 'hymnus'
                                               'Tumas', 'Edfu', 'Unas-Pyramide', 'Felsinschrift',
          'Achmim', 'Magische', 'Stelen', 'Statue', 'Luxor-Tempel',
          'Papyri', 'Papyrus'}

    st5 = {}

    contents = {}
    coffins = {}
    papyri = {}
    abu_simbel = {}
    hymns = {}
    b = 0
    for k, v in texts.items():
        # v.number2 = v.number
        # v.number = v.name
        # tle_entry.__repr__()

        name = v.name
        name1 = v.name
        name = re.sub(r'[\.;]', " ", name)
        name1 = re.sub(r'[\.;,]', " ", name)
        name_lst = vgf.strip_n_split(name, ",")
        name_lst1 = vgf.strip_n_split(name1, " ")
        name = set(name_lst)
        name1 = set(name_lst1)
        obj = k
        found = False
        for x in name_lst:
            if x.startswith('CG'):
                coffins.setdefault(x, []).append(obj)
                found = True
                break
            elif 'hymnus' in x:
                hymns.setdefault(x, []).append(obj)
                found = True
                break

            elif 'Abu Simbel' in x:
                abu_simbel.setdefault(x, []).append(obj)
                found = True
                break

        if not found:
            for x in [st, st2]:
                st1 = name1 & x
                if len(st1) == 1:
                    found = True
                    str1 = list(st1)[0]
                    contents.setdefault(str1, []).append(obj)
                    break
                elif len(st1) > 1:
                    found = True
                    for z in name_lst1:
                        if z in x:
                            str2 = z
                    contents.setdefault(str2, []).append(obj)
                    break

        if not found:
            for x in name_lst:
                if reg(r'^p[A-Z]', x):
                    papyri.setdefault(x, []).append(obj)
                    found = True
                    break

            if not found:
                contents.setdefault("other", []).append(obj)

    # pi.save_pickle(texts, 'tle_txts', 'hi')
    contents['hymns2'] = list(hymns.values())
    contents['Abu Simbel'] = list(abu_simbel.values())
    contents['coffins'] = list(coffins.values())
    contents['papyri2'] = list(papyri.values())

    pi.save_pickle(contents, 'tle_categories', 'hi')

    return


def get_allen_suffixes():
    allen = to.from_txt2lst(hdir + 'allen_grammar.txt')

    for f, line in en(allen):
        vgf.print_intervals(f, 500)
        lst = line.split()
        for e, z in en(lst):
            if reg(r'\w\.\w', z) and not reg(r'\d', z):
                st.add(z)

    st_allen = set()
    for f, line in en(allen):
        vgf.print_intervals(f, 500)
        lst = line.split()
        for e, z in en(lst):
            if reg(r'\w\.\w', z) and not reg(r'\d', z):
                st_allen.add(line)

    for suffix in study:
        p(f"""
        {suffix}
        """)

        for x in st_allen:
            if "." + suffix in x:
                p(x)


class scrub_datacl:
    def __init__(self, kind=""):
        self.kind = kind
        self.change_dct = {}
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')
        return

    def normal(self):
        self.txts = pi.open_pickle('tle_txts5', 'hi')

    def abnormal(self, lst):
        txts_stand = pi.open_pickle('tle_txts5', 'hi')
        orig_obj = txts_stand['1081']
        self.txts = {'1081': orig_obj}
        self.single_txt()
        pi.save_pickle(txts_stand, 'tle_txt5', 'hi')
        return

    def ad_hoc(self):
        self.make_dct_same()
        self.single_txt()

    def single_txt(self):
        self.copy_words()
        self.elim_destr()
        self.elim_cart()
        self.elim_bold()
        self.divide_dest()
        self.elim_dest_words2()
        self.handle_space()
        self.do_first_clean()
        self.handle_final_period()
        self.replace_iu()
        self.elim_colon()
        self.build_trust()
        self.put_destr_translit()
        self.clean_german()
        self.clean_german2()
        self.elim_ger_destr()
        self.calculate_damage()
        self.indent_german()
        return

    def fix_six(self):
        for y, x in self.txts.items():
            for e, z in en(x.translit_n_info):
                if z == [-6, '..']:
                    x.translit_n_info[e] = [[-6, ".."]]
                else:
                    for f, line in en(z):
                        line[0] = int(line[0])

    def copy_words(self):
        self.fix_six()
        b = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            x.translit = jsonc(x.translit_n_info)
            x.german2 = jsonc(x.translit2german)

    def destruction(self):
        self.destroyed = {'détruit',
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
                          'Zerstrung'
                          }

        self.destroyed_words = {
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

    def save_pickle(self):
        pass
        pi.save_pickle(self.txts, 'tle_txts5', 'hi')
        # pi.save_pickle(self.tle_dct, 'tle_dct6', 'hi')

    def elim_destr(self):
        self.destruction()
        st = set()
        d = 0
        b = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)

            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    num = line[0]
                    word = re.sub(r'[^a-zA-Züöé\s]', " ", word)
                    words = set(word.split())
                    st1 = words & self.destroyed
                    if st1:
                        tword = list(st1)[0]
                        if tword in x.german2[e]:
                            str1 = f"--{tword}--"
                            if str1 in x.german2[e]:
                                x.german2[e] = x.german2[e].replace(str1, '..')
                            else:
                                x.german2[e] = x.german2[e].replace(tword, '..')

                        d += 1
                        lst = [-7, ".."]
                        z[f] = lst

        return

    def elim_cart(self):
        b = 0
        num = 0
        lst = [
            "Kartusche",
            'cartouche',
            "Kartusch",
            "Kartushe",
            'cartouch',
            "artusche",
            "artushe",
            "artusch",
            "artush",
            'Stadtoval',
            "Serech",
        ]
        lst = vgf.sort_lst_by_len(lst)

        st = set()
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)

            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]

                    for d in ['artusch', 'artouch', 'artush', 'Stadtoval', 'Serech']:

                        if d in word:
                            word = word.replace('|', "")
                            for g in lst:
                                if g in word:
                                    word = word.replace(g, "")
                                    z[f] = [int1, word]
                                    ger = x.german2[e]
                                    ger = ger.replace('|', "")
                                    ger = ger.replace(g, "")
                                    x.german2[e] = ger
                                    num += 1
                                    break
                            else:
                                st.add(word)

        p(f'eliminated {num}')
        return

    def elim_bold(self):
        self.get_b_words()
        b = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)

            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    word1 = self.elim_bold2(word, int1)
                    if word1 != word:
                        z[f] = [int1, word1]
                        ger = x.german2[e]
                        oger = ger
                        gers = ger.split()
                        for idx, s in en(gers):
                            q = self.elim_bold2(s, 0)
                            ger = ger.replace(s, q)

                        x.german2[e] = ger

        return

    def get_b_words(self):
        self.tle = pi.open_pickle('tle_dct6', 'hi')
        self.bwords = set()
        self.blemmas = set()
        for y in self.tle.values():
            if reg(r'^b.+b$', y.word):
                word = re.sub(r'[^a-zA-Z0-9]', "", y.word)
                self.bwords.add(word)
                self.blemmas.add(y.lemma_no)
        return

    def elim_bold2(self, str1, lemma_no):
        if lemma_no in self.blemmas:
            return str1

        if reg(r'\[b.+b\]', str1):
            str1 = str1.replace("[b", "")
            str1 = str1.replace("b]", "")

        return str1

    def get_pos(self):
        self.tpos = {
            'v': -100,
            'pd': -101,
            'pp': -102,
            'npt': -103,
            'npc': -104,
            'ncf': -105,
            'npk': -106,
            'npg': -107,
            'm': -108,
            'j': -109,
            'npp': -110,
            'ncnh': -111,
            'i': -112,
            'nc': -113,
            'w': -114,
        }
        self.dest_dct = {
            -100: '[verb]',
            -101: '[dem pronoun]',
            -102: '[pronoun]',
            -103: '[title]',
            -104: '[name]',
            -105: '[noun feminine]',
            -106: '[king]',
            -107: '[god]',
            -108: '[number]',
            -109: '[adjective]',
            -110: '[place]',
            -111: '[noun, non-human]',
            -112: '[prep]',
            -113: '[noun masculine]',
            -114: '..',
        }

    def divide_dest(self):
        # keine Übersetzung vorhanden
        b = 0
        rem_tle = set()
        self.get_pos()
        for y, x in self.txts.items():
            b += 1
            # vgf.print_intervals(b, 500)

            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    if "_" in word and int1 > 0:
                        entry = self.tle_dct[int1]
                        for k, v in self.tpos.items():
                            if entry.pos.startswith(k):
                                lst = [v, '..']
                                z[f] = lst
                                break

        return

    def elim_dest_words2(self):
        b = 0
        self.get_pos()
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = int(line[0])
                    line[0] = int1

                    if int1 > 0 and (reg('^\-.+\-$', word) or
                                     "_" in word):
                        entry = self.tle_dct[int1]
                        for k, v in self.tpos.items():
                            if entry.pos.startswith(k):
                                lst = [v, '..']
                                z[f] = lst
                                break
                            else:
                                lst = [-114, '..']
                                z[f] = lst

    def handle_space(self):
        lst = to.from_txt2lst(hdir + 'temp/spaces.txt')
        splits = set()
        for x in lst:
            if '(?)' in x or "..." in x:
                splits.add(x)
            elif '-pn' in x:
                pass

        b = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            for e, z in en(x.translit):
                f = 0
                while f < len(z):
                    line = z[f]
                    word = line[1]
                    int1 = line[0]
                    if int1 > 0 and not reg(r'\[\s+\]', word) and " " in word:
                        if "..." in word:
                            z[f] = [int1, word[:word.index(" ")]]
                            lst = [-114, '..']
                            z.insert(f + 1, lst)
                        elif '..' in word:
                            z[f] = [int1, word[:word.index("..")]]
                            lst = [-114, '..']
                            z.insert(f + 1, lst)
                            lst1 = [28550, 'jrjw']
                            z.insert(f + 2, lst1)
                        elif 'bHdtj' in word:
                            z[f] = [int1, word[:word.index(" ")]]
                            lst = [400311, 'bHdtj']
                            z.insert(f + 1, lst)
                        elif '(?)' in word:
                            z[f] = [int1, word[:word.index(" ")]]
                            lst = [-114, '..']
                            z.insert(f + 1, lst)
                        else:
                            z[f] = [int1, word.replace(" ", "")]

                    elif word == 'zXAw-a-nswt-n-[ ]-n-xft-Hr':
                        entry = self.tle_dct[int1]
                        z[f] = [int1, entry.word]
                    elif int1 > 0 and " " in word:
                        z[f] = [-114, '..']

                    f += 1

    def do_first_clean(self):
        b = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    word = self.first_clean(word)
                    if word == 0:
                        z[f] = [-114, '..']
                    else:
                        z[f] = [int1, word]

        self.get_all_translits()
        return

    def get_all_translits(self):
        b = 0
        c = 0
        self.all_translits = set()
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            for e, z in en(x.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = int(line[0])
                    word = word.replace('.', '')
                    if int1 > 0:
                        c += 1
                        self.all_translits.add(word)

        # p (f'words {c}')

        return

    def first_clean(self, x):
        dct1 = {
            "wVH": 'wdH',
            'paVy': 'pAy',
            'pAV': 'pAw',
            'msV': 'msT'
        }

        dct2 = {
            ';': '.',
            ',': ".",
            '=': ".",
        }

        for dct in [dct1, dct2]:
            for k, y in dct.items():
                x = x.replace(k, y)

        lst = ['(Pl.)', "VP", '.V', '.pl', '(Du.)', 'V']
        for y in lst:
            x = x.replace(y, "")

        x = re.sub(r'[|<>~\{\}\(\)\!#\]\[\?]', "", x)
        x = x.replace(upside_down_q, "")
        x = re.sub(r'(\.){2,}', ".", x)
        x = x.strip()
        x = re.sub(r'(\s){2,}', " ", x)

        if not x or not reg('\S', x):
            return 0

        return x

    def handle_final_period(self):
        b = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            for e, z in en(x.translit):
                for f, line in en(z):
                    changed = False
                    word = line[1]
                    int1 = line[0]
                    if int1 == -7:
                        z[f] = [-7, '..']
                    elif int1 > 0:
                        if word == '.':
                            z[f] = [-114, '..']
                        else:
                            if "+" in word and not reg(r'[0-9]', word):
                                word = word.replace('+', "")
                                changed = True

                            if word[-1] == '.':
                                word = word[:-1]
                                changed = True
                            if changed:
                                z[f] = [int1, word]

        return

    def clean_german(self):
        b = 0
        c = 0
        for y, x in self.txts.items():
            b += 1
            vgf.print_intervals(b, 500)
            for e, line in en(x.german2):
                if 'zur Übersetzung' in line:
                    pass
                elif 'Übersetzung' in line:
                    line = '....'
                    x.german2[e] = line

                elif reg(r'\[\-+\]', line):
                    if c < 50:
                        pass
                        # p(line)
                    line = re.sub(r'\[\-+\]', '..', line)
                    c += 1
                    # if c < 50:
                    #     p (line)

                    x.german2[e] = line

                elif line == 'no translation':
                    x.german2[e] = '....'

        return

    def make_dct_same(self):
        for x, y in self.tle_dct.items():
            y.word = y.word.replace('i', 'y')
            y.word = y.word.replace('u', 'w')
            y.word = y.word.replace('=', '.')

    def clean_german2(self):
        b = 0
        for x, y in self.txts.items():
            b += 1
            vgf.print_intervals(b, 50)
            for e, z in en(y.german2):
                if reg(r'\[b.+b\]', z):
                    z = z.replace('[b', "")
                    z = z.replace('b]', "")
                    y.german2[e] = z

        for x, y in self.txts.items():

            for e, z in en(y.german2):
                if reg(r'\.{2}', z):
                    lst = z.split()
                    for f, h in en(lst):
                        lst[f] = re.sub('\.{2,}', '..', h)

                    str1 = " ".join(lst)
                    y.german2[e] = str1

        return

    def elim_ger_destr(self):
        self.destruction()
        for x, y in self.txts.items():
            for t, z in en(y.german2):
                forward = True
                delim = ""
                for word in self.destroyed:
                    str1 = "--" + word
                    if str1 in z:
                        idx = z.index(str1)
                        delim = '-'

                        break
                    str1 = word + '--'
                    if str1 in z:
                        idx = z.index(str1) + len(str1)
                        delim = '-'
                        forward = False
                        break
                    str1 = "[" + word
                    if str1 in z:
                        idx = z.index(str1)
                        delim = ']'
                        break
                    str1 = word + ']'
                    if str1 in z:
                        idx = z.index(str1) + len(str1)
                        delim = '['
                        forward = False
                        break

                if delim:
                    # p(z)
                    if forward:

                        u = idx + 2
                        for w in z[idx + 2:]:
                            if w == delim:
                                break
                            u += 1
                        z = z[:idx] + " .. " + z[u + 1:]


                    else:
                        idx -= 2
                        u = idx - 2
                        for w in reversed(z[:idx]):
                            if w == delim:
                                break
                            u -= 1
                        z = z[:u] + " .. " + z[idx + 1:]
                    if not reg(r'\w', z):
                        y.german2[t] = '..'
                        # p('..')
                    else:
                        y.german2[t] = z
                        # p(z)
                    break
        return

    def indent_german(self):
        for x, y in self.txts.items():
            for t, z in en(y.german2):
                str1 = vgf.limit_str_70(z)
                y.german2[t] = str1
        return

    def elim_colon(self):
        pre_lemma = 8
        ulemma = 11
        exceptions = {'As.t-j:ty'}
        dash = {"wsx-HA.tj-r-Hns-pA-tA-jw:Szp.f"}
        wper = {'tA-j:dj.w-jmn'}

        for x, y in self.txts.items():
            for e, z in en(y.translit):

                b = 0
                while b < len(z):
                    line = z[b]
                    word = line[1]
                    int1 = line[0]
                    if int1 > 0 and ":" in word:

                        if word[:2] == 'j:':
                            lst1 = [pre_lemma, 'j.']
                            lst2 = [int1, word[2:]]
                            z.insert(b, lst1)
                            z[b + 1] = lst2
                            b += 1
                        elif word[:2] == 's:':
                            line[1] = word.replace(':', "")

                        elif word in exceptions:
                            line[1] = word.replace(':', "")
                        elif word in dash:
                            line[1] = word.replace(':', "-")
                        elif word in wper:
                            line[1] = word.replace(':', ".")
                        else:
                            lst = word.split(":")
                            lst1 = [11, lst[0]]
                            lst2 = [int1, lst[1]]
                            z.insert(b, lst1)
                            z[b + 1] = lst2
                            b += 1

                    b += 1

        return

    def replace_iu(self):
        exceptions = {"ptol", 'darius'}
        b = 0
        for x, y in self.txts.items():
            vgf.print_intervals(b, 50)
            b += 1
            for e, z in en(y.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    if int1 > 0 and not word[0] == '-':
                        if 'i' in word and all(f not in word for f in exceptions):
                            line[1] = word.replace('i', 'j')
                        elif 'u' in word and 'darius' not in word:
                            line[1] = word.replace('u', 'w')

        # self.get_word2lemma()

    def get_word2lemma(self):
        g = time.time()
        self.word2lemma = {}
        self.word_n_lemma = defaultdict(int)
        b = 0
        for x, y in self.txts.items():
            vgf.print_intervals(b, 50)
            b += 1
            for e, z in en(y.translit):
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    if int1 > 0:
                        word = re.sub(r'[\.\-\']', '', word)
                        str1 = f"{int1}%{word}"
                        self.word2lemma.setdefault(word, set()).add(int1)
                        self.word_n_lemma[str1] += 1

        self.build_freq_table()
        p(round(time.time() - g, 3))

    def build_freq_table(self):
        self.lemma2freq = {}
        for x, y in self.word_n_lemma.items():
            lst = x.split("%")
            dct = self.lemma2freq.get(int(lst[0]))
            if dct:
                dct[lst[1]] = y
            else:
                dct = {lst[1]: y}
                self.lemma2freq[int(lst[0])] = dct

        pi.save_pickle(self.word2lemma, 'word2lemma', 'hi')
        pi.save_pickle(self.lemma2freq, 'lemma2freq', 'hi')

    def replace_iu_dct(self):
        exceptions = {"ptol", 'darius'}

        for x, y in self.tle_dct.items():
            if all(z not in y.word for z in exceptions):
                y.word = y.word.replace('i', 'j')
                y.word = y.word.replace('u', 'w')

        ins = tle_entry()
        ins.word = 'j.'
        ins.lemma_no = 8
        ins.eng_word = "[verb prefix]"
        self.tle_dct[8] = ins
        ins = tle_entry()
        ins.word = '[formerly attached to other word]'
        ins.lemma_no = 11
        ins.eng_word = '[formerly attached to other word]'
        self.tle_dct[11] = ins

        pi.save_pickle(self.tle_dct, 'tle_dct6', 'hi')

    def build_trust(self):
        for x, y in self.txts.items():
            trust = []
            if x == '8768':
                bb = 8

            for e, z in en(y.translit):
                lst = []
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    if int1 > 0:
                        lst.append(word)
                if lst:
                    str1 = " ".join(lst)
                    str1 = vgf.limit_str_70(str1)
                    trust.append(str1)

            y.trust = trust

        # self.calculate_damage()
        return

    def put_destr_translit(self):
        self.destruction()
        self.get_pos()
        right = 0
        wrong = 0
        more = 0
        for x, y in self.txts.items():
            trust = []
            for e, z in en(y.translit):
                lst = []
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    found = True
                    if int1 == -1:
                        found = False
                        for k in self.destroyed:
                            if k in word:
                                line[1] = '..'
                                word = '..'
                                line[0] = -7
                                found = True
                                more += 1
                                break
                    elif int1 == -6:
                        found = True
                        line[0] = -7
                        word = '..'
                    elif int1 < -99:
                        word = self.dest_dct[int1]
                        line[1] = word

                    if found:
                        lst.append(word)
                if lst:
                    str1 = " ".join(lst)
                    str1 = vgf.limit_str_70(str1)
                    trust.append(str1)

            y.trust = trust

    def calculate_damage(self):
        for x, y in self.txts.items():
            words = 0
            blanks = 0
            ewords = 0
            y.threshold = 0
            for e, z in en(y.german2):
                if not reg('\w', z):
                    y.german2[e] = '..'

                y.german2[e] = re.sub(r'\s{2,}', " ", z)
                words += y.german2[e].count(' ') + 1

                if y.german2 == '..':
                    blanks += 2
                    words += 2
                else:
                    blanks += y.german2[e].count('..')

            if not blanks:
                y.condition = 100
            else:
                y.condition = int((blanks / words) * 100)
            for w in y.translit:
                for rw in w:
                    if rw[0] > 0:
                        ewords += 1

            y.word_count = ewords

            if y.word_count < 6:
                y.threshold = 0
            elif y.word_count < 15:
                if blanks < 3:
                    y.threshold = 1
            elif y.word_count < 100:
                if not blanks:
                    y.threshold = 1

                elif blanks / y.word_count < .4:
                    y.threshold = 1
            else:
                y.threshold = 1

    def count_words(self):
        all_words = 0
        legible = 0
        thresholds = 0
        for x, y in self.txts.items():
            twords = 0
            for e, z in en(y.translit):
                for f, line in en(z):
                    int1 = line[0]
                    if int1 > 0:
                        twords += 1
            if y.threshold:
                thresholds += 1
                legible += twords
            all_words += twords

        p(all_words)
        p(legible)

    def inspect_egy(self):
        for x, y in self.txts.items():
            p(f"""
            
            {y.name}
            
            """)

            for e, z in en(y.translit):
                lst = []
                for f, line in en(z):
                    word = line[1]
                    int1 = line[0]
                    if int1 > 0:
                        lst.append(word)
                if lst:
                    str1 = " ".join(lst)
                    pp(str1)
                    p('')

        # b = 0
        # c = 0
        # d = 0
        # for x, y in self.txts.items():
        #     for z in y.german2:
        #         d += 1
        #         if ".." not in z:
        #             lst = z.split()
        #             b += len(lst)
        #             c += 1
        # p (b)
        # p (c)

        return


class fix_suffixes:
    def get_all_suffixes(self):
        allen_suffix = to.from_txt2lst(hdir + 'allen_suffixes')
        del allen_suffix[-1]
        allen_suffix = set(allen_suffix)

        suffixes = defaultdict(int)
        suffix_words = {}
        suffix_words2 = {}
        na_suf_freq = {}
        for x, y in self.word2freq.items():
            lst = x.split('-')
            for z in lst:
                lst1 = z.split('.')
                if len(lst1) > 1:
                    lst1 = lst1[1:]

                    for suffix in lst1:
                        suffix_words.setdefault(suffix, []).append(x)
                        suffixes[suffix] += y

        suffixes = sort_dct_val_rev(suffixes)
        for x, y in suffixes.items():
            if x not in allen_suffix:
                suffix_words2[x] = suffix_words[x]
                na_suf_freq[x] = suffixes[x]

        return


class classify_words:
    def __init__(self):
        self.tle_dct = pi.open_pickle('tle_dct6', 'hi')
        particles = {x: y for x, y in self.tle_dct.items()
                     if y.pos and y.pos[0] in ['e', 'w', 'c', 'q', 'o']}
        pbr = {x: y.frequency for x, y in particles.items()}
        pbr = sort_dct_val_rev(pbr)
        particles2 = {}
        for x, y in pbr.items():
            particles2[x] = self.tle_dct[x]

        for x, y in particles2.items():
            p(y.frequency, y.word, y.eng_word)
            p('')


'''
1. in html_parse_files - specify the folder from which you will get the files



2. make sure you are opening the pickle 'finished_texts7' in the main_text function. note that finished_texts7
is not the whole corpus

2b. set 'kind' in 'main_text' to blank

3. run function 'first' specify in the if clause which files you want to parse

4. In link_middles the file must end with 'l', specify which files you want to process

5. save newly processed files in special folder




key for words
-1 is other info
-7 is .. lacunae
-10 is a comma
-11 is a period
less than -99 are destroyed words of certain types



'''
