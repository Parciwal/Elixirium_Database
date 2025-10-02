import pathlib
import shutil

def save(name):
    current = pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db') #path of curent file, path of working directory is inconsistent
    new = pathlib.Path(__file__).parent.resolve().joinpath(f'{name}.db')
    shutil.copyfile(current,new)

def load(name):
    current = pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')
    old = pathlib.Path(__file__).parent.resolve().joinpath(f'{name}.db')
    shutil.copyfile(old,current)