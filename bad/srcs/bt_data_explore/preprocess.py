import numpy as np
from Pair import Pair
import pandas as pd
#import pygeoip
import csv
import sys
import time
from datetime  import datetime

import matplotlib as mpl
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import seaborn as sns 
sns.set_style("whitegrid")
sns.set(rc={"figure.figsize": (14, 6)})

failed_addr = ['-', '0' ]

def readPairs(file_in, col1, col2):
    data = pd.read_csv(file_in)
    print('Data read')
    d1 = data[col1]
    d2 = data[col2]
    if len(d1) != len(d2):
        raise Exception('Columns must have the same dimensions')
    pairs = set()
    for i in range(len(d1)):
        if i % 100000 == 0:
            print(i)
        p1 = int(d1[i])
        p2 = int(d2[i])
        pair = Pair(p1, p2)
        pairs.add(pair)
    print(len(pairs))
    return pairs

def writeHashesToFile(hashes, file):
    fo = open(file, 'w')
    for key in hashes:
        fo.write(str(key) + ' : ' + str(hashes[key]))
        fo.write('\n')
    fo.close()

def hashData(file_in, file_out, colname):
    data = pd.read_csv(file_in)
    column = data[colname]
    newcol = [None]*len(column)
    cnt_h = 0
    values = {}
    h = -1
    for i in range(len(column)):
        if i % 100000 == 0:
            print(i)
        val = column[i]
        if val in values:
            h = values[val]
        else:
            cnt_h += 1
            h = cnt_h
            values[val] = cnt_h
        newcol[i] = h
    data[colname] = pd.Series(newcol, data.index)
    data.to_csv(file_out, index=False)
    return values

def _init_axes_(figsize=(8,4), nrows=1, ncols=1, sharex=False,
                sharey=False, usetex=False):

    fig, ax = plt.subplots(figsize=figsize, nrows=nrows, ncols=ncols,
                           sharex=sharex, sharey=sharey)
    # plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
    params = {'backend': 'ps',
                'text.latex.preamble': [r"\usepackage{upgreek}"],
                'axes.labelsize': 20,
                'font.size': 20,
                'legend.fontsize': 20,
                'xtick.labelsize': 20,
                'ytick.labelsize': 20,
                # pdf backend params
                'pdf.compression': 9, # 0-9. 0 disables compression
                'pdf.fonttype': 3, # Type 3 (Type3) or Type 42 (TrueType)
                'text.usetex': usetex,
                'figure.figsize': figsize,
                'axes.unicode_minus': True}
    plt.rcParams.update(params)

    # #print len(ax), type(ax)
    # if nrows + ncols > 2 :
    #     for _ax in ax:
    #         _ax.spines['left'].set_position(('outward', 10))
    #         _ax.spines['bottom'].set_position(('outward', 10))
    #         _ax.spines['right'].set_visible(False)
    #         _ax.spines['top'].set_visible(False)
    #         _ax.yaxis.set_ticks_position('left')
    #         _ax.xaxis.set_ticks_position('bottom')
    # else:
    #     ax.spines['left'].set_position(('outward', 10))
    #     ax.spines['bottom'].set_position(('outward', 10))
    #     ax.spines['right'].set_visible(False)
    #     ax.spines['top'].set_visible(False)
    #     ax.yaxis.set_ticks_position('left')
    #     ax.xaxis.set_ticks_position('bottom')

    return fig, ax


def _load_metadata(fin) :
    mdata = pd.read_csv(fin,
                    header = 0,
                    lineterminator="\n",
                    skipinitialspace=True)

    mdata.columns = [str(x).strip().lower() for x in mdata.columns]
    k = mdata['unit_id'].values
    v = mdata [[ 'rannode', 'apnode', 'hubtype', 'headlinespeed' ]].as_matrix()
    mdict = zip(k, v)
    return dict(mdict)

def _load_exclude(fin):
    excl = pd.read_csv(fin,
                    header = 0,
                    lineterminator="\n",
                    skipinitialspace=True)
    return excl

