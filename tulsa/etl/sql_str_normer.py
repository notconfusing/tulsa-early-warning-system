"""
String functions that will help standardize naming for
uploads into PostgreSQL database
"""

import re


def normalize_name_generic(x, remove_leading_nums):
    """
    Lower and strip strings.

    :param x: string to normalize.
    :type x: str.
    :param remove_nums: whether to strip numbers.
    :type revome_nums: bool
    :returns: str -- the normalized string
    """
    out = x.lower()
    out = re.sub(r' to | - |-| ', '_', out)
    out = re.sub(r'[\[\]\(\)\.:\%]', '', out)
    if remove_leading_nums:
        out = re.findall('^\d*(.*)$', out)[0]
    return out


def normalize_colname(x, corrections=None):
    """
    Normalizes column name, also must remove leading nums.

    :param x: string to normalize.
    :type x: str.
    :param corrections: a corrections to apply after normalization
    :type corrections: dict
    :returns: str -- the normalized string
    """
    normed_colname = normalize_name_generic(x, remove_leading_nums=True)
    if corrections:
        return corrections.get(normed_colname, normed_colname)
    else:
        return normed_colname


def normalize_tablename(x):
    """
    Normalizes table names, so removes leading numbers.

    :param x: string to normalize.
    :type x: str.
    :returns: str -- the normalized string
    """
    return normalize_name_generic(x, remove_leading_nums=True)


if __name__ == '__main__':
    testcases = ['CamelCase', '135 to 136', 'work-it', '[5]grades']
    print('testing normalize colnames')
    for case in testcases:
        print(normalize_colname(case))
    print('testing normalize colnames')
    for case in testcases:
        print(normalize_tablename(case))
