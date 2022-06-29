

from general import *
import add_path
import random
import pyautogui
from PIL import Image
from global_hiero import *
from mine_tle import tle_entry

### inserted the names of the signs where Allen forgot them up to F12
class entry:
    def __init__(self, num):
        self.name = ""
        self.notes = ""
        self.determinatives = []
        self.phonogram = ""
        self.phonogram2 = []
        self.phonogram3 = []
        self.ideogram = ""
        self.variant_of = ""
        self.its_variants = []
        self.its_variants2 = []
        self.holonyms = ""
        self.meronyms = ""
        self.confusions = ""
        self.num = num
        self.full_txt = ""
        self.combination = ""
        self.glyph = ""
        self.unicode = ""
        self.uni_dec = 0

    def __repr__(self):
        return self.num




# david lord, slack
class split_sentences:
    def __init__(self):
        self.all_info = "/users/kylefoley/downloads/hieroglyphs/no_unicode/all_info/"
        self.sign2info = pi.open_pickle('process_symbols/sign2info14', 'hi')
        self.get_dcts()
        self.check_variants()
        return

    def get_other_resources(self):
        self.allen = pi.open_pickle('allen_egyptian3', "hi")
        # self.num2descr = pi.open_pickle('num2descr', 'hi')

    def double(self):
        """
                r13 also in g
                r61 also in i
                y10 also in m
                """

        dct1 = {
            's40': ['wAb'],
        }

    def get_glyph_info_from_phone(self, str1):
        lst = self.phone2num.get(str1)
        if lst:
            for v in lst:
                self.print_glyph(v.name, v.num, v, {})
        else:
            p('no glyph with this sound')

    def put_info_on_images(self):
        from PIL import Image
        tdir = "/users/kylefoley/downloads/hieroglyphs/no_unicode/all_info/"
        sdir = "/users/kylefoley/downloads/hieroglyphs/no_unicode/no_info/"
        no_info = os.listdir(sdir)
        from PIL import ImageFont
        from PIL import ImageDraw

        font_dir = "/Library/Fonts/Microsoft/Times New Roman.ttf "
        font_dir = "/System/Library/Fonts/Palatino.ttc"
        font_dir = "/System/Library/Fonts/sfcompactdisplay-bold.otf"
        # font1 = ImageFont.truetype(font_dir, 16)
        lst = ['g48a', 'h6b', 'm43a', 'i64', 'm63', 'n46b', 'r61', 'b24', 'c175a']
        # a119 needs 3 rows
        for file in no_info:
            # if file =="c175a.png":
            if file != ds:
                p(file)
                img = Image.open(sdir + file)
                iname = file[:-4]
                ins = self.sign2info[iname]
                name = ins.name
                more_left = False
                if len(name) > 20:
                    b = len(name) * .4
                    b = int(b)
                    idx = name[b:].index(" ")
                    lst1 = list(name)
                    lst1.insert(b + idx, "\n")
                    name = "".join(lst1)
                    more_left = True

                phono = ""
                if ins.phonogram3:
                    phono = " ".join(ins.phonogram3)

                if phono:
                    str1 = f"{iname}  {phono}  {name}"
                else:
                    str1 = f"{iname}  {name}"

                draw = ImageDraw.Draw(img)
                # font = ImageFont.truetype(<font-file>, <font-size>)
                # font = ImageFont.truetype("sans-serif.ttf", 16)
                font = ImageFont.truetype(font_dir, 32)
                # draw.text((x, y),"Sample Text",(r,g,b))
                width, height = img.size
                if more_left:
                    x = int(width * .20)
                else:
                    x = int(width * .30)

                if iname in lst:
                    y = int(height * .85)
                else:
                    y = int(height * .07)

                draw.text((x, y), str1, (0, 0, 0), font=font)
                img = img.resize((int(width * .4), int(height * .4)), Image.ANTIALIAS)
                img.save(tdir + file, quality=95)
                # im = Image.open(tdir + file)
                #
                # im.show()

                # str1 = input('move on: ')

                # resize((x,y))

    # d10 and its parts are not phonograms

    def test_phonograms(self, review=False):
        lst = []
        for_review = []
        for x, y in self.sign2info.items():
            if y.phonogram3 and not y.notes == 'not in allen' and \
                    y.glyph and all(len(z) < 3 for z in y.phonogram3):
                lst.append(y)

        tcorrect = 0
        ttotal = 0
        random.shuffle(lst)
        for ins in lst:
            p('')
            p("      " + ins.glyph)
            p('')
            str1 = input('input phonograms: ')
            p(ins.phonogram3)
            p(ins.name)
            p(ins.num)
            p("")
            if str1:
                lst1 = str1.split()
                st = set(lst1)
                correct = len(st & set(ins.phonogram3))
            else:
                correct = 0
            total = len(ins.phonogram3)
            ttotal += total
            tcorrect += correct
            score = int((tcorrect / ttotal) * 100)
            p(f"score: {score}")

    def get_num_from_name(self, str1):
        num = self.name2num.get(str1)
        if num:
            p(num)
        else:
            p(f'not found {str1}')

    def get_name_from_num(self, str1):
        num = self.num2name.get(str1)
        if num:
            p(num)
        else:
            p(f'not found {str1}')

    def search_by_category(self):
        dct = pi.open_pickle('process_symbols/categories', 'hi')
        dct['aa'] = 'unclassified'
        self.by_category = dct
        self.by_shape = pi.open_pickle('process_symbols/by_shape', 'hi')

        self.num2shape = {}
        for e, x in en(self.by_shape.keys()):
            p(e + 1, x)
            self.num2shape[str(e + 1)] = x

        while True:
            try:
                p ("""
                1 - take an exact name return gard num
                2 - takes an english word, prints all which have that
                    word in their name
                3 - takes a gard category, prints all in that category
                4 - takes num 1-4 prints all in verti, horiz etc
                5 - takes a gard num returns name and image
                6 - prints list of categories
                7 - take a phonogram and prints the glyphs
                q - to end
                """)

                cat = input('choose category: ')

                assert cat[0] in ['1','2','3','4', '5', '6', '7', 'q']
                num = cat[0]
                str1 = ""
                if len(cat) > 1:
                    str1 = cat[2:]

                if num == '1':
                    self.get_num_from_name(str1)
                elif num == '5':
                    self.get_name_from_num(str1)
                elif num == '3':
                    self.print_category(str1)
                elif num == '4':
                    self.print_shape_category(str1)
                elif num == '2':
                    self.search_by_name(str1)
                elif num == '6':
                    for x, y in self.by_category.items():
                        p(x, y)
                    for x, y in self.num2shape.items():
                        p(x, y)
                elif num == "7":
                    self.get_glyph_info_from_phone(str1)

                elif num == 'q':
                    return


            except:
                p ('wrong input')

    def print_category(self, cat):
        no_unicode = {}
        b = len(cat)
        for x, ins in self.sign2info.items():
            if x[:b] == cat:
                self.print_glyph(ins.name, ins.num, ins, no_unicode)
        self.print_no_unicode(no_unicode)

    def print_shape_category(self, cat):
        no_unicode = {}
        cat = self.num2shape[cat]
        values = self.by_shape[cat]
        for gnum in values:
            ins = self.sign2info.get(gnum)
            if not ins:
                p(f'do not have {gnum}')
            else:
                self.print_glyph(ins.name, ins.num, ins, no_unicode)


    def search_by_name(self, str1):
        no_unicode = {}
        lst1 = str1.split()
        st1 = set(lst1)

        for gname, gnum in self.name2num.items():
            lst5 = gname.split()
            lst5 = [z[:-1] if z[-1].isdigit() and len(z) > 1 else z for z in lst5]
            lst5 = [z[:-1] if z[-1] == "*" else z for z in lst5]
            st5 = set(lst5)
            if st5 & st1:
                ins = self.sign2info[gnum]
                self.print_glyph(gname, gnum, ins, no_unicode)

        self.print_no_unicode(no_unicode)

    def print_no_unicode(self, no_unicode):
        p(f"there are {len(no_unicode)} which meet this requirement")
        p('and have no unicode')
        p('')

        for e, x in en(list(no_unicode.keys())):
            p(e, x)

        p('')
        p('input the numbers you want to look up or x for none')
        nums = input("input: ")
        if nums == 'x':
            return
        else:
            lst2 = nums.split()
            lst2 = [int(x) for x in lst2]
            self.no_unicode2(lst2, no_unicode)


    def no_unicode2(self, lst2, no_unicode, print_all=False):
        e = 0
        for k, v in no_unicode.items():
            if e in lst2 or print_all:
                file = self.all_info + v + ".png"
                im = Image.open(file)
                im.show()
                str2 = input('move on')

            e += 1

    def print_glyph(self, gname, gnum, ins, no_unicode):
        if ins.notes == 'not in allen':
            return

        elif ins.glyph:
            p('')
            if ins.phonogram3:
                str2 = " ".join(ins.phonogram3)

                p(f"{ins.glyph}     {ins.num} {str2}   {ins.name}")

            else:
                p(f"{ins.glyph}     {ins.num}   {ins.name}")


        else:
            no_unicode[gname] = gnum

    def random_literals(self, answers=True):
        lst = [x for x, y in self.sign2info.items() if y.phonogram3 and y.glyph]
        random.shuffle(lst)
        for x in lst[:20]:
            item = self.sign2info[x]
            if answers:
                p(f"{item.glyph}  {item.phonogram3}  {item.name}")
                p('')
            else:
                p(f"{item.glyph}  {item.name}")
                p('')
                str1 = input('what are the phonograms')
                p(f"{item.phonogram3}")
                p('')

    def check_variants(self):
        parent2child = {}
        is_a_variant = []

        for k, v in self.sign2info.items():
            if v.variant_of:
                is_a_variant.append(v)
                for x in v.variant_of:
                    parent2child.setdefault(x, []).append(k)

        for k, v in parent2child.items():
            obj = self.sign2info.get(k)
            if obj:
                obj.its_variants2 = v
            else:
                assert False

        for k, v in self.sign2info.items(): v.its_variants2 = []

        for k, v in parent2child.items():
            self.sign2info[k].its_variants2 = v

        self.parent2child = parent2child

        for k, v in self.sign2info.items():
            if v.variant_of and not v.phonogram3:
                lst1 = []
                for z in v.variant_of:
                    if z == '0':
                        assert False
                    else:
                        obj = self.sign2info.get(z)
                        for phono in obj.phonogram3:
                            lst1.append(phono)

                if lst1:
                    p(k, lst1)
                    v.phonogram3 = lst1

        for k, v in self.sign2info.items():
            for phon in v.phonogram3:
                self.phone2num.setdefault(phon, []).append(v)


        return

    # def inspect_variants(self):
    #
    #     b = 0
    #     for k, v in parent2child.items():
    #         p('')
    #         p('')
    #         p(f"parent {k}")
    #
    #         for z in v:
    #             b += 1
    #             item = self.sign2info[z]
    #             p(f'child{z}')
    #             pp(item.full_txt)
    #             p('')
    #         if b > 50:
    #             break

    def get_dcts(self):
        self.num2name = {}
        self.name2num = {}
        self.phone2num = {}

        for k, v in self.sign2info.items():
            if v.name:
                self.num2name[k] = v.name
                if v.name in self.name2num:
                    assert False, f"{v.name} is taken"
                self.name2num[v.name] = k

    def save_pickle(self):
        pi.save_pickle(self.name2num, 'name2num', 'hi')
        pi.save_pickle(self.num2name, 'num2name', 'hi')
        pi.save_pickle(self.phone2num, 'phone2num', 'hi')

    def linkchildren2parents(self):
        variants = ['Variant of', 'Older variant of', 'Ocasional variant of',
                    'Later variant of', 'More common variant of', ]
        has_variant = [', Variants',
                       'Variants ,', 'Variants', 'Variant']

        mid_sents = ['variant of']

        # for k, v in self.sign2info.items():
        #     if v.variant_of:
        #         for z in v.variant_of:
        #             item = self.sign2info.get(z)
        #             if item and item.phonograms2:
        #                 if not v.phonogram2:
        #                     v.phonogram2 = []
        #                 v.phonogram2 += item.phonogram2
        #
        #
        # pi.save_pickle(self.sign2info, 'sign2info', 'hi')

        return

    # def old_get_headers(self):
    #     self.sign2info = pi.open_pickle('sign2info', 'hi')
    #     for k, v in self.sign2info.items():
    #
    #         if v.full_txt[0] == '(' and v.full_txt[-1] == ")":
    #             p(k)
    #             str1 = v.full_txt[1:-1]
    #
    #             str1 = str1.strip()
    #             str1 = str1.replace('  ', " ")
    #             str1 = str1.replace("." + chr(8221), chr(8221) + ".")
    #
    #             lst = str1.split('.')
    #             lst = [x.strip() for x in lst if x]
    #             self.num2descr2[k] = lst

    def get_headers(self):
        two_words = [
            "Determinative in", 'Ideogram for', 'Variant of', 'Older variant of',
            'Determinative of', 'Determinative for', 'Ocassional variant of',
            'Part of', 'Later variant of', 'In hieratic', 'More common variant of',
            "Ideogram in", 'Sometimes for', ', Variants', 'Variants ,',
            "Determinative", 'Phonogram', 'Ideogram', 'Variant', "Variants"]

        no_name = ['Determinative', 'Ideogram', ',', 'Variant', 'Variants',
                   'Occasional', 'Part', 'Later', 'More', 'Phonogram', 'Older']

        exceptions = ['Part of a ship']
        lst2 = ['determinative', 'ideogram', 'phonogram', 'hieratic', 'variant']
        for k, v in self.num2descr.items():
            for sent in v:
                if any(z in sent for z in lst2):
                    p(k)
                    p(sent)
                    p('')

        variants = ['Variant of', 'Older variant of', 'Ocassional variant of',
                    'Later variant of', 'More common variant of', ]
        has_variant = [', Variants',
                       'Variants ,', 'Variants', 'Variant']

        # When doubled
        str6 = 'rare variant'
        irreg_phono = ['gs', f"{a2}{d2}", 'sn']
        self.sign2info = {}

        for k, v in self.num2descr.items():
            ins = entry(k)
            name = True
            ins.full_txt = ". ".join(v)
            first = v[0]
            words = first.split()

            if words[0] in self.num2descr.keys():
                ins.meronyms = v
                name = False
            elif words[0] in no_name:
                name = False

            for e, sent in en(v):
                if sent == 'Unknown':
                    ins.name = 'Unknown'

                elif not e and name:
                    ins.name = sent
                else:
                    ideo_for_same = False
                    words = sent.split()
                    word1 = words[0]

                    if 'also ideogram for same' in sent:
                        sent = sent[:-22]
                        ideo_for_same = True

                    if word1 == 'Determinative':
                        for z in ['Determinative for', 'Determinative in',
                                  'Determinative of', 'Determinative']:

                            if sent.startswith(z):
                                ins.determinatives = sent[len(z) + 1:]
                                if ideo_for_same:
                                    ins.ideogram = sent[len(z) + 1:]

                                break

                    elif word1 == 'Phonogram':
                        ins.phonogram = sent[len('Phonogram') + 1:]

                    elif sent.startswith('Sometimes for'):
                        ins.ideogram = sent[len('Sometimes for') + 1:]

                    elif word1 == 'Ideogram':
                        for z in ['Ideogram for', 'Ideogram in', 'Ideogram']:
                            if sent.startswith(z):
                                ins.ideogram = sent[len(z) + 1:]
                                break

                    elif any(sent.startswith(x) for x in variants):
                        for x in variants:
                            if sent.startswith(x):
                                ins.variants = sent[len(x) + 1:]
                                break

                    elif any(sent.startswith(x) for x in has_variant):
                        for x in has_variant:
                            if sent.startswith(x):
                                ins.its_variants = sent[len(x) + 1:]
                                break

                    elif not sent.startswith('Part of a') and \
                            sent.startswith("Part of"):
                        ins.holonyms = sent[len("Part of "):]

            self.sign2info[k] = ins
        pi.save_pickle(self.sign2info, 'sign2info', "hi")

        return

    def build_num2name(self):
        oexcept = ['Aa16']
        exceptions = ['v48', 'v3', 's28',
                      'o15', 'n13',
                      'd218a',
                      ]

        rep = ['Aa13', 'S29', 'O34', 'S29', 'W10', 'X1', 'N11', 'N14',
               'O43']

        self.name2num = {}
        for k, v in self.sign2info.items():
            if k not in exceptions:
                if v.name and not v.name == 'Unknown':
                    if v.name.startswith('Possibly '):
                        v.name = v.name[len('possibly '):] + "*"

                    self.name2num.setdefault(v.name.lower(), []).append(k)

        ambiguous = []
        for k, v in self.name2num.items():
            if len(v) > 1:
                ambiguous += v

        for k, v in self.sign2info.items():
            v.full_txt = v.full_txt.lower()

        for k, v in self.name2num.items():
            self.name2num = [z.lower() for z in v]

        dct8 = {
            'a84': 'standing man with hand to mouth*',
            'a25': 'man striking with one arm*',
            'd5': 'eye with paint and lashes*',
            'd36a': 'forearm hands open*',
            'd42': 'forearm with palm down hand open*',
            'd47': 'curled hand*',
            'd50': 'vertical finger*',
            'f27': 'cowskin curved*',
            'f39': 'spine and half-spinal cord*',
            'm38': 'bundle of flax more lines*',
            'n21': 'small tongue of land*',
            's19': 'seal on necklace large*',
            's40': 'animal-headed staff large head*',
            't7': 'round axe*',
            't8': 'straight dagger*',
            't9': 'flat bow*',
            'u6': 'three-sticked hoe*',
            'u23': 'long chisel*',
            'aa27': 'small spindle*',
            'v16': 'large hobble for cattle*',
            'v38': 'elliptical bandage*',
            'w10a': 'pot with dipper*',
            'w24': 'round pot*'}

        dct9 = {
            'aa6': 'large m*',
            'aa7': 'hot iron(',
            'aa9': 'cylinder*',
            'aa13': 'live whip*',
            'aa19': 'arch*',
            'aa21': 'eiffel tower*',
            'aa25': 'curved cross*',
            'aa26': 'cactus*',

        }
        # o1, aa30

        for x, y in dct9.items():
            self.sign2info[x].name = y

        self.num2name = {}
        for x, y in self.sign2info.items():
            if y.name:
                self.num2name.setdefault(y.name, []).append(x)
                if len(self.num2name[y.name]) > 1:
                    p(x)

        for x in exceptions:
            item = self.sign2info[x].name
            lst = item.split()

            for z in en(lst):
                w = self.sign2info.get(z)
                if w:
                    item = item.replace(z, w.name)
            p(item)
            self.sign2info[x].name = item

        return




def inspect(sign2info):
    atts = ['determinatives', 'phonogram', 'ideogram', 'variant_of',
            'its_variants', 'holonyms']
    for att in atts:
        b = 0
        for k, v in sign2info.items():
            item = getattr(v, att)
            if item:
                b += 1
                p('')
                p(k, item)
                p(v.full_txt)
                p('')
                if b > 70:
                    break

    for k, v in sign2info.items():
        if v.name:
            p(v.name)

    return

if eval(not_execute_on_import):

    args = vgf.get_arguments()
    args.append('cat')
    # args.append('water')


    if 'ph' in args:
        assert args[2]
        ins = split_sentences()
        ins.get_glyph_info_from_phone(args[2])
    elif 'te' in args:
        ins = split_sentences()
        ins.random_literals(False)
    elif 'cat' in args:
        ins = split_sentences()
        ins.search_by_category()
    elif 'tph' in args:
        ins = split_sentences()
        ins.test_phonograms()
    elif 'se' in args:
        ins = split_sentences()
        assert args[2]
        ins.search_by_name(args[2])
    elif 'ss' in args:
        split_sentences()