def prepare_rawdata (fin, fout=None, metadata=None, exclude=None,
                     url_to_ip=None, drop_failed=True,
                     drop_reserved=None):

    datefromat='%d-%b-%y %H.%M.%S.%f'
    fromtimestamp = lambda x: datetime.fromtimestamp(int(x) / 1000.)
    totimestamp = lambda x:  datetime.strptime(x[:-3], datefromat)#.strftime("%s")
    #totimestamp = lambda x:  datetime.strptime(x[:-3], datefromat).strftime("%s")
    strip_http = lambda x: str(x).strip('http://')
    
    def expand_date(x):
        #d = datetime.fromtimestamp(float(x))
        return (x.month, x.day, x.hour, x.minute)

    #gethour = lambda x: datetime.fromtimestamp( int(datetime.fromtimestamp(float(x)).hour) )

    tohash = lambda x: hashlib.md5(x).hexdigest()

    X = pd.read_csv(fin,
                    date_parser=totimestamp,
                    parse_dates=["DTIME"],
                    converters={"TARGET": strip_http},
                    lineterminator="\n",
                    skipinitialspace=True)

    # cleanup cols
    X.columns = [str(x).strip().lower() for x in X.columns]
    (nrow, ncol) = X.shape
    
    # if index'ing by time 
    # X.index=X['dtime']
    # X.drop(['dtime'], axis=1, inplace=1)
    
    z = np.asarray( list ( X['dtime'].apply(expand_date) ) )

    X.insert(3, 'month',  z[:,0])
    X.insert(4, 'day',  z[:,1])
    X.insert(5, 'hour',  z[:,2])
    X.insert(6, 'minute',  z[:,3])

    #  exclude 30th april 
    if exclude is not None:
        z = _load_exclude(exclude)

        x = X[ X['month'] == 4 ]
        x = x[ x['day'] == 30 ]
        #print z
        idx = x[x['unit_id'].isin( z['ID'] )].index.values
        X.drop(idx, inplace=True)

    # add the meta data
    (nrow, ncl) = X.shape
    if metadata is not None :
        mdict = _load_metadata( metadata )
        # get the unit properties
        z= X['unit_id'].apply( lambda x: mdict[x] if x in mdict.keys() \
                                else [np.NaN, np.NaN, np.NaN, np.NaN] )

        z = np.asarray( list(z))
        X.insert(ncl, 'ranNode',  z[:,0])
        X.insert(ncl+1, 'apNode',  z[:,1])
        X.insert(ncl+2, 'hubType',  z[:,2])
        X.insert(ncl+3, 'headlineSpeed',  z[:,3])

    # map urls to ip addr.
    if url_to_ip is not None :
        tip =  pd.read_csv(url_to_ip,
                        header = 0,
                        lineterminator="\n",
                        skipinitialspace=True)

        tipdict = dict(zip  (tip ['TARGET'], tip['ADDRESS']) )

        z = X['target'].apply( lambda x: tipdict[x] if x in tipdict.keys() \
                                 else np.NaN )
        X['target'] = z


    if drop_failed == True:
        " drop obviously failed tests "

        idx = X[X['target'].isin( failed_addr )].index.values
        X.drop(idx, inplace=True)
        
        if 'address' in list (X.columns.values ):
            idx = X[X['address'].isin( failed_addr )].index.values
            X.drop(idx, inplace=True)


    if drop_reserved is not None:
        """drop private reserved IP addresses
        https://en.wikipedia.org/wiki/Reserved_IP_addresses

        """
        print 'drop reserved'
        reserved = pd.read_csv(drop_reserved,
                            header = None,
                            lineterminator="\n",
                            skipinitialspace=True)

        idx = X[X['target'].isin( reserved.values.T[0]  )].index.values
        X.drop(idx, inplace=True)

        if 'address' in list (X.columns.values ):
            idx =  X[X['address'].isin( reserved.values.T[0]  )].index.values
            X.drop(idx, inplace=True)


    # reset index in case of drops
    x = np.arange(len(X))
    X.index = x
    # sort by time
    X.sort(['dtime'], ascending=True, inplace=True)

    print 'X=%s  dropped=%s' % (X.shape, nrow-X.shape[0])

    if fout is not None:
        print 'save', fout
        X.to_csv(fout, index=False)

    return X

def convertToHashes(file_in, file_out, values, colname):
    data = pd.read_csv(file_in)
    column = data[colname]
    newcol = [None]*len(column)
    for i in range(len(column)):
        if i % 100000 == 0:
            print(i)
        val = column[i]
        val = val.replace('http://', '')
        if val in values:
            h = values[val]
        else:
            print(val)
        newcol[i] = h
    data[colname] = pd.Series(newcol, data.index)
    data.to_csv(file_out, index=False)

def convertToCountryCodes(file_in, file_out, colname):
    data = pd.read_csv(file_in)
    gi = pygeoip.GeoIP('/home/koki/Desktop/BT/GeoIP.dat')
    column = data[colname]
    newcol = [None]*len(column)
    missing = 0
    for i in range(len(column)):
        if i % 100000 == 0:
            print(i)
        val = column[i]
        code = ''
        try:
            code = gi.country_code_by_addr(val)
        except (OSError, RuntimeError, TypeError, NameError):
            missing += 1
            #print('missing ', missing)
            pass
        newcol[i] = code
    data[colname] = pd.Series(newcol, data.index)
    data.to_csv(file_out, index=False)

if __name__ == "__main__":
    # preprocess raw data 
    data_fin='../data/raw/httpget-H1march2014.csv'
    data_fout='../data/preprocessed/httpget-H1march2014_expanded.csv'
    meta_fin = '../data/metadata/metadata-anon.csv'
    exclude_fin = '../data/metadata/probes_on_a_trial.csv'
    url_to_ip = '../data/metadata/url_to_ip.csv'
    reserved_ips = '../data/metadata/ipaddr_reserved.csv'

    # create enrinched data  
    X = prep.prepare_rawdata(data_fin, 
                         fout=data_fout, 
                         metadata=meta_fin, 
                         exclude=exclude_fin,
                         url_to_ip = url_to_ip,
                         drop_reserved = reserved_ips
                        )
    
