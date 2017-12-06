import csv
from os.path import exists

FILE_NAME = 'KASLnetwork.csv'

def fetch(fn):
    if exists(fn):
        print(fn, "Already exists")
    else:
        fn = str(input("Input file name (Network.csv): "))
        if exists(fn):
            print(fn, "now exists")


def read_data():
    fetch(FILE_NAME)
    with open(FILE_NAME, 'r') as rf:
        return rf.read()


if __name__ == '__main__':
    read_data()