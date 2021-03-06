# -*- coding: utf-8 -*-
'''
BackEnd de ModManager 2.x
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
### ManagerMods para MC todas versiones v2.4
### codigo por Daniel G.
#############

import sqlite3 as sql
import os, shutil
import platform as pf

class BackEnd():
    def __init__(self):
        print("Iniciando BackEnd")
        self.sqlFile = "data/data.db"
        
        self.connect = sql.connect(self.sqlFile)
        
        self.cursor = sql.Cursor(self.connect)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Servers (
                                ServerName CHAR    PRIMARY KEY
                                                   NOT NULL,
                                Version    CHAR,
                                NumMods    CHAR,
                                PathMods   CHAR,
                                IsActive   BOOLEAN)''')

        self.cursor.execute("SELECT * FROM Servers")
        if(self.cursor.fetchall() == []):
            self.cursor.execute("INSERT INTO Servers VALUES ('Vanilla', '0.0.0', '0', NULL ,1)")
        self.connect.commit()
        self.OS = pf.system()

    def CrearServer(self, serverName, version, numMods = 0, origenMods = ""):
        print("Creando servidor...")
        print("    ",serverName)
        print("    ",version)
        print("    ",numMods)
        print("    ",origenMods)
        
        crearCarpeta = True
        modsPath = "None"
        if(numMods != 0):
            comp = ""
            if(self.OS == "Windows"):
                comp = f"{os.getcwd()}\\{serverName}"
            elif(self.OS == "Linux"):
                comp = f"{os.getcwd()}/{serverName}"
            if (comp == origenMods):
                crearCarpeta = False
            if(crearCarpeta):
                try:
                    os.mkdir(serverName)
                except:
                    pass
            modsPath = os.getcwd()+"/"+serverName
            
            for mod in os.listdir(origenMods):
                if(os.listdir(origenMods) == os.listdir(modsPath)):## hacer en ModImporter que si se importa de os.getcwd() en vez de crear temp los mueva ahí, solo funciona en modo carpeta y archivos
                   print("Carpetas iguales, no se copia")
                   break
                if ".jar" in mod or ".meta" in mod:
                    print("Copiando mod:", mod)
                    shutil.copy((origenMods+"/"+mod), modsPath)
        
        self.cursor.execute("INSERT INTO Servers VALUES (?,?,?,?,?)",
                            ((serverName, version, numMods, modsPath, False)))
        
        
        self.connect.commit()
        print("Server creado")
        try:
            shutil.rmtree(origenMods)
        except:
            print("Temp ya ha sido borrado")
    def EditarServer(self, serverName, newData):
        ## New data es [serverName, ver, numMods, origenMods]
        ## siempre se modifican ya que puede coincidir el nombre....
        print("Editando servidor:", serverName)
        self.cursor.execute("SELECT NumMods, PathMods FROM Servers WHERE ServerName=?", (serverName,))
        
        oldNumMods, oldPathMods = self.cursor.fetchall()[0]
        modsPath = "None"

        ##elimina los mods de /mods
        for mod in os.listdir():
            if ".jar" in mod or ".meta" in mod:
                os.remove(mod)

        ## si en los nuevos datos no hay mods los elimina       
        if(newData[2] == "0"):
            print("Server a Vanilla")
            for mod in os.listdir(oldPathMods):
                if ".jar" in mod or ".meta" in mod:
                    print("Eliminando mod",mod)
                    os.remove(f"{oldPathMods}/{mod}")
            os.rmdir(oldPathMods)
        else:
            # si antes era Vanilla crea la carpeta y copia
            if(oldNumMods == "0"):
                print("crear carpeta y mods")
                try:
                    os.mkdir(newData[0])
                except:
                    print("La carpeta ya existia, esto no deberia pasar")
                for mod in os.listdir(newData[3]):
                    if ".jar" in mod or ".meta" in mod:
                        print("Copiando mod", mod)
                        shutil.copy((newData[3]+"/"+mod),newData[0])
                
                modsPath = f"{os.getcwd()}/{newData[0]}"
            else:
                # si ya tenia mods los elimina y copia de la nueva fuente
                print("Reponer mods")
                for mod in os.listdir(oldPathMods):
                    print(f"Eliminando mod {mod} de la fuente antigua")
                    os.remove(f"{oldPathMods}/{mod}")
                ##si cambia el nombre elimina la carpeta vieja y crea la nueva
                ## pero ojo, modImporter debe comprovar que no exista!!!
                if(newData[0] != serverName):
                    print("nuevo nombre")
                    os.rmdir(oldPathMods)
                    os.mkdir(newData[0])
                    modsPath = os.getcwd()+"/"+newData[0]
                else:
                    modsPath = oldPathMods
                
                for mod in os.listdir(newData[3]):
                    print(f"Moviendo mod {mod} a la nueva ubicación") 
                    shutil.move(f"{newData[3]}/{mod}", modsPath)
        
        self.cursor.execute("UPDATE Servers set ServerName=?,Version=?,NumMods=?,PathMods=? WHERE ServerName=?",
                            (newData[0], newData[1], newData[2], modsPath, serverName))

        self.connect.commit()
        print("Server editado\n")
    def EliminarServer(self, serverName, delMods = False):
        ## recupera el path por si acaso
        print("Procediendo a eliminar", serverName)
        self.cursor.execute("SELECT PathMods FROM Servers WHERE ServerName=?", (serverName,))
        modsPath = self.cursor.fetchall()[0][0]

        ##guardar si era activo
        self.cursor.execute("SELECT IsActive FROM Servers WHERE ServerName=?", (serverName,))
        isActive = self.cursor.fetchall()[0][0]

        self.cursor.execute("DELETE FROM Servers WHERE ServerName=?", (serverName,))

        # elimina mods de /mods si es el server activo
        if int(isActive):
            print("Server es activo")
            print("Eliminando mods de /mods")
            for mod in os.listdir():
                if ".jar" in mod or ".meta" in mod:
                    os.remove(mod)

        ##elimina la carpeta
        if(delMods):
            print("eliminando la carpeta de los mods y los mods")
            shutil.rmtree(modsPath)
        ##Si la carpeta esta vacia la elimina igual
        else:
            if(serverName in os.listdir(os.getcwd())):
               if(os.listdir(serverName) == []):
                   print("Eliminando la carpeta de los mods")
                   os.rmdir(serverName)
               
        
        self.connect.commit()
        print("Server eliminado\n")

    def ActivarServer(self, serverName):
        print("Activando server",serverName)
        ##Comprueba si es vanilla el server o no
        self.cursor.execute("SELECT NumMods, PathMods FROM Servers WHERE ServerName=?", (serverName,))
        
        numMods, modsPath = self.cursor.fetchall()[0]
        

        ##En todo caso elimina los mods actuales
        for mod in os.listdir():
            if ".jar" in mod or ".meta" in mod:
                print("eliminando mod",mod,"de /mods")
                os.remove(mod)

        #Ahora cambia la activacion
        self.cursor.execute("UPDATE Servers set IsActive=0 WHERE IsActive=1")
        self.cursor.execute("UPDATE Servers set IsActive=1 WHERE ServerName=?", (serverName,))

        ##si tenia mods los copia
        if numMods != "0":
            for mod in os.listdir(modsPath):
                if ".jar" in mod:
                    print("Copiando mod",mod,"hacia /mods")
                    shutil.copy(f"{modsPath}/{mod}", os.getcwd())
        self.connect.commit()
        print("Server Activado\n")
    def VerServers(self):
        print("Accediendo a la base de datos")
        self.cursor.execute("SELECT * FROM Servers")

        lista = self.cursor.fetchall()

        return lista

        
if(__name__ == "__main__"):
    caca = BackEnd()    
