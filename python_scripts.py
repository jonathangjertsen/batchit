import glob
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))

def wat(args):
    files = list(sorted(glob.glob("{}/*.bat".format(HERE))))
    names = [file.split("\\")[-1].split(".bat")[0] for file in files]

    if args:
        script = args[0]
        for name, filename in zip(names, files):
            if name == script:
                with open(filename) as file:
                    return file.read()
        return "No script named {}".format(script)

    headers = []
    for name, filename in zip(names, files):
        with open(filename) as file:
            header = file.readline()
        headers.append(header)
    max_name_len = max(len(name) for name in names)
    return "".join([
        "{}{}{}".format(name, " " * (max_name_len - len(name) + 1), header)
        for name, header in zip(names, headers)
    ])

if __name__ == "__main__":
    args = sys.argv[1:]

    if args:
        command, args = args[0], args[1:]
        try:
            func = globals()[command]
        except KeyError:
            print("No command named {}".format(command))
        else:
            result = func(args)
            print(result)
