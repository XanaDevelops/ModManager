# -*- coding: utf-8 -*-

################
### ManagerMods para MC todas versiones v2.0.0 beta
### codigo por Daniel G.
#############


import tkinter as tk


from tkinter import ttk as ttk
import tkinter.filedialog as filed
import tkinter.messagebox as mbox

from BackEnd import *
from ModImporter import *
from data.Style import *
from data.Custom import CustomFont_Label as FontLabel

import os

class FrontEnd(tk.Frame):
    def __init__(self, parent):

        self.verApp = "2.0.0 beta"
        self.parent = parent

        self.parent.title("Manager Mods")
        self.parent.geometry("400x300")
        
        self.parent.iconphoto(True, tk.PhotoImage(file="data/icono.png"))

        self.sql = BackEnd()
        self.modImporter = ModImporter(self.parent)
        self.style = Styles()
        self.font = "data/Minecraftia-Regular.ttf"

        self.pantallas = [tk.Frame(self.parent), ## inicio
                          tk.Frame(self.parent), ## crear
                          tk.Frame(self.parent)] ## navegar servers
        
        #self.P_Inicial()
        #self.P_Crear()
        self.firma = tk.Label(self.parent, text= f"Daniel Garcia Vazquez 2020© v{self.verApp}")
        self.firma.pack(side=tk.BOTTOM)
        self.CargadorPantalla(0)
        
        
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
    def Separar(self, fila):
        self.separador = ttk.Separator(self.pantalla, orient = tk.VERTICAL,
                                       style = "TSeparator")
        
        self.separador.grid(row = fila, column = 0, sticky = ("N","S","W","E"), pady = 5)
    def UpdateData(self):
        self.listaServers = self.sql.VerServers()
        print(self.listaServers)

        for server in self.listaServers:
            if server[4] == 1:
                self.actualServer = server
                break
        if len(self.listaServers) == 1 and self.listaServers[0][0] == "Vanilla":
            self.soloVanilla = True
        else:
            self.soloVanilla = False
        
    def P_Inicial(self):
        self.pantalla = self.pantallas[0]

        self.titular = tk.Frame(self.pantalla, relief = tk.RAISED, bd=10)

        
        self.titulo = FontLabel(self.titular, text = "Manager de Mods",
                                size = 25) 
        self.titulo.grid(row = 0, column = 0)
        self.subTitulo = FontLabel(self.titular, text = "Preocupate solo de jugar", size = 12)
        self.subTitulo.grid(row = 1, column = 0)

        self.titular.grid(row = 0, column = 0)

        ##
        self.UpdateData()
        #####
        if(self.soloVanilla):
            fff  = mbox.showwarning("Sin Servers", "Es necesario que crees uno")
        
        self.infoS = tk.Frame(self.pantalla, relief = tk.RIDGE, bd=5)

        self.tServer = FontLabel(self.infoS, text = "Servidor Activo: ",)
        self.tServer.grid(row = 0, column = 0)
        self.nServer = FontLabel(self.infoS, text = self.actualServer[0])
        self.nServer.grid(row = 0, column = 1)

        

        self.tVer = FontLabel(self.infoS, text = "Versión Mc: ")
        self.tVer.grid(row = 1, column = 0)
        self.vVar = tk.StringVar(value="")
        self.vVar.set(self.actualServer[1])
        
        self.nVer = FontLabel(self.infoS, text = self.vVar.get())
        self.nVer.grid(row = 1, column = 1)

        self.tMod = FontLabel(self.infoS, text = "Mods utilizados: ")
        self.tMod.grid(row = 2, column = 0)
        self.vMods = tk.StringVar(value="")
        self.vMods.set(self.actualServer[2])

        self.nMod = FontLabel(self.infoS, text = self.vMods.get())
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
        nombre = self.vServer.get()
        ver = self.vVer.get()
        
        for server in self.listaServers:
            
            if(nombre.upper() == server[0].upper()):
                mbox.showwarning("ERROR", "Ya existe un server con ese nombre")
                return None

        self.barraDeCarga.start(25)
        
        
        r = mbox.askyesno("Mods?", "Desea incluir Mods?")
        if(r):
            self.modImporter.init(self.parent, nombre, ver)
            
            self.parent.wait_window(self.modImporter.ventana)
            
            if(self.modImporter.crear):
                numMods, origenMods = self.modImporter.numMods,self.modImporter.origenMods
                mbox.showinfo("Mods Añadidos", "Los mods han sido añadidos")     
                print("exxitzz")
                self.sql.CrearServer(nombre, ver, str(numMods), origenMods)
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
            mbox.showinfo("ERROR", "El server ya se encuentra activado,\nprocediendo igualmente")
        self.sql.ActivarServer(self.listaServers[list(serverPos)[0]][0])
    
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
        
        self.modImporter.init(self.parent, server[0], server[1], edit = True)
        if(server[2] != "0"):
            self.modImporter.Importar("carpeta", auto = True, ruta = server[3])
            
        self.parent.wait_window(self.modImporter.ventana)
        if(self.modImporter.serverBorrar):
            self.Borrar(serverPos)
            
            
        elif(self.modImporter.crear):
            newData = self.modImporter.nameServer.get(),self.modImporter.version.get(), self.modImporter.numMods,self.modImporter.origenMods
            self.sql.EditarServer(server[0], newData)
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

    frontEnd = FrontEnd(vMaestra)

    vMaestra.mainloop()
