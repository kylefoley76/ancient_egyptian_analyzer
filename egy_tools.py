import add_path
from general import *
from global_hiero import *
from hieroglyphs import temp_word
import read_txts, scrub_tle, fix_dct


def txt_loop():
    lst = ['619', '1382', '354', '1589']
    # translations needed
    lst1 = ['1608',
            '20640', '20641', '20643']
    # 20640 Davies, B. G., Egyptian Historical Inscriptions of the Nineteenth Dynasty, Jonsered 1997, 213-19 ff
    # 1608 in pritchard vol 2 pg 89


def loop_german():
    lst = ['426', '427', '429', '430', '354']
    ins = new_txt('426')
    ins.print_german(lst, 1)


class tough_phrases(read_txts.parent):
    def __init__(self, args):
        read_txts.parent.__init__(self, args)
        self.get_date()
        self.past = []
        self.future = []
        lst = to.from_txt2lst_tab_delim(fcdir + f'tough_phrases{self.dat}.txt')
        b = 0
        for egy, eng in lst:
            p(f"{b} of {len(lst)}")
            egy1 = vgf.limit_str_70(egy, 70)
            p(egy1)
            str1 = input('continue')
            eng1 = vgf.limit_str_70(eng, 70)
            p(eng1)
            str1 = input('/ for wrong, return for right')
            if str1 == '/':
                self.future.append((egy, eng))
            else:
                self.past.append((egy, eng))
            b += 1

        to.from_lst2txt(self.future, f'tough_phrases{self.tar_day}.txt')
        to.from_lst2txt(self.past, f'tough_phrases{self.dat}.txt')


