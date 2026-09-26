import pandas as pd


def generalize(ser, match_name, default=None, regex=False, case=False):
    """Search a series for text matches.
    Based on code from https://www.metasnake.com/blog/pydata-assign.html

    ser: pandas series to search
    match_name: tuple containing text to search for and text to use for normalization
    default: If no match, use this to provide a default value, otherwise use the original text
    regex: Boolean to indicate if match_name contains a  regular expression
    case: Case sensitive search

    Returns a pandas series with the matched value

    """
    seen = None
    is_cat = pd.CategoricalDtype.is_dtype(ser)
    for match, name in match_name:
        mask = ser.str.contains(match, case=case, regex=regex)
        if seen is None:
            seen = mask
        else:
            seen |= mask

        if is_cat and name not in ser.cat.categories:
            ser = ser.cat.add_categories(name)
