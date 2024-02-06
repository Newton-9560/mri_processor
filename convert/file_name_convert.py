from .utils import *


def get_t2w_path(s, method='replace'):
    if method == 'replace':
        return s.replace('T1w', 'T2w')
    else:
        raise ValueError('Method {} not recognized'.format(method))


def rename_t1w(filename, old, new=''):
    return filename.replace(old, new)
