def sort(int_list):
    # if not int_list:
    #     return []
    #
    # s = sorted(set(int_list))
    # return s + [s[-1]] * (len(int_list) - len(s))

    if not int_list:
        raise Exception("empty list")

    return sorted(int_list)
