from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor
from hashlib import sha3_256 as hasher

primary_color = QColor(176, 224, 230)
white_color = QColor(255, 255, 255)
db_encoding = "cp1251"
spec_symbol = "‡"
spec_s_regex_restrictor = QRegExp("[^{0}]*".format(spec_symbol))
uf_fname = "test.f"
