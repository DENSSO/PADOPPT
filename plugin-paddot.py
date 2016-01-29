__author__ = 'daniel'
from Tkinter import *
import glob
import tkMessageBox
import matplotlib as mpl
from math import sqrt
from pymol import cmd
import pwd
import gui

mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def __init__(self):
    self.menuBar.addmenuitem('Plugin', 'command', 'PADDOT-plugin', label='PADDOT-plugin',
                             command=lambda: gui.Ventana(self.menuBar))




