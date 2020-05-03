# -*- coding: utf-8 -*-

################
### ManagerMods para MC todas versiones v1.0.0
### codigo por Daniel G.
#############

## ModImporter ##

import tkinter as tk


from tkinter import ttk as ttk
import tkinter.filedialog as filed
import tkinter.messagebox as mbox

from data.Style import *
from data.Custom import CustomFont_Label as FontLabel

import os, shutil
import platform as pf

import zipfile as zipf

class ModImporter(tk.Frame):
    def __init__(self,parent):
        pass
    def init(self, parent, nameServer = "TESTCRAFT", ver = "666.6.6", edit = False):
        self.ventana = tk.Toplevel()
        self.ventana.title("Importar Mods")
        self.ventana.transient(master = parent)
        self.ventana.grab_set()
        ## variables necesarias
        self.edit = edit
        self.rutasMods = []
        self.nombresMods = []
        self.numeroDeMods = tk.IntVar(value = 0)

        self.single = tk.BooleanVar(self.ventana, value = True)

        self.crear = False

        self.nameServer = tk.StringVar(value= nameServer)
        self.oldName = nameServer
        self.version = tk.StringVar(value=ver)

        self.serverBorrar = False
        ## se comprueba el SO
        self.OS = pf.system()
        ##se crea aqui la carpeta temporal...

        try:
            if(self.OS == "Windows"):
                os.mkdir(f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods")
            elif(self.OS == "Linux"):
                os.mkdir(f"/home/{os.environ['USER']}/.cache/mods")
        except:
            if(self.OS == "Windows"):
                shutil.rmtree(f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods")
                os.mkdir(f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods")
            elif(self.OS == "Linux"):
                shutil.rmtree(f"/home/{os.environ['USER']}/.cache/mods")
                os.mkdir(f"/home/{os.environ['USER']}/.cache/mods")

        ## ahora se crea la pantalla
        #self.frame = self.Constructor()
        self.Constructor()
        #comentar para debug
        #self.ventana.mainloop()

    def ActualizarLista(self):
        self.lista.delete(0, "end")
        if(self.nombresMods != []):
            self.lista.insert("end", *self.nombresMods)
        self.numeroDeMods.set(len(self.nombresMods))
    def Listar(self, rutas, nombres = []):
        if nombres != []:
            mods = nombres[::]
            print("nombres dados")
        else:
            print("nombres no dados")
            mods = []
            for x in rutas:
                name = ""
                print(f"x {x}")
                for y in list(x[::-1]):
                    #print(f"y {y}")
                    if(y != "/"):
                       name+=y
                    else:
                        break
                mods.append(name[::-1])
            print(f"Mods: {mods}")
        if self.rutaCarpeta == "":
            name = mods[0]
            ruta = rutas[0]
            n = len(name)

            self.rutaCarpeta = ruta[:len(ruta)-n-1]
            print(self.rutaCarpeta)
        for x in mods:
            if(not ".jar" in x):
                print("archivo que no es mod encontrado")
            else:
                if x in self.nombresMods:
                    r = False
                    if(not self.single.get()):
                        r = mbox.askyesno("Mod repetido",
                                      f"Parece ser el mod {x} ya esta para importar, desea importarlo igualmente?")
                    if(r):
                        self.rutasMods.append(f"{self.rutaCarpeta}/{x}")
                        self.nombresMods.append(x)
                else:
                    self.rutasMods.append(f"{self.rutaCarpeta}/{x}")
                    self.nombresMods.append(x)
        
        print(self.rutasMods)
        print(self.nombresMods)
        self.numeroDeMods.set(len(self.nombresMods))
        
    def Importar(self,modo, auto = False, ruta = ""):
        ## Leera la entrada y lo pasará una lista con las rutas absolutas
        if modo == "carpeta":
            if(auto):
                self.rutaCarpeta = ruta
            else:
                self.rutaCarpeta = filed.askdirectory()
            print(self.rutaCarpeta)
            if(self.rutaCarpeta != ""):
                mods = os.listdir(self.rutaCarpeta)
                
                self.Listar(self.rutaCarpeta, mods)   
                    
        if modo == "file":
            self.archivosRaw = filed.askopenfiles(filetypes=[("Minecraft Mod", "*.jar")])
            if(self.archivosRaw != ""):
                self.rutasArchivos = [x.name for x in self.archivosRaw]
                print(self.rutasArchivos)
                
                self.rutaCarpeta = ""
                self.Listar(self.rutasArchivos)

        if modo == "zip":
 
            self.rutaArchivo = filed.askopenfile(filetypes=[("Archivo Zip", "*.zip"),
                                                          ("Archivo Rar","*.rar")]).name
            print(self.rutaArchivo)
            if self.rutaArchivo != "":
                path = ""
                if(self.OS == "Windows"):
                    path = f"C:/Users/{os.getlogin()}/Appdata/Local/temp"
                elif(self.OS == "Linux"):
                    path = f"/home/{os.environ['USER']}/.cache"
                
                try:
                    os.mkdir(f"{path}/mods/")
                except:
                    pass
                miZip = zipf.ZipFile(self.rutaArchivo)
                print(f"{path}/mods/")
                miZip.extractall(f"{path}/mods/", pwd=None)
                miZip.close()
                print("OK descompresion")
                
                print("Ok todo")

                self.rutaCarpeta = f"{path}/mods/"
                self.Listar(self.rutaCarpeta, os.listdir(f"{path}/mods/"))
            
                    
        self.ActualizarLista()
            
    def Guardar(self):
        ##devolverá los valores adecuados, la ruta de la carpeta si no es .minecraft/mods
        ##                                  lo pasará a %temp%
        ######
        if(self.nameServer.get() in os.listdir(os.getcwd()) and self.oldName != self.nameServer.get()):
            mbox.showwarning("ERROR", "El nombre del Server ya existe")
            return None
        self.numMods = len(self.rutasMods)
        if(len(self.rutasMods) == 0):
            r = mbox.askyesno("Cuidado", "No se ha importado ningun mod, Quieres que sea Vanilla?")
            if(not r):
                return
            else:
                self.ventana.destroy()
        if(self.OS == "Windows"):
            self.origenMods = f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods"
        elif(self.OS == "Linux"):
            self.origenMods = f"/home/{os.environ['USER']}/.cache/mods"
        
        try:
            os.mkdir(self.origenMods)
        except:
            pass
        
        for mod in self.rutasMods:
            if self.origenMods not in mod:
                shutil.copy(mod, self.origenMods)
        self.crear = True
        self.ventana.destroy()
    def Constructor(self):
        self.frame = ttk.Frame(self.ventana)
        
        self.titular = ttk.Frame(self.frame)
        self.titulo = FontLabel(self.titular, text = "Importador de mods", size = 20)
        self.titulo.grid(row = 0, column = 0)
        if(self.edit):
            self.subtitulo = ttk.Frame(self.titular)

            self.nombreF = FontLabel(self.subtitulo,
                                     text = "Server: ")
            self.nombreF.grid(row = 0, column = 0)

            self.nombreE = ttk.Entry(self.subtitulo, textvariable = self.nameServer)
            self.nombreE.grid(row = 0, column = 1)

            self.versionF = FontLabel(self.subtitulo, text = "Version")
            self.versionF.grid(row = 0, column = 2)

            self.versionE = ttk.Entry(self.subtitulo, textvariable = self.version)
            self.versionE.grid(row = 0, column = 3)
        else:
            self.subtitulo = FontLabel(self.titular,
                                       text = f"Server: {self.nameServer.get()}   ver: {self.version.get()}")
        self.subtitulo.grid(row = 1, column = 0)
        self.titular.grid(row = 0, column = 0, columnspan = 2)
        ## Parte botones
    
        self.botonesImport = ttk.Frame(self.frame)

        self.botonCarpeta = ttk.Button(self.botonesImport, text = "Importar de Carpeta",
                                       command=lambda:self.Importar("carpeta"))
        self.botonCarpeta.grid(row= 0, column = 0, sticky=["W","E"])
        self.botonArchivo = ttk.Button(self.botonesImport, text = "Importar de Archivo",
                                       command=lambda:self.Importar("file"))
        self.botonArchivo.grid(row= 1, column = 0, sticky=["W","E"])
        self.botonZip = ttk.Button(self.botonesImport, text = "Importar de archivo comprimido",
                                       command=lambda:self.Importar("zip"))
        self.botonZip.grid(row= 2, column = 0)

        self.chkButtonDoble = ttk.Checkbutton(self.botonesImport,
                                              text =  "Evitar Duplicados",
                                              variable = self.single)
        self.chkButtonDoble.grid(row = 3, column = 0, sticky=["W","E"])
        
        self.botonesImport.grid(row= 1, column = 0, sticky=["W","E"])
        self.botonesEdit = ttk.Frame(self.frame)
        if(self.edit):
            self.botonBorrarServer = ttk.Button(self.botonesEdit, text = "Borrar Server",
                                                command = lambda: self.Borrar(server = True))
            self.botonBorrarServer.grid(row = 2, column = 0, sticky=["W","E"])
            
        
        self.botonBorrar = ttk.Button(self.botonesEdit, text = "Desmarcar Seleccionado",
                                      command=lambda:self.Borrar())
        self.botonBorrar.grid(row = 0, column = 0, sticky=["W","E"])

        self.botonBorrarAll = ttk.Button(self.botonesEdit, text = "Desmarcar todos los mods",
                                      command=lambda:self.Borrar(todo=True))
        self.botonBorrarAll.grid(row = 1, column = 0, sticky=["W","E"])
    
        self.botonesEdit.grid(row = 2, column = 0, sticky=["W","E"])

        

        ## aqui verás los mods que se van a incluir, si hay
        self.frameLista = ttk.Frame(self.frame)
        self.frameNumMods = ttk.Frame(self.frameLista)
        
        self.numeroDeModsL = FontLabel(self.frameNumMods, text = "Numero de mods:")
        self.numeroDeModsL.grid(row = 0, column = 0)
        self.numeroDeModsV = ttk.Label(self.frameNumMods,
                                       textvariable = self.numeroDeMods)
        self.numeroDeModsV.grid(row = 0, column = 1)

        self.frameNumMods.grid(row = 0, column = 0)
        
        self.lista = tk.Listbox(self.frameLista, width = 50,
                             height = 10)
        self.lista.grid(row = 1, column = 0, sticky=("N","S","E","W"))

        self.scroll = ttk.Scrollbar(self.frameLista, orient = tk.VERTICAL,
                                command = self.lista.yview)
        self.scroll.grid(row = 1, column = 1, sticky = ("N","S"))
        
        self.lista["yscrollcommand"] = self.scroll.set
        self.lista.bind("<Delete>", lambda e: self.Borrar())
        
        self.frameLista.grid(row = 1, column = 1,
                             rowspan = 2)

        self.separador = ttk.Separator(self.frame, orient = tk.VERTICAL,
                                       style = "TSeparator")
        
        self.separador.grid(row = 3, column = 0, columnspan = 2,
                            sticky = ("N","S","W","E"), pady = 5)
    

        self.botones = ttk.Frame(self.frame)
        self.guardar = ttk.Button(self.botones, text = "Guardar",
                                  command = lambda:self.Guardar())
        self.guardar.grid(row= 0,column = 0)
        self.salir = ttk.Button(self.botones, text = "Salir sin importar",
                                command=lambda:self.Salir())
        self.salir.grid(row = 0, column = 1)
        self.botones.grid(row = 4, column = 0, columnspan = 2, pady = 2)
        self.frame.pack()

    def Borrar(self, todo = False, server = False):
        
        if(server):
            r = mbox.askyesno("Borrar Server?", "Estas seguro?, no hay vuelta atras")
            if(r):
                self.serverBorrar = True
                self.ventana.destroy()
        elif(todo):
            self.rutasMods = []
            self.nombresMods = []

            self.ActualizarLista()
        else:
            if(self.lista.curselection() == ()):
                mbox.showwarning("Desmarcar", "Selecciona un Mod")
                return
            index = self.lista.curselection()[0]
            name = self.lista.get(index)
            indexL = self.nombresMods.index(name)

            self.rutasMods.pop(indexL)
            self.nombresMods.pop(indexL)

            self.ActualizarLista()
            
            
    def Salir(self):
        if(self.edit):
            r = mbox.askokcancel("Salir?", "No se Guardarán los cambios")
            if(r):
                self.ventana.destroy()
        else:
            r = mbox.askokcancel("Salir?", "El server será Vanilla, Ok?")
            if(r):
                self.ventana.destroy()
        
        
if(__name__ == "__main__"):
    v = tk.Tk()
    caca = ModImporter(v)
    caca.init(v)