"""
Generate a dataset of effect applied guitar audio by applying effect of various parameters to dry guitar signals.
"""

import gt_audio_util as util
import dataset_config as dat

data_num = 0  # Serial number of the data
for guitar in dat.guitars.keys():
    for string in dat.strings:
        for fret in dat.frets:
            for fx in dat.fxs.keys():
                guitar_info = util.GuitarInfo(guitar, string, fret)
                guitar_info.add_fx(fx)
                data_num = dat.make_dataset(guitar_info, data_num)
