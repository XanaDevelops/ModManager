# -*- coding: utf-8 -*-
'''
ModImporter de ModManager 2.x
    Copyright (C) 2020  Daniel García Vázquez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
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

import os, shutil, sys
import platform as pf

import zipfile as zipf

class ModImporter(tk.Frame):
    def __init__(self,parent):
        pass
    def init(self, parent, nameServer = "TESTCRAFT", ver = "666.6.6", edit = False):
        print("Iniciando ModImporter siendo el modo editar",edit)
        
        self.ventana = tk.Toplevel()
        self.ventana.title("Importar Mods")
        #self.ventana.transient(master = parent) ## esto causaba un bug
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
        self.cancel = False
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

        ##variables para geometry
        x = self.ventana.winfo_width()
        y = self.ventana.winfo_height()
        
        xOffset = int(self.ventana.winfo_screenwidth()/4 - x/2)
        yOffset = int(self.ventana.winfo_screenheight()/4.25 - y/2)
        self.ventana.geometry(f"+{xOffset}+{yOffset}")
        #descomentar para debug
        #self.ventana.mainloop()

    def ActualizarLista(self):
        self.lista.delete(0, "end")
        if(self.nombresMods != []):
            self.lista.insert("end", *self.nombresMods)
        self.numeroDeMods.set(len(self.nombresMods))

    def Recursivo(self, ruta):
        for mMod in os.listdir(f"{self.rutaCarpeta}/{ruta}"):
            if(".jar" in mMod or ".meta" in mMod):
                if mMod in self.nombresMods:
                    r = False
                    if(not self.single.get()):
                        r = mbox.askyesno("Mod repetido",
                                                f"Parece ser el mod {mMod} ya esta para importar, desea importarlo igualmente?")
                    if(r):
                        self.rutasMods.append(f"{self.rutaCarpeta}/{ruta}/{mMod}")
                        self.nombresMods.append(mMod)
                else:
                    self.rutasMods.append(f"{self.rutaCarpeta}/{ruta}/{mMod}")
                    self.nombresMods.append(mMod)
            else:
                print("Comprobando carpeta en carpeta recursividad...")
                try:
                    moreDir = os.listdir(f"{self.rutaCarpeta}/{ruta}/{mMod}")
                    self.Recursivo(f"/{ruta}/{mMod}")
                except:
                    print("No es una carpeta RECURSIVA o ", f"ERROR {sys.exc_info()[0]}", sys.exc_info()[1])


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
                    #print(f"y {y}") ## debug
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

        print("MODSSS   ", mods) ##debug
        moreMods = [] #Mas mods que se pueden encontrar en subcarpetas
        
       
        for x in mods:
            if(not ".jar" in x and not ".meta" in x):
                print("archivo ",x," que no es mod or metadata encontrado, comprobando si es un directorio")
                try:
                    dire = os.listdir(f"{self.rutaCarpeta}/{x}")
                    if not dire == []:
                        moreMods.append(x)
                        self.Recursivo(x)
                        

                except:
                    print("No es una carpeta o ", f"ERROR {sys.exc_info()[0]}", sys.exc_info()[1])
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
        
        #print(self.rutasMods)
        print("Nombres de los mods actualmente:")
        for mod in self.nombresMods:
            print(mod)
        #print(self.nombresMods)
        self.numeroDeMods.set(len(self.nombresMods))
       
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

        self.botonExport = ttk.Button(self.botonesImport, text="Exportar mods",
                                      command=lambda:self.Exportar())
        self.botonExport.grid(row =3, column=0)
        
        self.botonesImport.grid(row= 1, column = 0, sticky=["W","E"])
        self.botonesEdit = ttk.Frame(self.frame)
        if(self.edit):
            self.botonBorrarServer = ttk.Button(self.botonesEdit, text = "Borrar Server",
                                                command = lambda: self.Borrar(server = True))
            self.botonBorrarServer.grid(row = 2, column = 0, sticky=["W","E"])
            
        
        self.botonBorrar = ttk.Button(self.botonesEdit, text = "Desmarcar mod seleccionado",
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

        self.chkButtonDoble = ttk.Checkbutton(self.frameNumMods,
                                              text =  "Evitar Duplicados",
                                              variable = self.single)
        self.chkButtonDoble.grid(row = 0, column = 2, sticky=["W","E"])

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
        self.salir = ttk.Button(self.botones, text = "Salir sin guardar",
                                command=lambda:self.Salir())
        self.salir.grid(row = 0, column = 1)
        self.botones.grid(row = 4, column = 0, columnspan = 2, pady = 2)
        self.frame.pack()

    def Importar(self,modo, auto = False, ruta = ""):
        ## Leera la entrada y lo pasará una lista con las rutas absolutas
        if modo == "carpeta":
            if(auto):
                self.rutaCarpeta = ruta
            else:
                self.rutaCarpeta = filed.askdirectory()
            print("Carpeta a importar",self.rutaCarpeta)
            if(self.rutaCarpeta != ""):
                mods = os.listdir(self.rutaCarpeta)
                self.Listar(self.rutaCarpeta, mods)  
                
                #mbox.showerror(f"ERROR {sys.exc_info()[0].__name__}",sys.exc_info()[1])
                    
                 
                    
        if modo == "file":
            self.archivosRaw = filed.askopenfiles(filetypes=[("Minecraft Mod", "*.jar")])
            if(self.archivosRaw != ""):
                self.rutasArchivos = [x.name for x in self.archivosRaw]
                print("Archivos a importar:")
                for mod in self.rutasArchivos:
                    print(mod)
                print()
                
                self.rutaCarpeta = ""
                self.Listar(self.rutasArchivos)

        if modo == "zip":
 
            self.rutaArchivo = filed.askopenfile(filetypes=[("Archivo Zip", "*.zip")]).name #,("Archivo Rar","*.rar")
            print("Zip a descomprimir",self.rutaArchivo)
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
                
                print("Ok todo\n")

                self.rutaCarpeta = f"{path}/mods/"
                print("DEBUG" ,os.listdir(self.rutaCarpeta))
                self.Listar(self.rutaCarpeta, os.listdir(f"{path}/mods/"))
            
                    
        self.ActualizarLista()
    
    def Exportar(self):
        if (self.numeroDeMods.get() == 0):
            mbox.showwarning("Aviso", "El server no tiene mods que exportar")
            return
        print("Iniciando la exportación de los mods")
        self.rutaArchivo = filed.asksaveasfile(filetypes=[("Archivo Zip", "*.zip")], defaultextension=".zip")
        print("ruta al archivo es" + self.rutaArchivo.name)
        with zipf.ZipFile(self.rutaArchivo.name, mode ="w") as modzip:
            for mod in self.rutasMods:
                print("exportando mod ", mod)
                modzip.write(mod, self.nombresMods[self.rutasMods.index(mod)])
            modzip.close()
            del modzip

        print("Mods exportados")
        mbox.showinfo("ÉXITO", "Mods exportados\nSi te aparece un error al abrir el zip, cierra ModManager y vuelvelo a intentar")


    def Guardar(self):
        ##devolverá los valores adecuados, la ruta de la carpeta si no es .minecraft/mods
        ##                                  lo pasará a %temp%
        ######
        print("Guardando Servidor")
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


    def Borrar(self, todo = False, server = False):
        
        if(server):
            r = mbox.askyesno("Borrar Server?", "Estas seguro?, no hay vuelta atras")
            if(r):
                self.serverBorrar = True
                print("Procediendo a borrar el servidor")
                self.ventana.destroy()
        elif(todo):
            self.rutasMods = []
            self.nombresMods = []

            self.ActualizarLista()
        else:
            if(self.lista.curselection() == ()):
                mbox.showwarning("Desmarcar", "Selecciona un Mod")
                return
            print("Borrando de la importacion el mod seleccionado")
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
            r = mbox.askokcancel("Salir?", "No se creará ningún server")
            if(r):
                self.cancel = True
                self.ventana.destroy()
                
        
        
if(__name__ == "__main__"):
    v = tk.Tk()
    caca = ModImporter(v)
    caca.init(v)
