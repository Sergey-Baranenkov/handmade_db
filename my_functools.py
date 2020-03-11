from initial import *
from os.path import isfile
from collections import defaultdict, OrderedDict


def check_encoding(string, encoding):
    try:
        string.encode(encoding, string)
        return True
    except UnicodeEncodeError:
        return False


def get_indexes(path, field_name):
    path = path + "/" + uf_fname
    if isfile(path):
        i = [0, 0]
        with open(path, "r", encoding=db_encoding) as f:
            for line in f:
                i[1] += len(line)
                line = line.rstrip().split(spec_symbol, maxsplit=1)
                if line[0] == field_name:
                    return tuple([int(idx) for idx in line[1].split()]), tuple(i)
                i[0] = i[1]

    return tuple(), None


def get_hash_path(word):
    h = hasher(word.encode()).hexdigest()
    hp = "/".join([h[i:i + 2] for i in range(0, len(h), 2)])
    return hp


def get_unique_indexes(fields, add_info_needed=False):
    add_info = defaultdict(set)
    unique_indexes = set()

    get_all = True
    for header, value in fields.items():
        if value == "*":
            continue

        hash_path = get_hash_path(value)

        if cur_field_indexes := get_indexes(header + "/" + hash_path, field_name=value):
            if add_info_needed:
                add_info[header] = {(hash_path + "/" + uf_fname, cur_field_indexes)}  # хеш, подходящие индексы

            if get_all:
                unique_indexes = set(cur_field_indexes[0])
            else:
                unique_indexes = unique_indexes & set(cur_field_indexes[0])

            get_all = False
        else:
            unique_indexes = set()
            get_all = False
            break

    if get_all:
        unique_indexes = "*"

    return unique_indexes, add_info


def get_options(table, row):
    fields = OrderedDict()
    for i in range(table.columnCount()):
        item = table.cellWidget(row, i)
        fields[table.horizontalHeaderItem(i).text()] = item.text()
    return fields
