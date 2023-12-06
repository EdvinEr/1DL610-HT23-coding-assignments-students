def extract_author(author_string):
    if ',' in author_string:
        split_names = author_string.split(',', 1)
        names = [split_names[0].strip(), split_names[1].strip()]
        return names
    else:
        names = author_string.rsplit(' ', 1)
        if len(names) == 1:
            return names[0], ''
        return reversed(names)


def extract_authors(author_string):
    result = []
    for author in author_string.split('and'):
        result.append(tuple(extract_author(author.strip())))

    return result