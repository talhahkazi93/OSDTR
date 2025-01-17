import ntpath

import pandas as pd
import math
import category_encoders as ce
from enum import Enum, auto
import os
import pathlib
import numpy as np

class Encodings(Enum):
    # Options of encoding defined
    NumberBased = auto()
    Asymmetric = auto()
    ModifiedAsymmetric = auto()
    GenericEncoding = auto()


def num_encoding(ds):
    features = ds.iloc[:, :-1]
    labels = ds.iloc[:, -1:]

    # print(features)
    # print(labels)
    binfeat = convert_dataset(features)
    binclass = convert_dataset(labels)

    # bintable = binclass.append(binfeat)
    bintable = pd.concat([binfeat, binclass], axis=1)

    return bintable


def osdt_enc(ds):
    # modified Asymetric encoding
    de = pd.get_dummies(data=ds, drop_first=True)

    return de

    # print(de.head())


def Asym_enc(ds):
    # modified Asymetric encoding
    # de = pd.get_dummies(data=ds,columns=['a1', 'a2', 'a3', 'a4', 'a5', 'a6'], drop_first=False)
    # de = pd.get_dummies(data=ds,columns=['top-left-square', 'top-middle-square', 'top-right-square', 'middle-left-square',
    #                                      'middle-middle-square', 'middle-right-square', 'bottom-left-square',
    #                                      'bottom-middle-square', 'bottom-right-square'], drop_first=False)

    # classname = ds.pop('Class')
    de = pd.get_dummies(data=ds,columns=[], drop_first=False)
    # print(len(de.columns))
    # de.insert(len(de.columns), 'class', classname)
    return de


def gneric_encoding(ds):
    # # Default binary encoder
    encoder = ce.BinaryEncoder(cols=[], return_df=True)
    data_encoded = encoder.fit_transform(ds)

    return data_encoded

def convert_dataset(features):
    dict = {}
    for column in features:

        ncol_lst = []
        cols = features[column].astype('category')
        cols = cols.cat.codes

        # # UNIQUE FEATURES IN CLOUMN
        unq_val = cols.nunique()
        # # expected columns for feature
        expt_columns = math.ceil(math.log(unq_val, 2))

        l = 1

        if expt_columns > 1:
            if unq_val > 2:
                maintin_list = []
                for i in cols:
                    bits = bin(i)[2:].zfill(expt_columns)
                    bit_lst = [int(d) for d in str(bits)]
                    maintin_list += [bit_lst]
                # print(bin(i)[2:].zfill(expt_columns))

            # dict = dict((el,0) for el in ncol_lst)
            l = len(maintin_list[0])

        for i in range(0, expt_columns):
            ncol_lst.append(str(column) + '_' + str(i + 1))

        for i in range(0, l):
            # varnam = "d" + str(i)
            if expt_columns > 1:
                varnam = [item[i] for item in maintin_list]
            else:
                varnam = [item for item in cols]
            dict[ncol_lst[i]] = varnam

    cnvt_data = pd.DataFrame(dict)
    return cnvt_data


def converter(dataset, selection, idCol):
    de = None
    # First Column Remove
    if idCol == 'last':
        ds = dataset.iloc[:, :-1]
    # Second Column Remove
    elif idCol == 'first':
        ds = dataset.iloc[:, 1:]
    else:
        ds = dataset
    # cols = list(ds.columns)
    # # cols = [cols[-1]] + cols[:-1]
    # ds = ds[['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'class']]
    # ds = ds.astype(str)

    if selection == Encodings.ModifiedAsymmetric:
        de = osdt_enc(ds)
    elif selection == Encodings.Asymmetric:
        de = Asym_enc(ds)
        # de = de[['a1_1', 'a1_2', 'a1_3','a2_1', 'a2_2', 'a2_3', 'a3_1', 'a3_2', 'a4_1','a1_2', 'a4_3', 'a5_1', 'a5_2','a5_3', 'a5_4', 'a6_1', 'a6_2', 'class']]
    elif selection == Encodings.NumberBased:
        de = num_encoding(ds)
    elif selection == Encodings.GenericEncoding:
        de = gneric_encoding(ds)
    return de


def encode(filename='../data/monks-1.test', idCol=None, encodingtype=Encodings.NumberBased):
    file = filename

    # idCol = 'last'
    # idCol = 'first'

    if file.endswith('.csv'):
        ds = pd.DataFrame(pd.read_csv(file, sep=";"))
    else:
        ds = pd.DataFrame(pd.read_csv(file, sep=","))

    # for (index, val) in enumerate(ds['class']):
    #     if val == 'unacc':
    #         ds.loc[index, 'class'] = 0
    #     elif val == 'good':
    #         ds.loc[index, 'class'] = 1
    #     else:
    #         print('wtf is this'+str(index))
    #
    # ds.to_csv("car.csv", index=False, sep=';')
    ds = converter(ds, encodingtype, idCol)

    return ds


def writefile(filename, dataset, encodingtype):
    print(encodingtype)
    if encodingtype == Encodings.ModifiedAsymmetric:
        save_path = '../data/datasets/ModifiedAsymmetric/'
    elif encodingtype == Encodings.Asymmetric:
        save_path = '../data/datasets/Asymmetric_enc/'
    elif encodingtype == Encodings.NumberBased:
        save_path = '../data/datasets/Numberbased_enc/'
    elif encodingtype == Encodings.GenericEncoding:
        save_path = '../data/datasets/Generic_enc/'

    file_name = ntpath.basename(filename)

    #check if path exist and if not creates one
    pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)

    completeName = save_path+file_name
    print(completeName)
    # Export to csv
    dataset.to_csv(completeName+".csv",index=False,sep=';')
    # for col in dataset:
    #     print(col)
    # print(dataset)

def main():
    filename = '../data/datasets/Generic_enc/car.csv'
    encod = Encodings.GenericEncoding
    ds = encode(filename=filename, encodingtype=encod)
    writefile(filename, ds, encod)

if __name__ == "__main__":
    main()
