

import sys
import add_english
import read_txts
import scrub_tle
import hieroglyphs
import ocr
from global_hiero import *
import filter_txt
import mine_tle
from mine_tle import tle_entry, tle_file
import fix_dct
import egy_tools

args = vgf.get_arguments()
p = print

for e, x in enumerate(args):
    try:
        x = int(x)
        args[e] = x
    except:
        pass


if len(args) < 2:
    args = ['fd_rtt_fu']
    args = ['fd_rtt_in']
    args = ['fd_rtt_ol']
    args = ['rt_rw']
    args = ['et_sr']
    args = ['fd_lg']
    args = ['et_nt']
    args = ['fd_bs']
    args = ['et_nt_dg']
    args = ['ae_tt']
    args = ['t5']
    args = ['fd_rtt_fnl']
    args = ['rt_tv']
    args = ['et_nt_12']
    args = ['et_nt_pg']
    args = ['rt_fr']
    args = ['ft_ep']
    args = ['ft_t5']
    args = ['ft_et']
    args = ['et_nt_lo']
    args = ['fd_rtt_jc']
    args = ['rtt']





if "rt_re" in args:
    dct = {
        'kind': 'otf',
        'new_test':0,
        'keep_score':0,
        'debug':1,
        'file_name': '369',
        'day':0,
        'start':0,
        'tar_day':0,
        'estart':0,
    }

    ins = read_txts.read_egy(dct)
    ins.step2b()

elif 'ft_t5' in args:
    filter_txt.temp5()

elif 'et_nt_dg' in args:
    ins = fix_dct.new_txt()
    ins.divide_german()


elif 'ft_et' in args:
    filter_txt.extract_text()

elif 'rt_fr' in args:
    dct = {
        'day': 0,
        'tar_day':0
    }
    try:
        dct['day'] = args[2]
        dct['tar_day'] = args[3]
    except:
        pass


    ins = read_txts.parent(dct)
    ins.get_date()
    _ = ins.get_to_study(ins.tar_day)
    ins.future_study = _
    ins.fix_apostrophe2(ins.future_study)
    ins.for_review()

elif 'et_nt' in args:
    ins = egy_tools.new_txt()
    ins.main()

elif 'et_nt_lo' in args:
    ins = egy_tools.new_txt()
    ins.main_loop()



elif 'fd_lg' in args:
    fix_dct.loop_german()

elif 'sd_w2l' in args:
    ins = scrub_tle.scrub_datacl()
    ins.normal()
    ins.get_word2lemma()



elif 'et_sr' in args:
    ins = egy_tools.speed_read()
    ins.loop_corpus()

elif 'et_sr_bs' in args:
    ins = egy_tools.speed_read()
    ins.build_synoptic()

elif 'et_nt_cw' in args:
    ins = egy_tools.new_txt()
    ins.count_words_all()

elif 'et_tp' in args:
    dct = {
        'day': 0,
        'tar_day': 0
    }
    egy_tools.tough_phrases(dct)




elif 'rtt' in args:
    dct = {
        #'file_name': '1081',
        'file_name': '1382',
        'tar_day': -1,
        'day':0,
        'debug': 0,
    }
    ins = fix_dct.run_time_test(dct)
    ins.just_check()

elif 'et_nt_pe' in args:
    ins = fix_dct.new_txt('872')
    ins.print_english()

elif 'fd_rtt_ol' in args:
    dct = {
        'file_name': '1081',
        'day': 0,
        'tar_day':0
    }
    try:
        dct['day'] = args[2]
        dct['tar_day'] = args[3]
    except:
        pass


    ins = fix_dct.run_time_test(dct)
    ins.link_words()

elif 'fd_rtt_fu' in args:
    dct = {
        'file_name': '1081'

    }
    ins = fix_dct.run_time_test(dct)
    ins.full()

elif 'ae_pt2a' in args:
    add_english.prepare_txt2audio()

elif 'hi_uti' in args:
    hieroglyphs.use_tle_index()

elif 'ocr_rt2' in args:
    dir1 = hdir + 'books/parkinson poems/'
    dest = hdir + 'books/parkinson poems 2/'
    ocr.rotate270(dir1, dest)


elif args[1] == 'tv':

    dct = {
        'day': 1,
        'tar_day':-1
    }
    try:
        dct['day'] = args[2]
        dct['tar_day'] = args[3]
    except:
        pass

    ins = read_txts.test_vocab(dct)
    ins.review_words()

elif 'rt_cw' in args:
    read_txts.count_words()


elif "mt_st" in args:
    mine_tle.scrape_tle()

elif 'mt_hp' in args:
    ins = mine_tle.process_tle()
    ins.html_parse_files()

elif 'mt_pt' in args:
    ins = mine_tle.process_tle()
    ins.main_text()

elif 'rt_pt' in args:
    dct = {
        'file_name': '369',
        'start': 0,
        'debug':1,
        'estart':0,
        'day':0,

    }
    ins = read_txts.prepare_test(dct)
    ins.step2b()


elif 0:
    x = scrub_tle.tle_bibl()
    x.by_length()

elif 'sd_ab' in args:
    ins = scrub_tle.scrub_datacl()
    ins.abnormal([])

elif 'sd_bi' in args:
    scrub_tle.build_tle_idx()

elif "ae_tt" in args:
    add_english.translate_txt()

elif "ae_ae" in args:
    add_english.add_englishcl()

elif "ocr_cr" in args:
    ocr.crop_kind(dir1, dest)



elif 0:
    crop_epub(dir1, dest)
elif 0:
    from_jpg2txt(dir1, file_name, 1, 0, 0)

elif 0:
    filter_txt.temp5()



elif len(args) > 1 and args[1] == 'pg':
    print ('hey')
    str1 = str(args[2])
    assert len(args) == 3
    lst = str1.split("/")
    print (lst)
    str5 = input('hey')
    ins= egy_tools.new_txt({})
    ins.print_german(lst, 2)

elif 'rti' in args:
    ocr.rotate_images()


elif 'p2j' in args:
    from_pdf2jpg(file_name, dest)
elif 'se' in args:
    scan_epub(dir1)
elif 'ahs' in args:
    ad_hoc_scrub_ocr(file_name)

elif 'ta' in args:
    trim_all_images(dir1, dest)

elif 'sk' in args:
    scan_kind(dir1)

elif 'png2p' in args:
    from_png2pdf(dir1, dir2, file_name)

elif 'j2p' in args:
    from_jpg2pdf(dir1, file_name)
elif 'p2t' in args:
    from_pdf2txt(file_name, dest)
elif 'png2t' in args:
    from_jpg2txt(dir1, file_name, 1, 1, 1)

elif 'db' in args:
    double(dir1, dest)

elif 'ch' in args:
    cut_in_half(dir1, dest)

elif 'ah' in args:
    ad_hoc_offset(dir1, dest)