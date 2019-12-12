import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))

def croplines(string, width='76'):
    width = int(width)
    lines = string.split("\n")
    croppeds = []
    for line in lines:
        cropped = line[:width]
        if cropped != line:
            cropped += "..."
        croppeds.append(cropped)
    return "\n".join(croppeds)

def cropfile(string, width='76'):
    with open(string) as file:
        return croplines(file.read(), width)

def envlist(*args):
    return croplines(subprocess.check_output("env").decode("utf-8"))


def wat(script=None, *args):
    files = list(sorted(glob.glob("{}/*.bat".format(HERE))))
    names = [file.split("\\")[-1].split(".bat")[0] for file in files]

    if script is not None:
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
    try:
        args = sys.argv[1:]
        if args:
            command, args = args[0], args[1:]
            try:
                func = globals()[command]
            except KeyError:
                print("No command named {}".format(command))
            else:
                result = func(*args)
                print(result)
    except Exception:
        print("Called with argv: ", sys.argv)
        raise
