import turtle
import sys

# Used to block certain modules
import types
from unittest.mock import patch

# Blocked modules
import os
import subprocess
import sys
import shutil
import pathlib
import tempfile
import psutil

blocked_modules = [
    os,
    subprocess,
    sys,
    shutil,
    pathlib,
    tempfile,
    psutil,
]


# def open(*args, **kwargs):
#     raise NotImplementedError("open() is blocked")


# def exec(*args, **kwargs):
#     raise NotImplementedError("exec() is blocked")


# def eval(*args, **kwargs):
    # raise NotImplementedError("eval() is blocked")


"""
#################
!!Don't touch the code below!!
Unless you want to uncomment the 'turtle.done()' line
#################
'turtle.done()' is used to keep the turtle graphics window open
Uncomment the line if you want to see the turtle graphics window

However, when judging your code, we don't want to see the turtle graphics window, 
so we commented it
#################
"""

if __name__ == "__main__":

    # def overwrite_module_fns(module):
    #     def nothing(*args, **kwargs):
    #         pass

    #     for name in dir(module):
    #         if not name.startswith("__"):  # Skip special attributes/methods
    #             attr = getattr(module, name)
    #             if isinstance(attr, types.FunctionType):
    #                 setattr(module, name, nothing)
    #             elif isinstance(attr, types.BuiltinFunctionType):
    #                 patched_func = nothing
    #                 patch(f"{module.__name__}.{name}", new=patched_func).start()

    # # Block students from executing any system code
    # for module in blocked_modules:
    #     overwrite_module_fns(module)

    # raise NotImplementedError("ps_file not updated!")

    # ps_file = sys.argv[1]  # Accept output path as a command-line argument
    # print(f'ps file: {ps_file}')
    
    s = turtle.getscreen()
    ps_file = 'media/result/output.ps'
    pen = turtle.Turtle()

    drawing(pen)

    canvas = s.getcanvas()
    canvas.postscript(file=ps_file)
