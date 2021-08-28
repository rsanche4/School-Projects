from shutil import copyfile
import pathlib
import random

def main():
    src = str(pathlib.Path(__file__).parent.resolve()) + "\MarryMe.py"
    dst = str(pathlib.Path(__file__).parent.resolve()) + "\MarryMe" + str(random.randint(0, 9999999)) + ".py"
    copyfile(src, dst)

if __name__ == '__main__':
    main()