class new_txt(fix_dct.run_time_test):
    def __init__(self):
        fix_dct.run_time_test.__init__(self, {"file_name": '858'})
        self.get_txts()


    def main_loop(self):
        for num in self.corpus2:
            self.file_name = num
            self.txt = self.txts[num]
            self.main()


    def count_words_all(self):
        total = 0
        for x in ['354']:
            p (x)
            txt = self.txts[x]
            total = read_txts.count_words(txt, total)



    def main(self):
        lst = [self.file_name]
        self.print_german(lst, 0)
        self.divide_german()
        self.get_all_english()

        """
        ['863', 0, 31],
            ['858', 20, -1],
            ['860', 109, -1]]
        """

    def get_old_english(self, file_num):
        file = hdir + f'tle_trans/{file_num}_english_div.txt'
        lst = to.from_txt2lst(file)
        lst = [str(x) for x in lst]
        engl, _ = self.build_english(lst, 0)
        engl = [" ".join(x) for x in engl]
        for e, x in en(engl):
            engl[e] = re.sub(r'=\d+\**', '', x)

        return engl

    def get_answers(self, answers, z, entry):
        if entry:
            pos = entry.pos
            rank = entry.rank
            word = entry.eng_word
            answers.append(f"{z[0]}\t{rank}\t{pos}\t\t{z[1]}\t\t{word}")

    # def fix_old(self, start, stop):
    #     pass
    #
    # def fix_loop(self):
    #     dct = {
    #         '863': [0, 31],
    #         '858': [20, -1],
    #         '860': [109, -1]
    #     }
    #     lst = ['790', '860', '943', '939']
    #
    #     for num in self.corpus:
    #         self.file_name = num
    #         self.file = num
    #         self.txt = self.txts[num]
    #
    #         if not hasattr(self.txt, 'english2'):
    #             str1 = hdir + f'tle_trans/{num}_english_div.txt'
    #             self.eng_file = str1
    #             self.en_lst = to.from_txt2lst(self.eng_file, 1)
    #             self.txt.english2, _ = self.build_english(self.en_lst)
    #             for e, x in en(self.txt.english2):
    #                 self.txt.english2[e] = " ".join(x)
    #
    #
    #         if hasattr(self.txt, 'revised'):
    #             if type(self.txt.revised[0][0]) != list:
    #                 self.get_revised_egy(self.txt.revised)
    #                 self.fix_new(1)
    #                 p(f'string {num}')
    #
    #             elif any(len(z) > 3 for x in self.txt.revised
    #                      for z in x):
    #                 pass
    #                 p(f'normal {num}')
    #             else:
    #                 p(num)
    #                 self.fix_new()
    #         else:
    #             p(f'not revised {num}')
    #             if num == '860':
    #                 start = 109
    #             elif num == '858':
    #                 start = 20
    #             else:
    #                 start = 0
    #
    #             self.divide_german(start)
    #             self.get_revised_egy(self.txt.revised)
    #             self.fix_new(1)
    #
    #             bb = 8
    #         if num == '790':
    #             del self.txt.revised[0]
    #         if self.txt.trust == []:
    #             self.build_trust()
    #
    #
    #
    #         if len(self.txt.english2) != len(self.txt.trust):
    #             bb = 8
    #
    #
    #         # assert len(self.txt.english2) == len(self.txt.trust)
    #
    #     pi.save_pickle(self.txts, 'tle_txts5', 'hi')
    #
    # def fix_new(self, ignore_pos=0):
    #     file = hdir + f"tle_trans/{self.file_name}_divided.txt"
    #     file_an = hdir + f"tle_trans/{self.file_name}_div_answers.txt"
    #     lst = []
    #     answers = []
    #     for z in self.txt.revised:
    #         for x in z:
    #             lem = x[1]
    #             entry = 0
    #             if lem > 0:
    #                 pos = 'z'
    #                 entry = self.tle_dct.get(lem)
    #                 if entry:
    #                     pos = entry.pos
    #                 if not ignore_pos:
    #                     x.insert(2, pos)
    #             lst.append(x)
    #             self.get_answers(answers, x, entry)
    #     to.from_lst2txt_tab_delim(lst, file)
    #     to.from_lst2txt(answers, file_an)

    # def loop_divide_egy(self):
    #     for x in lst:
    #         self.file_name = x
    #         self.txt = self.txts[x]
    #         if x == '860':
    #             start = 109
    #         else:
    #             start = 0
    #         self.divide_german(start)

    def divide_german(self, start=0,open_f=0):
        stop = 31
        lst = []
        answers = []
        e = 0
        for x in self.txt.translit[start:]:
            for z in x:
                if z[0] < 1:
                    lst.append([e, z[0], z[1]])
                else:
                    entry = self.tle_dct.get(z[0])
                    if entry:
                        pos = entry.pos
                        rank = entry.rank
                        word = entry.eng_word
                        lst.append([e, z[0], pos, z[1]])
                        answers.append(f"{z[0]}\t{rank}\t{pos}\t\t{z[1]}\t\t{word}")
                    else:
                        answers.append(f"{z[0]}\t{z[1]}\t[missing]")
                        lst.append([e, z[0], "z", z[1]])

                e += 1

            lst.append([e, -11, '.'])
            e += 1
        self.txt.revised = lst
        file = hdir + f'tle_trans/{self.file_name}_divided.txt'
        file2 = hdir + f'tle_trans/{self.file_name}_div_answers.txt'
        to.from_lst2txt_tab_delim(lst, file)
        to.from_lst2txt(answers, file2)
        if open_f:
            vgf.open_txt_file(file)
            vgf.open_txt_file(file2)

    def print_german(self, lst, open_f=False):
        texts = pi.open_pickle('tle_txts5', 'hi')
        for id in lst:
            obj = texts[id]
            # p (f'word count: {obj.words}')

            ger_lst = []
            for e, x in en(obj.german2):
                lst1 = [e, x]
                ger_lst.append(lst1)

            trust_lst = []
            for e, x in en(obj.trust_old):
                lst1 = [e, x]
                trust_lst.append(lst1)

            original_translit = []
            for e, x in en(obj.translit_n_info):
                lst3 = [z[1] for z in x]
                str1 = " ".join(lst3)
                lst5 = [e, str1]
                original_translit.append(lst5)

            trust_file = hdir + f'tle_trans/{id}_trust.txt'
            german = hdir + f'tle_trans/{id}_german.txt'
            otrans = hdir + f'tle_trans/{id}_otranslit.txt'

            to.from_lst2txt_tab_delim(trust_lst, trust_file, 1)
            to.from_lst2txt_tab_delim(ger_lst, german, 1)
            to.from_lst2txt_tab_delim(original_translit, otrans, 1)
            if open_f > 0:
                vgf.open_txt_file(trust_file)
                if open_f == 2:
                    vgf.open_txt_file(german)
                    vgf.open_txt_file(otrans)

    def get_all_english(self):
        # p('just use first letter')
        # str1 = input('other english trans ')
        str1 = ''
        lst = [""]
        if str1:
            lst1 = str1.split()
            lst += lst1
        for e, x in en(lst):
            self.divide_txt(self.file_name, x, e)

    def print_english(self):
        self.txt = self.txts[self.num]
        file = hdir + f'tle_trans/{self.num}_english_final.txt'
        to.from_lst2txt(self.txt.english2, file)
        vgf.open_txt_file(file)

    def divide_txt(self, num, name="", idx=0):
        if name:
            name = "_" + name
        file = hdir + f'tle_trans/{num}_english{name}.txt'
        file2 = hdir + f'tle_trans/{num}_english{name}_div.txt'
        lst = to.from_txt2lst(file)
        lst1 = []
        for e, line in en(lst):
            line = str(line)
            line = re.sub(r'^(\d|\-|\,){1,}', "", line)
            line = line.strip()
            line = line.replace("|", "")
            lst[e] = line

        for line in lst:
            if reg(r'\S', line):
                lst2 = line.split()
                for z in lst2:
                    lst1.append(z)
                    lst1.append("")
                lst1.append('|')

        if not idx:
            lst1 = self.alter_punct(lst1)
        for x in range(30):
            lst1.insert(0, "")
        to.from_lst2txt(lst1, file2)
        vgf.open_txt_file(file2)
        return

    def alter_punct(self, lst1):
        e = 0
        lst2 = []
        while e < len(lst1):
            sent = lst1[e]
            sent = sent.strip()
            b = len(sent)
            for let in reversed(sent):
                if reg(r'[a-zA-Z0-9]', let):
                    break
                else:
                    bb = 8
                b -= 1
            if b != len(sent):
                sent1 = sent[:b]
                sent2 = sent[b:]
                lst2.append(sent1)
                lst2.append(sent2)
            else:
                lst2.append(sent)
            e += 1

        return lst2


