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
### ModImporter v3.0
### codigo por Daniel G.
#############

## New ModImporter ##

import tkinter as tk


from tkinter import ttk as ttk
import tkinter.filedialog as filed
import tkinter.messagebox as mbox

from data.Style import *
from data.Custom import CustomFont_Label as FontLabel

import os, shutil, sys
import platform as pf

from PIL import ImageTk, Image

import zipfile as zipf

class ModImporter(tk.Frame):
    def __init__(self,parent):
        pass
    def init(self, parent, nameServer = "TestCraft", ver = "6.6.6", edit = False):
        print("Iniciando ModImporter")

        #Configurando la ventana
        self.ventana = tk.Toplevel()
        self.parent = parent
        self.ventana.title(f"ModImporter - {nameServer}")
        self.ventana.wait_visibility()
        self.ventana.grab_set()
        self.ventana.focus_force()

        ## Variables que ModManager recupera
        self.numMods = 0
        self.origenMods = ""

        self.crear = False ## tanto para crear como editar
        self.serverBorrar = False
        self.cancel = False

        ## Variables propias de ModImporter
        self.OS = pf.system()

        self.edit = edit

        self.rutasMods = []
        self.nombresMods = []
        self.numeroDeMods = tk.IntVar(value = 0)
        self.allowDuplicate = tk.BooleanVar(value = False)
        self.nameServer = tk.StringVar(value = nameServer)
        self.oldNameServer = nameServer
        self.version = tk.StringVar(value = ver)

        ## carpeta TEMP depende del sistema
        self.TEMP = ""
        try:
            if(self.OS == "Windows"):
                os.mkdir(f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods")

                self.TEMP = f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods"
            elif(self.OS == "Linux"):
                os.mkdir(f"/home/{os.environ['USER']}/.cache/mods")

                self.TEMP = f"/home/{os.environ['USER']}/.cache/mods"
        except:
            if(self.OS == "Windows"):
                shutil.rmtree(f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods")
                os.mkdir(f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods")

                self.TEMP = f"C:/Users/{os.getlogin()}/Appdata/Local/temp/mods"
            elif(self.OS == "Linux"):
                shutil.rmtree(f"/home/{os.environ['USER']}/.cache/mods")
                os.mkdir(f"/home/{os.environ['USER']}/.cache/mods")

                self.TEMP = f"/home/{os.environ['USER']}/.cache/mods"
        
        print("Llamando a Constructor")
        self.Constructor()

        ## centrar pantalla
        
        x = self.ventana.winfo_width()
        y = self.ventana.winfo_height()
        
        xOffset = int(self.ventana.winfo_screenwidth()/3 - x/2)
        yOffset = int(self.ventana.winfo_screenheight()/4 - y/2)
        self.ventana.geometry(f"+{xOffset}+{yOffset}")
        
        
        #self.ventana.mainloop() #descomentar para debug


    def ActualizarLista(self, busqueda = ""):
        self.lista.delete(0, "end")
        if(self.nombresMods != []):
            for name in self.nombresMods:
                if busqueda == "" or busqueda.upper() in name.upper():
                    self.lista.insert("end", name)
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
                    if(not self.allowDuplicate.get()):
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
 
            self.rutaArchivo = filed.askopenfile(filetypes=[("Archivo Zip", "*.zip")])#,("Archivo Rar","*.rar")
            
            if self.rutaArchivo != None:
                self.rutaArchivo = self.rutaArchivo.name 
            else:
                return
            print("Zip a descomprimir",self.rutaArchivo)
            if self.rutaArchivo != "":
                path = ""
                if(self.OS == "Windows"):
                    path = f"C:/Users/{os.getlogin()}/Appdata/Local/temp"
                elif(self.OS == "Linux"):
                    path = f"/home/{os.environ['USER']}/.cache"
                
                try:
                    os.mkdir(f"{path}/modsZIP/")
                except:
                    shutil.rmtree(f"{path}/modsZIP/")
                    os.mkdir(f"{path}/modsZIP/")

                miZip = zipf.ZipFile(self.rutaArchivo)
                print(f"{path}/modsZIP/")
                miZip.extractall(f"{path}/modsZIP/", pwd=None)
                miZip.close()
                print("OK descompresion")
                
                print("Ok todo\n")

                self.rutaCarpeta = f"{path}/modsZIP/"
                print("DEBUG" ,os.listdir(self.rutaCarpeta))
                ##self.Listar(self.rutaCarpeta, os.listdir(f"{path}/mods/"))
                self.Importar("carpeta", auto = True, ruta= self.rutaCarpeta)
                #shutil.rmtree(f"{path}/modsZIP/")
            
                    
        self.ActualizarLista()
    
    def Exportar(self):
        if (self.numeroDeMods.get() == 0):
            mbox.showwarning("Aviso", "El server no tiene mods que exportar")
            return
        print("Iniciando la exportación de los mods")
        self.rutaArchivo = filed.asksaveasfile(filetypes=[("Archivo Zip", "*.zip")], defaultextension=".zip")
        if self.rutaArchivo == None:
            return
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
        self.nameServer.set(self.nameServer.get().rstrip())

        if(self.nameServer.get() in os.listdir(os.getcwd()) and self.oldNameServer != self.nameServer.get()):
            mbox.showwarning("ERROR", "El nombre del Server ya existe")
            return None
        elif self.nameServer.get().rstrip() == "":
            mbox.showwarning("AVISO", "El nombre no puede estar en blanco")
            return
        self.numMods = len(self.rutasMods)
        if(len(self.rutasMods) == 0):
            r = mbox.askyesno("Cuidado", "No se ha importado ningun mod, Quieres que sea Vanilla?")
            if(not r):
                return
            else:
                self.ventana.destroy()
       
        self.origenMods = self.TEMP
        
        try:
            os.mkdir(self.origenMods)
        except:
            pass
        print(self.rutasMods)
        for mod in self.rutasMods:
            try:
                print("Copiando mod ", mod, " Para guardar")
                shutil.copy(mod, self.origenMods)
            except:
                print("mod ", mod, " ya se encuentra en destino")
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

    def MenuContructor(self):
        self.menuBar = tk.Menu(self.ventana) ## raiz del menu
        self.ventana.config(menu = self.menuBar) ## asociar menu
        

        self.serverMenu = tk.Menu(self.menuBar, tearoff = 0) ## submenu del server

        self.serverMenu.add_command(label = "Guardar", command = lambda: self.Guardar())
        self.serverMenu.add_command(label = "Eliminar todos los mods", command = lambda: self.Borrar(todo = True))
        self.serverMenu.add_command(label = "Eliminar Servidor", command = lambda: self.Borrar(server = True))
        self.serverMenu.add_separator()
        self.serverMenu.add_command(label = "Salir", command = lambda: self.Salir())

        self.importMenu = tk.Menu(self.menuBar, tearoff = 0) ## submenu de importación
        self.importMenu.add_command(label = "Importar de Archivo", command = lambda: self.Importar("file"))
        self.importMenu.add_command(label = "Importar de Carpeta", command = lambda: self.Importar("carpeta"))
        self.importMenu.add_command(label = "Importar de Carpeta Comprimida", command = lambda: self.Importar("zip"))
        self.importMenu.add_separator()
        self.importMenu.add_checkbutton(label = "Autobloquear duplicados", onvalue = 1, offvalue = 0,
                                        variable = self.allowDuplicate)

        self.menuAyuda = tk.Menu(self.menuBar, tearoff = 0)
        self.menuAyuda.add_cascade(label = "Con la tecla de borrar '<---' puedes eliminar el mod seleccionado")

        self.menuBar.add_cascade(label = "Server", menu=self.serverMenu)
        self.menuBar.add_cascade(label = "Importar", menu=self.importMenu)
        self.menuBar.add_command(label = "Exportar", command = lambda: self.Exportar())
        self.menuBar.add_cascade(label = "Ayuda", menu=self.menuAyuda)

        #self.allowDuplicate.trace("w", lambda a,e,i: print(self.allowDuplicate.get()))

    def Constructor(self):
        print("Creando ventana")
        self.frame = ttk.Frame(self.ventana)
        ## crear barra de menu
        self.MenuContructor()

        ##Titulo
        self.titular = tk.Frame(self.frame, relief = tk.RAISED, bd= 10)
        self.titulo = FontLabel(self.titular, text = "ModImporter", size =40)
        self.titulo.grid(row = 1, column = 0, columnspan = 2)
        self.titular.grid(row = 0, column = 0)

        self.frameName = ttk.Frame(self.frame)

        self.textNameServer = FontLabel(self.frameName, text = "Nombre y versión del servidor: ")
        self.textNameServer.grid(row = 0, column = 0)
        self.labelNameServer = ttk.Entry(self.frameName, textvariable = self.nameServer)
        self.labelNameServer.grid(row = 0, column = 1)

        self.labelVerServer = ttk.Entry(self.frameName, textvariable = self.version)
        self.labelVerServer.grid(row = 0, column = 2)

        self.frameName.grid(row = 2, column = 0, columnspan = 2)
        
        self.frameBusqueda = ttk.Frame(self.frame)
        self.lupaImg = Image.open("data/lupa.jpg")
        self.lupa = ImageTk.PhotoImage(self.lupaImg.resize((25, 25), Image.ANTIALIAS))
        self.lupaLabel = ttk.Label(self.frameBusqueda, image = self.lupa)
        self.lupaLabel.grid(row = 3, column = 0)

        self.busqueda = tk.StringVar(value = "")
        self.barraBusqueda = ttk.Entry(self.frameBusqueda, textvariable = self.busqueda, width = 60)
        self.barraBusqueda.grid(row = 3, column = 1,
                                sticky = ("N","S","W","E"))

        self.textNumMods = FontLabel(self.frameBusqueda, text = "Numero de Mods: ")
        self.textNumMods.grid(row = 3, column = 2)
        self.labelNumMods = ttk.Label(self.frameBusqueda, textvariable = self.numeroDeMods)
        self.labelNumMods.grid(row = 3, column = 3)

        self.frameBusqueda.grid(row = 3, column = 0, columnspan = 1, sticky = ("N","S","W","E"))


        self.frameLista = ttk.Frame(self.frame)
        
        self.lista = tk.Listbox(self.frameLista, width = 100,
                             height = 20)
        self.lista.grid(row = 1, column = 0, sticky=("N","S","E","W"))

        self.scroll = ttk.Scrollbar(self.frameLista, orient = tk.VERTICAL,
                                command = self.lista.yview)
        self.scroll.grid(row = 1, column = 1, sticky = ("N","S"))
        
        self.lista["yscrollcommand"] = self.scroll.set
        self.lista.bind("<Delete>", lambda e: self.Borrar())
        self.lista.bind("<BackSpace>", lambda e: self.Borrar())
        
        self.frameLista.grid(row = 4, column = 0, columnspan = 2)

        self.separador = ttk.Separator(self.frame, orient = tk.VERTICAL,
                                       style = "TSeparator")
        
        self.separador.grid(row = 5, column = 0, columnspan = 2,
                            sticky = ("N","S","W","E"), pady = 5)
    

        self.botones = ttk.Frame(self.frame)
        self.guardar = ttk.Button(self.botones, text = "Guardar",
                                  command = lambda:self.Guardar())
        self.guardar.grid(row= 0,column = 0)
        self.salir = ttk.Button(self.botones, text = "Salir",
                                command=lambda:self.Salir())
        self.salir.grid(row = 0, column = 1)
        self.botones.grid(row = 6, column = 0, columnspan = 2, pady = 2)

        self.frame.grid(padx= 10)

        self.nameServer.trace("w", lambda a,e,i: self.ventana.title(f"ModImporter - {self.nameServer.get()}"))
        self.busqueda.trace("w", lambda e,a,u: self.ActualizarLista(busqueda = self.busqueda.get()))

        self.ventana.protocol("WM_DELETE_WINDOW", self.Salir)
        self.ActualizarLista()
        print("Finalizado construcción")
        

if(__name__ == "__main__"):
    v = tk.Tk(baseName = "Test")
    caca = ModImporter(v)
    caca.init(v)
    
    
