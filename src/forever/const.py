
import re

# constants for regex formula
# blank string
PT_BLANK = re.compile(u'^\s*$')
# email
PT_EMAIL = re.compile(u'^\w+(\.\w+)*@\w+(\.\w+)+$')

# constants for lenght of char fields
CHAR_SHORT = 8
CHAR_MID = 16
CHAR_LONG = 32
CHAR_XLONG = 64

# count of limited request if a view function need
REQ_FREQUENCY_LIMIT = 10

# random string base
RAND_STR_BASE = '1234567890QWERTYUIOPLKJHGFDSAZXCVBNM'

# oldest age in our site
OLDEST = 128

# threshold amount of access
THETA_NUM = 1000

# err code information
class ErrInfo:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

err = {
    'OK': ErrInfo(0, ''),
    'ERROR': ErrInfo(1, 'has error'),
    'NOT_EXIST': ErrInfo(2, 'not exist'),
}

