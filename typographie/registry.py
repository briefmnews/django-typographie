all_filters = []


def register_filter(f):
    all_filters.append(f)
    return f
