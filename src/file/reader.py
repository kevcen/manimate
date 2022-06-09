import tokenize

# unused yet
class Reader:
    """
    TODO: Reader class which can import an existing manim .py file
    """

    def __init__(self, filename):
        with open(filename, "r", encoding="utf-8") as f, open(
            "scene/tokens.txt", "w", encoding="utf-8"
        ) as print_file:
            last_lineno = -1
            last_col = 0
            for (
                type,
                tok_str,
                (sline, scol),
                (eline, ecol),
                ltext,
            ) in tokenize.generate_tokens(f.readline):
                print_file.write(
                    "%10s %-14s %-50r %r \n"
                    % (
                        tokenize.tok_name.get(type, type),
                        "%d.%d-%d.%d" % (sline, scol, eline, ecol),
                        tok_str,
                        ltext,
                    )
                )
                if sline > last_lineno:
                    last_col = 0

                last_col = ecol
                last_lineno = eline
