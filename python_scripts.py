import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))

def extract_value_from_param_file(paramfile, key):
    for line in paramfile.readlines():
        line_key, value = line.split()
        if key == line_key:
            return value
    raise KeyError("Nothing in {} named {}".format(paramfile.name, key))


def param(key):
    try:
        with open("{}/params.txt".format(HERE)) as paramfile:
            return extract_value_from_param_file(paramfile, key)
    except (FileNotFoundError, KeyError):
        with open("{}/default_params.txt".format(HERE)) as paramfile:
            return extract_value_from_param_file(paramfile, key)

def setup(name):
    return """
from setuptools import setup, find_packages

setup(
    name='{}',
    version='0.0.1',
    description='',
    packages=find_packages(exclude=["test"])
)
""".format(name)

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

def get_wat(directory, *args):
    files = list(sorted(glob.glob("{}/*.bat".format(directory))))
    names = [file.split("\\")[-1].split(".bat")[0] for file in files]
    headers = []
    for name, filename in zip(names, files):
        with open(filename) as file:
            header = "    " + file.readline()
        headers.append(header)
    max_name_len = max(len(name) for name in names)
    summary = "".join([
        "{}{}{}".format(name, " " * (max_name_len - len(name) + 1), header)
        for name, header in zip(names, headers)
    ])
    return files, names, summary

def wat(script=None, *args):
    files_g, names_g, summary_g = get_wat(HERE)
    files_p, names_p, summary_p = get_wat(os.path.join(HERE, "personal"))

    if script is not None:
        for name, filename in zip(names_g + names_p, files_g + files_p):
            if name == script:
                with open(filename) as file:
                    return file.read()
        return "No script named {}".format(script)
    else:
        return "Batchit scripts:\n" + summary_g + "\nPersonal files:\n" + summary_p


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