class speed_read(read_txts.parent):
    def __init__(self):
        read_txts.parent.__init__(self, {})
        self.get_txts()
        bk = to.from_txt2lst(hdir + 'bookmark.txt')
        self.file_num = str(bk[2])
        self.bk = bk[3]

    def loop_corpus(self):
        idx = self.corpus.index(self.file_num)
        for self.file_num in self.corpus[idx:]:
            self.main()
        return

    def all_synoptic(self):
        dct = {
            'sinuhe': [('848', 0, 29),
                       ('842', 20, -1)],
            'peasant': [
                ['863', 0, 31],
                ['858', 20, -1],
                ['860', 109, -1]],
        }

    def build_synoptic(self):
        dct1 = {
            'sinuhe': ['848', '842'],
            'peasant': ['863', '858', '860']
        }
        for x, y in dct1.items():
            obj = self.txts[x]
            obj.english2 = []
            obj.revised = []
            obj.trust = []

            for z in y:
                obj2 = self.txts[z]
                obj.english2 += obj2.english2
                obj.trust += obj2.trust
                obj.revised += obj2.revised

        pi.save_pickle(self.txts, 'tle_txts5', 'hi')



    def main(self):
        self.txt = self.txts[self.file_num]
        if self.file_num in ['1081', '369']:
            self.new_system()
        else:
            self.old()

    def old(self):
        engl = self.txt.english2

        bk = self.bk
        egy = self.txt.trust
        for e, eg in en(egy[bk:]):
            b = e + bk
            p(f'{b} of {len(egy)}')
            if e == 0:
                p(eg)
            else:
                eng = engl[b - 1]
                eng = eng[:-1] if eng[-1] == '|' else eng
                p(f"""

{vgf.limit_str_70(eng, 70)}

{vgf.limit_str_70(eg, 70)}

                """)

            str1 = input('continue, q to quit')
            if str1 == 'q':
                self.quit_read(e)

        p(engl[-1])

    def quit_read(self, e):
        lst = to.from_txt2lst(hdir + 'bookmark.txt')
        lst[2] = self.file_num
        lst[3] = e + self.bk
        to.from_lst2txt(lst, hdir + 'bookmark.txt')
        sys.exit()

    def new_system(self):
        bk = self.bk
        egy = self.txt.trust
        eng = self.txt.english2
        for i in range(bk, len(egy), 3):
            one = egy[i]
            two = egy[i + 1]
            three = egy[i + 2]
            eg = f"{one} {two} {three}"
            eg = vgf.limit_str_70(eg)

            if i > 0:
                en1 = eng[i - 3]
                en2 = eng[i - 2]
                en3 = eng[i - 1]
                en1 = f"{en1} {en2} {en3}"

            else:
                en1 = ""
            en1 = vgf.limit_str_70(en1)

            p("""
            return to show english and the next egyptian
            / to show word meanings

            """)
            str1 = input('see english?, q to quit ')

            str1 = 0
            if not str1:
                p(f"""

{vgf.limit_str_70(en1, 70)}

{vgf.limit_str_70(eg, 70)}

                """)
            elif str1 == 'q':
                self.quit_read(i)
