def split_line(line: str, max_symbols: int):
    line += ' '
    new_lines = [[]]
    for i, elem in enumerate(line):
        new_lines[-1].append(elem)
        if elem == ' ':
            try:
                if len(new_lines[-1]) + (line.index(' ', i + 1) - i) > \
                        max_symbols:
                    new_lines[-1] = ''.join(new_lines[-1])
                    new_lines.append([])
            except ValueError:
                new_lines[-1].append(line[i + 1:])
                new_lines[-1] = ''.join(new_lines[-1])
                break
        elif len(new_lines[-1]) + 1 > max_symbols:
            new_lines[-1] = ''.join(new_lines[-1])
            new_lines.append([])
        elif i + 1 == len(line):
            new_lines[-1] = ''.join(new_lines[-1])
    if not any(new_lines[-1]):
        del new_lines[-1]
    return list(filter(lambda x: any(x.strip()), new_lines))
