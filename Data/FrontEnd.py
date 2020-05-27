# -*- coding: utf-8 -*-
'''
FrontEnd de ModManager 2.x
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
### ManagerMods para MC todas versiones v2.0.0
### codigo por Daniel G.
#############

import os, sys
import platform as pf

try:
    import tkinter as tk

    from tkinter import ttk as ttk
    import tkinter.filedialog as filed
    import tkinter.messagebox as mbox
except:
    print("No se ha podido importar tkinter")
    sys.exit()

from BackEnd import *
from ModImporter import *
from data.Style import *
from data.Custom import CustomFont_Label as FontLabel
from data.Custom import CustomFont_Message as FontMessage

import argparse as arg
import subprocess as subp

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
    
class FrontEnd(tk.Frame):
    def Debug(self):
        if self.OS == "Windows":
            if "FrontEnd.py" in os.listdir(os.getcwd()):
                subp.Popen("cmd /C python FrontEnd.py".split(" "))
                sys.exit()
            else:
                
                subp.Popen("cmd /C ModManager.exe | more".split(" "))
                sys.exit()
            
   
    def __init__(self, parent):
        print("###### BIENVENIDO A MODMANGER ######")

        
        sys.stdout = Unbuffered(sys.stdout)
        self.verApp = "2.2.0"
        self.parent = parent
        self.parent.title("ModManager")
        self.OS = pf.system()
        print(f"Version: {self.verApp} corriendo en {self.OS}")
        ## argumentos de comando
        parser = arg.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="Mostrar información de depuración",
                            action="store_true")
        
        args = parser.parse_args()
        if args.verbose:
            self.Debug()
     
        ## variables para centrar la ventana, no tienen self porque realmente
        ## no hace falta
        xOffset = int(self.parent.winfo_screenwidth()/2 - 400/2)
        yOffset = int(self.parent.winfo_screenheight()/2.5 - 320/2)
        self.parent.geometry(f"400x320+{xOffset}+{yOffset}")
        
        
        self.parent.iconphoto(True, tk.PhotoImage(file="data/icono.png"))
        
        self.sql = BackEnd()
        self.modImporter = ModImporter(self.parent)
        self.style = Styles()
        self.font = "data/Minecraftia-Regular.ttf"

        self.pantallas = [tk.Frame(self.parent), ## inicio
                          tk.Frame(self.parent), ## crear
                          tk.Frame(self.parent)] ## navegar servers
        
        self.firmador = ttk.Frame(self.parent)
        self.firma = tk.Label(self.firmador, text= f"Daniel Garcia Vazquez 2020© v{self.verApp}")
        self.firma.grid(row = 0, column = 0)
        self.acercaDeB = ttk.Button(self.firmador, text = "Acerca de",
                                    command = lambda:self.AcercaDe())
        self.acercaDeB.grid(row = 0, column = 1)
        self.firmador.pack(side=tk.BOTTOM)
        
        self.CargadorPantalla(0)

    def AcercaDe(self):
        print("Abriendo AcercaDe")
        
        self.about = tk.Toplevel(self.parent)
        
        self.about.title("Acerca de ModManager")

        self.titular = tk.Frame(self.about, relief = tk.RAISED, bd=15)
        self.titulo = FontLabel(self.titular, text = "ModManager", size=40)
        self.titulo.grid(row = 0, column = 0)
        self.titular.grid(row = 0, column = 0)
        
        self.Separar(1,self.about)
        self.descripcion = ttk.Frame(self.about)

        self.text1 = FontLabel(self.descripcion, text="Manager de mods de Minecraft")
        self.text1.pack()
        self.text2 = FontLabel(self.descripcion, text="Deja el trabajo sucio")
        self.text2.pack()
        self.text3 = FontLabel(self.descripcion, text="a este programa")
        self.text3.pack()
        self.descripcion.grid(row = 2, column = 0)

        self.Separar(3,self.about)
        self.sistemaF = ttk.Frame(self.about)
        self.sistema = FontLabel(self.sistemaF, text=f"Version {self.verApp} {self.OS}",
                                 size = 11)
        self.sistema.grid(row= 4, column = 0)
        self.debug = ttk.Button(self.sistemaF, text="Activar debug",
                                command=lambda:self.Debug())
        self.debug.grid(row = 4, column = 1)
        self.sistemaF.grid(row = 4, column = 0)
        self.nombre = FontLabel(self.about, text="Daniel García Vázquez 2020© GLP3",
                                size = 11)
        self.nombre.grid(row = 5, column = 0)
        
    def CargadorPantalla(self, nPantalla):
        
        for p in range(len(self.pantallas)):
            self.pantallas[p].destroy()
        self.pantallas = [tk.Frame(self.parent), ## inicio
                          tk.Frame(self.parent), ## crear
                          tk.Frame(self.parent)] ## navegar servers
        self.pantalla = self.pantallas[nPantalla]
        if(nPantalla == 0):
            self.P_Inicial()
        elif(nPantalla == 1):
            self.P_Crear()
        elif(nPantalla == 2):
            self.P_Leer()
            
        
        
        self.pantalla.pack()
        
        self.pantallas[nPantalla] = self.pantalla
    def Separar(self, fila, pant = None):
        if not pant:
            pant = self.pantalla
        self.separador = ttk.Separator(pant, orient = tk.VERTICAL,
                                       style = "TSeparator")
        
        self.separador.grid(row = fila, column = 0, sticky = ("N","S","W","E"), pady = 5)
    def UpdateData(self):
        print("Actualizando datos de servidor")
        self.listaServers = self.sql.VerServers()
        print("Servidores actualmente registrados:")
        for server in self.listaServers:
            print("    ",server)

        for server in self.listaServers:
            if server[4] == 1:
                self.actualServer = server
                print("El server activo es",server[0])
                break
        if len(self.listaServers) == 1 and self.listaServers[0][0] == "Vanilla":
            self.soloVanilla = True
            print("Solo se encuentra el servidor Vanilla")
        else:
            self.soloVanilla = False
        
    def P_Inicial(self):
        self.pantalla = self.pantallas[0]

        self.titular = tk.Frame(self.pantalla, relief = tk.RAISED, bd=10)

        
        self.titulo = FontLabel(self.titular, text = "ModManager",
                                size = 35) 
        self.titulo.grid(row = 0, column = 0)
        self.subTitulo = FontLabel(self.titular, text = "Preocupate solo de jugar",
                                   size = 18)
        self.subTitulo.grid(row = 1, column = 0)

        self.titular.grid(row = 0, column = 0)

        ##
        self.UpdateData()
        #####
        if(self.soloVanilla):
            fff  = mbox.showwarning("Sin Servers", "Es necesario que crees uno")
        
        self.infoS = tk.Frame(self.pantalla, relief = tk.RIDGE, bd=5)

        self.tServer = FontLabel(self.infoS, text = "Servidor Activo: ",size = 16)
        self.tServer.grid(row = 0, column = 0)
        self.nServer = FontLabel(self.infoS, text = self.actualServer[0],size = 16)
        self.nServer.grid(row = 0, column = 1)

        

        self.tVer = FontLabel(self.infoS, text = "Versión Mc: ",size = 16)
        self.tVer.grid(row = 1, column = 0)
        self.vVar = tk.StringVar(value="")
        self.vVar.set(self.actualServer[1])
        
        self.nVer = FontLabel(self.infoS, text = self.vVar.get(),size = 16)
        self.nVer.grid(row = 1, column = 1)

        self.tMod = FontLabel(self.infoS, text = "Mods utilizados: ",size = 16)
        self.tMod.grid(row = 2, column = 0)
        self.vMods = tk.StringVar(value="")
        self.vMods.set(self.actualServer[2])

        self.nMod = FontLabel(self.infoS, text = self.vMods.get(),size = 16)
        self.nMod.grid(row = 2, column = 1)

        
        self.infoS.grid(row = 1, column = 0)

        self.Separar(2)
        
        self.botones = tk.Frame(self.pantalla)

        self.bCrear = ttk.Button(self.botones, text = "Crear",
                             command = lambda: self.CargadorPantalla(1))
        self.bCrear.grid(row = 0, column = 0)
        self.bListar = ttk.Button(self.botones, text = "Ver servidores",
                             command = lambda: self.CargadorPantalla(2))
        self.bListar.grid(row = 0, column = 1)

        self.bSalir = ttk.Button(self.botones, text = "Salir",
                             command = lambda: self.parent.destroy())
        self.bSalir.grid(row = 1, column = 0, columnspan = 2)

        self.botones.grid(row = 3, column = 0)


    def Mods(self):
        ## ahora los maneja ModImporter
        
        print("exitz")
        
		
    def Crear(self):
        print("Creando servidor\n")
        
        nombre = self.vServer.get()
        ver = self.vVer.get()
        print("Servidor:", nombre, "Version", ver)
        for server in self.listaServers:
            
            if(nombre.upper() == server[0].upper()):
                mbox.showwarning("ERROR", "Ya existe un server con ese nombre")
                print("Ya existe ese servidor")
                return

        self.barraDeCarga.start(25)
        
        
        r = mbox.askyesno("Mods?", "Desea incluir Mods?")
        if(r):
            try: ## handle errors
                self.modImporter.init(self.parent, nombre, ver)
            except:
                mbox.showerror(f"ERROR {sys.exc_info()[0].__name__}",sys.exc_info()[1])
                self.barraDeCarga.stop()
                self.modImporter.ventana.destroy()
                return
            self.parent.wait_window(self.modImporter.ventana)
            
            if(self.modImporter.crear):
                numMods, origenMods = self.modImporter.numMods,self.modImporter.origenMods
                mbox.showinfo("Mods Añadidos", "Los mods han sido añadidos")     
                print("exxitzz")
                self.sql.CrearServer(nombre, ver, str(numMods), origenMods)
            elif self.modImporter.cancel:
                self.CargadorPantalla(0)
                return
            else:
                self.sql.CrearServer(nombre, ver)
                
        else:
            self.sql.CrearServer(nombre,ver)
        self.sql.ActivarServer(nombre)
        mbox.showinfo("EXITO", "Será este el server activo")
        
        self.barraDeCarga.stop()
        
        self.UpdateData()
        
        
        
        self.CargadorPantalla(0)
        
    def P_Crear(self):

        self.pantalla = self.pantallas[1]
        
        self.test = FontLabel(self.pantalla, text = "Crear Servidor")
        self.test.grid(row = 0, column = 0)

        self.fDatos = ttk.Frame(self.pantalla)
        
        self.tServer = FontLabel(self.fDatos, text = "Nombre servidor: ")
        self.tServer.grid(row = 0, column = 0)

        self.vServer = tk.StringVar(value="XanaCraft")
        self.nServer = ttk.Entry(self.fDatos, textvariable = self.vServer)
        self.nServer.grid(row = 0, column = 1)

        

        self.tVer = FontLabel(self.fDatos, text = "Versión Mc: ")
        self.tVer.grid(row = 1, column = 0)
        
        self.vVer = tk.StringVar(value = "0.0.0")
        self.nVer = ttk.Entry(self.fDatos, textvariable = self.vVer)
        self.nVer.grid(row = 1, column = 1)


        self.fDatos.grid(row = 1, column = 0)

        self.barraDeCarga = ttk.Progressbar(self.pantalla, mode="indeterminate")
        self.barraDeCarga.grid(row = 2, column = 0, sticky=("N","S","E","W"))
        self.Separar(3)
        
        self.botones = tk.Frame(self.pantalla)

        self.bCrear = ttk.Button(self.botones, text = "Crear",
                             command = lambda: self.Crear())
        self.bCrear.grid(row = 0, column = 0)
        self.bListar = ttk.Button(self.botones, text = "Volver",
                             command = lambda: self.CargadorPantalla(0))
        self.bListar.grid(row = 0, column = 1)

        self.bSalir = ttk.Button(self.botones, text = "Salir",
                             command = lambda: self.parent.destroy())
        self.bSalir.grid(row = 1, column = 0, columnspan = 2)

        self.botones.grid(row = 4, column = 0)

        self.pantalla.focus_force()


    def Activar(self, serverPos):
        if(serverPos == ()):
            mbox.showwarning("Error", "Selecciona un server")
            return None
        self.barraDeCarga.start(40)
        print(f" SERVERS: {self.listaServers[list(serverPos)[0]][0]} + {self.actualServer}")
        if(self.listaServers[list(serverPos)[0]][0] == self.actualServer[0]):
            mbox.showinfo("AVISO", "El server ya se encuentra activado,\nprocediendo igualmente")
        try:
            self.sql.ActivarServer(self.listaServers[list(serverPos)[0]][0])
        except:
            mbox.showerror(f"ERROR {sys.exc_info()[0].__name__}",sys.exc_info()[1])
            self.barraDeCarga.stop()
            return
        mbox.showinfo("EXITO", "el server se ha cambiado sin problemas")
        self.barraDeCarga.stop()
        self.CargadorPantalla(0)

    def Borrar(self, serverPos):
        ## comprovar que se ha seleccionado uno
        if(serverPos == ()):
            mbox.showwarning("Error", "Selecciona un server")
            return None
        server = self.listaServers[list(serverPos)[0]]
        nameServer = server[0]
        if(nameServer == "Vanilla"):
            mbox.showwarning("ERROR", "No se puede borrar el server Vanilla")
            return None
        r = mbox.askyesno("Borrar Server?", "Desea continuar?")
        if(r ==False):
            return None
        r = False
        self.barraDeCarga.start(25)
        mbox.showinfo("Borrar Server?", "Se va a proceder a borrar el registro del server")

        if(server[2]!= "0"):
            r = mbox.askyesno("Borrar Mods?", "Quieres eliminar los mods?")
        if(r):
            self.sql.EliminarServer(nameServer, delMods=True)
        else:
            self.sql.EliminarServer(nameServer)
        mbox.showinfo("EXITO", "Se ha borrado el servidor")
        self.barraDeCarga.stop()
        self.sql.ActivarServer("Vanilla")

        self.CargadorPantalla(2)
        

    def Editar(self, serverPos):
        if(serverPos == ()):
            mbox.showwarning("Error", "Selecciona un server")
            return None
        server = self.listaServers[list(serverPos)[0]]
        
        nameServer = server[0]
        if(nameServer == "Vanilla"):
            mbox.showwarning("ERROR", "No se puede editar el server Vanilla")
            return None
        
        try: ## handle Errors
            self.modImporter.init(self.parent, server[0], server[1], edit = True)
        except:
            mbox.showerror(f"ERROR {sys.exc_info()[0].__name__}",sys.exc_info()[1])
            self.modImporter.ventana.destroy()
            return
        
        if(server[2] != "0"):
            try:
                self.modImporter.Importar("carpeta", auto = True, ruta = server[3])
            except:
                mbox.showerror(f"ERROR {sys.exc_info()[0].__name__}",sys.exc_info()[1])
                self.modImporter.ventana.destroy()
                return
        self.parent.wait_window(self.modImporter.ventana)
        if(self.modImporter.serverBorrar):
            self.Borrar(serverPos)
            
            
        elif(self.modImporter.crear):
            newData = self.modImporter.nameServer.get(),self.modImporter.version.get(), self.modImporter.numMods,self.modImporter.origenMods
            self.sql.EditarServer(server[0], newData)
            self.UpdateData()
            self.Activar(serverPos)
            mbox.showinfo("EXITO", "Server Editado")
        self.CargadorPantalla(0)

        
        

        
        
    def P_Leer(self):

        self.titulo = FontLabel(self.pantalla, text = "Selecciona el servidor:")
        self.titulo.grid(row = 0, column = 0, columnspan = 2)

        self.UpdateData()

        self.fListaServers = tk.Frame(self.pantalla)

        self.lista = tk.Listbox(self.fListaServers, width = 50,
                             height = 10)
        self.lista.grid(row = 0, column = 0, sticky=("N","S","E","W"))

        self.scroll = ttk.Scrollbar(self.fListaServers, orient = tk.VERTICAL,
                                command = self.lista.yview)
        self.scroll.grid(row = 0, column = 1, sticky = ("N","S"))
        
        self.lista["yscrollcommand"] = self.scroll.set

        self.lista.bind("<Return>", lambda e: self.Activar(self.lista.curselection()))
        self.lista.bind("<Delete>", lambda e: self.Borrar(self.lista.curselection()))


        if(self.actualServer == ["Vanilla"]):
            fff  = mbox.showwarning("Sin Servers", "Es necesario que crees uno")
        else:
            datos = []

            for server in self.listaServers:
                serv = f"Server: {server[0]} en versión {server[1]} con {server[2]} mods."
                self.lista.insert("end", serv)
            

        self.fListaServers.grid(row = 1, column = 0, sticky=("N","S","E","W"))
        
        self.barraDeCarga = ttk.Progressbar(self.pantalla, mode="indeterminate")
        self.barraDeCarga.grid(row = 2, column = 0, sticky=("N","S","E","W"))
        
        self.Separar(3)
        
        self.botones = tk.Frame(self.pantalla)

        self.bCrear = ttk.Button(self.botones, text = "Activar",
                             command = lambda: self.Activar(self.lista.curselection()))
        self.bCrear.grid(row = 0, column = 0)
        self.bBorrar = ttk.Button(self.botones, text = "Editar",
                             command = lambda: self.Editar(self.lista.curselection()))
        self.bBorrar.grid(row = 0, column = 1)
        self.bListar = ttk.Button(self.botones, text = "Volver",
                             command = lambda: self.CargadorPantalla(0))
        self.bListar.grid(row = 0, column = 2)

        self.bSalir = ttk.Button(self.botones, text = "Salir",
                             command = lambda: self.parent.destroy())
        self.bSalir.grid(row = 1, column = 0, columnspan = 3)

        self.botones.grid(row = 4, column = 0)
    
        
        
if (__name__ == "__main__"):
    vMaestra = tk.Tk()

    try:
    	frontEnd = FrontEnd(vMaestra)
    except tk.TclError:
        mbox.showerror(f"ERROR {sys.exc_info()[0]}", sys.exc_info()[1])
    except SystemExit:
        sys.exit()
    except:
        mbox.showerror(f"ERROR {sys.exc_info()[0]}", sys.exc_info()[1])
        vMaestra.destroy()
        sys.exit()

    vMaestra.mainloop()
