from csv import DictReader

from fetchcsv import read_data


def parse_data():
    txt = read_data()
    lines = txt.splitlines()
    return list(DictReader(lines))

def getsevername():
    newrows = []
    o_rows = parse_data()
    for row in o_rows:
        if row['VIRTUAL'] == 'N':
            rowip = row['IP_ADDRESS']
            newrows.append(rowip)
    return newrows

if __name__ == "__main__":
    getsevername()
