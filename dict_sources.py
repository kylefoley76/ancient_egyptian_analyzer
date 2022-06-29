

from general import *
import add_path
from global_hiero import *
from mine_tle import tle_entry, tle_file









class dct_sourcescl:
    def __init__(self):
        self.dct = pi.open_pickle('tle_dct6','hi')
        st = defaultdict(int)
        for x in self.dct.values():
            lst = vgf.strip_n_split(x.main_source, ";")
            for y in lst:
                lst1 = vgf.strip_n_split(y, ",")
                z = lst1[0]
                if reg(r'^(v|V)gl.', z):
                    z = z[4:].strip()


                if z.startswith("Van"):
                    try:
                        idx = z[5:].index(" ")
                        st[z[:idx + 5]] += 1
                    except:
                        pass

                elif " " in z:
                    idx = z.index(" ")
                    st[z[:idx]] += 1
                else:
                    st[z] += 1

        st = sort_dct_val_rev(st)

        return


dct_sourcescl()