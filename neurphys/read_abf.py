#!/usr/bin/env python
__author__ = "Dan Galtieri and Chad Estep (chadestep@gmail.com)"

from neo import io
import pandas as pd

def read_abf(filename):
    """
    Imports ABF file using neo io AxonIO, breaks it down by blocks 
    which are then processed into a multidimensional pandas dataframe 
    where each block corresponds to a sweep and columns represent time
    and each recorded channel.

    Parameters
    ----------
    filename: str
        filename WITH '.abf' extension

    Returns
    ------_
    df: DataFrame
        Pandas DataFrame broken down by sweep

    References
    ----------
    [1] https://neo.readthedocs.org/en/latest/index.html
    """

    r = io.AxonIO(filename = filename)
    bl = r.read_block(lazy=False, cascade=True)
    num_channels = len(bl.segments[0].analogsignals)
    channels = ['Primary']
    signals = []
    df_list = []
    sweep_list = []

    for seg_num, seg in enumerate(bl.segments):
        for i in range(num_channels):
            signals.append(bl.segments[seg_num].analogsignals[i])
            if i >= 1:
                channels.append('channel_' + str(i))
        data_dict = dict(zip(channels, signals))
        time = seg.analogsignals[0].times - seg.analogsignals[0].times[0]
        data_dict['time'] = time
        df = pd.DataFrame(data_dict)
        df_list.append(df)
        sweep_list.append('sweep' + str(seg_num + 1).zfill(3))
        df = pd.concat(df_list, keys=sweep_list, names=['sweep'])
    return df