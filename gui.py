__author__ = 'daniel'
import os
import glob
import tkFileDialog
import platform
from Tkinter import *
import pwd
import TextIO
import tkMessageBox
from pymol import cmd
import rmsd
import shelve


class Ventana():
    def __init__(self, menu):
        self.menuBar = menu
        # parent = app.root
        self.sistm = platform.system()
        self.usr = pwd.getpwuid(os.geteuid()).pw_name
        if self.sistm == 'Linux' or self.sistm == 'Linux2':
            #
            self.dirbin = "/home/" + self.usr + "/.paddot"
            #self.dirbin = "~/.paddot"
            if not os.path.exists(self.dirbin):
                os.makedirs(self.dirbin, 0755)
            else:
                print "Directory already exist"
        elif self.sistm == 'Darwin':
            try:
                os.makedirs('~/Paddot')
            except OSError:
                print "Directory already exist"
        elif self.sistm == 'Windows':
            try:
                os.makedirs('C://PADDOT')
            except OSError:
                print "Directory already exist"
        self.sel = []
        self.parent = Tk()
        self.parent.title("Working directory")
        self.menubar = Menu(self.parent)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Close', command=self.parent.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_separator()
        self.pdb_ops = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='PDBs', menu=self.pdb_ops)
        self.menubar.add_separator()
        self.about = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='about', menu=self.about)
        self.parent.config(menu=self.menubar)
        self.x = 0
        self.ste = IntVar(master=self.parent)
        self.arr = {}
        self.clustr = StringVar(master=self.parent)
        self.method = IntVar(master=self.parent)
        self.frametools = Frame(self.parent, height=200, width=300)
        self.frametools.pack(side=TOP, fill=BOTH, expand=True)
        self.Menu = Menu(self.parent)
        # self.dat = data_m()
        self.pros = TextIO.Pdb()
        self.clcrsmd = rmsd.Rmsd()
        # Second Frame
        self.scndfrm = Frame(self.parent, height=200, width=500)
        self.scndfrm.pack(side=BOTTOM, expand=True, fill="both")

        self.dlgframe = Frame(self.scndfrm, width=300, height=100)
        self.dlgframe.grid(column=0, row=0, sticky="nswe", padx=3, pady=3)
        self.cnv = Canvas(self.dlgframe, width=250, height=150)
        self.cnv.grid(row=0, column=0, sticky='nswe')

        self.hScroll = Scrollbar(self.dlgframe, orient=HORIZONTAL, command=self.cnv.xview)
        self.hScroll.grid(row=1, column=0, sticky='we')
        self.vScroll = Scrollbar(self.dlgframe, orient=VERTICAL, command=self.cnv.yview)
        self.vScroll.grid(row=0, column=1, sticky='ns')
        self.cnv.configure(xscrollcommand=self.hScroll.set, yscrollcommand=self.vScroll.set)
        self.frm = Frame(self.cnv, height=100)
        self.frm.pack(fill="both", expand=True)
        self.frm.pack_propagate(False)
        # # This puts the frame in the canvas's scrollable zone
        self.cnv.create_window(0, 0, window=self.frm, anchor='nw')

        self.openlabel = Label(self.frametools, text="Open Directory")
        self.openlabel.grid(row=1, column=0)
        self.browsebtn = Button(self.frametools, text="Browse",
                                command=lambda: self.loadtemplate(self.cnv, self.frm, self.arr, self.parent), width=10)
        self.browsebtn.grid(row=1, column=1, sticky="sw", padx=2, pady=2)
        self.workdir = Label(self.frametools, text="Save to Working Directory")
        self.workdir.grid(row=3, column=0)
        self.folderbrs = Button(self.frametools, text="Browse", width=10,
                                command=lambda: self.savedir())
        self.folderbrs.grid(row=3, column=1, sticky="sw", padx=2, pady=2)
        self.dlg_all = Checkbutton(self.scndfrm, text="Select all",
                                   command=lambda: self.checkbtn(self.ste, self.dlg_all), onvalue=1, offvalue=0,
                                   variable=self.ste)
        self.dlg_all.grid(row=2, column=0)
        self.clusfrm = Frame(self.scndfrm, width=100, height=120, bd=1, relief=SUNKEN)
        self.clusfrm.grid(row=0, column=2, sticky=N + S + W)
        self.clusfrm.grid_propagate(0)
        # clusfrm.grid_rowconfigure(1, weight= 2, minsize= 6)

        self.clslbl = Label(self.clusfrm, text="Clustering")
        self.clslbl.grid(row=0, column=0)

        self.eucrdbt = Radiobutton(self.clusfrm, text="Euclidian",
                                   variable=self.clustr, value="eucl", command='''lambda :self.clustr.set("eucl")''')
        self.eucrdbt.grid(row=1, column=0, sticky=W + N + S)
        self.eucrdbt.select()

        self.mngrdbt = Radiobutton(self.clusfrm, text="Manhattan", variable=self.clustr,
                                   value="manh", command=lambda: self.clustr.set("manh"))
        self.mngrdbt.grid(row=2, column=0, sticky=W + N + S)
        self.methframe = Frame(self.scndfrm, width=150, height=120, bd=1, relief=SUNKEN)
        self.methframe.grid(row=0, column=1, sticky=N + S)
        self.methframe.grid_propagate(0)

        self.mthlbl = Label(self.methframe, text="Method")
        self.mthlbl.grid(row=0, column=0, sticky=W + N + S)
        self.rmsdrb = Radiobutton(self.methframe, text="RSMD",
                                  variable=self.method, value=1)
        self.rmsdrb.grid(row=1, column=0, sticky=W + S + N)
        self.rmsdrb.select()

        self.avrgrb = Radiobutton(self.methframe, text="Average",
                                  variable=self.method, value=2)
        self.avrgrb.grid(row=2, column=0, sticky=W + N + S)

        self.comprb = Radiobutton(self.methframe, text="Complete",
                                  variable=self.method, value=3)
        self.comprb.grid(row=3, column=0, sticky=W + N + S)

        self.snglrb = Radiobutton(self.methframe, text="Single",
                                  variable=self.method, value=4)
        self.snglrb.grid(row=4, column=0, sticky=W + S + N)

        self.rmsdtxt = Entry(self.methframe, width=5)
        self.rmsdtxt.insert(2, "2.0")
        self.rmsdtxt.grid(row=1, column=1)

        self.cnclbt = Button(self.scndfrm, text="Cancel", width=10,
                             command=lambda: self.parent.destroy())
        self.cnclbt.grid(row=2, column=1, sticky=N + W)

        self.okbtn = Button(self.scndfrm, text="Ok", width=10, command=lambda: self.ok(self.clustr, self.parent))
        self.okbtn.grid(row=2, column=2, sticky=N + W)
        # self.parent.mainloop()

    def loadtemplate(self, cnv, frme, arr, parent):
        self.parent = parent
        self.frm = frme
        self.cnv = cnv
        self.arr = arr
        self.selt = []
        global dirname
        try:
            self.dirname = tkFileDialog.askdirectory()
            os.chdir(self.dirname)

        except:
            pass
        self.cnt = 0
        # Lista donde guardaremos los nombres de los archivos .dlg
        for name in glob.glob('*.dlg'):
            self.arr[name] = IntVar(self.parent)  # Anadimos una clave al diccionario con el valor de 0
        for key in self.arr:
            # self.arr[key] = IntVar()#Cambiamos el valor de 0 por un IntVar para poder trabajar con el en tkinter
            self.r = Checkbutton(self.frm, text=key, onvalue=1, offvalue=0, variable=self.arr[key])
            self.selt.append(self.r)
            self.r.grid(row=self.cnt, column=1, sticky=W)
            self.cnt += 1
        self.frm.update_idletasks()
        # print self.arr
        # # Configure size of canvas's scrollable zone
        self.cnv.configure(scrollregion=(0, 0, self.frm.winfo_width(), self.frm.winfo_height()))
        self.frm.update_idletasks()
        # # Configure size of canvas's scrollable zone
        self.cnv.configure(scrollregion=(0, 0, self.frm.winfo_width(), self.frm.winfo_height()))

    def savedir(self):
        try:
            self.dirct = tkFileDialog.askdirectory()
            self.dirct += "/"

        except:
            self.dirct = self.dirname
            tkMessageBox.showinfo("Advertencia", "El trabajo se guardara en " + str(os.getcwd()))

    def checkbtn(self, ste, chkdlg):
        chkdlg.update_idletasks()

        if ste.get() == 1:
            for key, value in self.arr.items():
                self.arr[key].set(1)
        if ste.get() == 0:
            for key, value in self.arr.items():
                self.estado = value.get()
                self.arr[key].set(0)

    def ok(self, clustr, parent):
        self.m = {}
        # self.plt = grap(parent)
        parent.withdraw()
        # self.scn_root = Tk()
        # self.frme = Frame(self.scn_root,width= 200, height= 200)
        # self.frme.pack(expand= False )
        try:
            self.menuBar.addmenu('PADDOT-plugin', 'Menu de PADDOT')
            self.menuBar.addcascademenu('PADDOT-plugin', 'PDB Files', 'Set some other preferences',
                                        traverseSpec='z', tearoff=0)

        except ValueError:
            tkMessageBox.showerror("Error", "Ya se creo el menu de PADDOT")
            # parent.destroy()
        if clustr.get() == "eucl":
            for key, value in self.arr.items():
                if self.arr[key].get() == 1:
                    self.lista, self.fbereturn = self.pros.iopdb(key, self.dirct, rmsd)
                    self.vct_list = self.pros.lst_num(self.lista)
                    rmsdgrups = self.clcrsmd.cal_rmsd(self.vct_list, self.rmsdtxt.get(), self.lista)
                    self.binmak(key, self.fbereturn, self.vct_list, rmsdgrups)
                    try:
                        self.menuBar.addmenuitem('PDB Files', 'command', label=key.replace(".dlg", ".pdb"),
                                                 command=lambda i=key: self.visual(i))
                    except AttributeError:
                        tkMessageBox.showerror("Error", "The menu is already set")
        elif clustr.get() == "manh":
            tkMessageBox.showinfo("Opcion", "Manhattan")

            # self.fbemin, self.fbemax = self.pros.pross(key, self.dirname)
        parent.destroy()

    def visual(self, uno):
        cmd.reinitialize()
        nombre = uno.replace(".dlg", ".pdb")
        cmd.load(self.dirct + nombre, "COMP")
        cmd.split_states("COMP")

        # cmd.hide("all")
        #cmd.show("sticks", "COMP_0001")
        #cmd.show("sticks", "COMP_0002 COMP_0044 COMP_0063 COMP_0068 COMP_0087")

    def binmak(self, nombre, fbelist, vectores, grupos):
        fn = nombre.replace(".dlg", ".dat")
        archbin = shelve.open(self.dirbin + "/" + fn)
        archbin["fbelist"] = fbelist
        archbin["vectores"] = vectores
        archbin["grupos"] = grupos
        print "bin creado" + fn
        archbin.close()

    def openbn(self, nombre):
        bnopn = shelve.open(self.dirbin + "/" + nombre)
        bnopn.close()
