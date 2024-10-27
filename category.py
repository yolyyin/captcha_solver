"""
Ting: helper function for generate the number-category dictionary for training from symbol list
"""


def create_category(symbol_str):
    cat2class = {}
    class2cat= {}
    for i,char in enumerate(symbol_str):
        cat2class[char] = i
        class2cat[i] = char
    return cat2class, class2cat
