# -*- coding: utf-8 -*-
'''
Instalador de ModManager 2.x
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
### instalador Mod Manager 2.x
#### Daniel García

import os, shutil
import platform as pf


class Instalador():
    def __init__(self):
        self.path = ""

        ## Detectar SO y por ende si .py o exe
        self.OS = pf.system()
        
        if self.OS == "Windows":
            self.path = f"C:/Users/{os.getlogin()}/Appdata/Roaming/.minecraft/mods"
            print("Corriendo en Windows")
        elif self.OS == "Linux":
            self.path == f"/home/{os.getlogin()}/.minecraft/mods"
            print("Linux based detectado")
        elif self.OS == "Darwin":
            self.path == f"/home/{os.getlogin()}/.minecraft/mods" ## a comprovar
            print("Mac detectado")
        else:
            self.path == f"~/.minecraft/mods"
            print("No se ha podido identificar el SO")
        ## detectar si ModManager esta en .exe o .py
            self.modo = "EXE"
        if ".exe" in os.listdir(os.getcwd()+"/Data"):
            self.modo = "EXE"
        else:
            self.modo = "PY"
        print(self.modo)
            
        print("Bienvenido al instalador de ModManager 2.x")
        print("Por favor, tomese su tiempo a leer lo siguiente")
        readme = open("sortLICENSE")
        print(readme.read())
        print("")
        print("Por favor Selecciona una opción a continuación")
        for tries in range(3):
            respuestas = ["I","D","A","S","L"]
            r = input("(I)nstalar, (D)esinstalar, (A)ctualizar, (S)alir, (L)icencia: ").upper()
            if r in respuestas:
                if r == "I":
                    self.Instalar()
                elif r == "D":
                    self.Desinstalar(hasExit = True) ## solo debug v1x = True
                elif r == "A":
                    self.Actualizar()
                elif r == "L":
                    self.Licencia()
                elif r == "S":
                    exit()
                else: print("no se como hemos llegado aquí")
            else:
                print("Por favor, vuelvelo a intentar")
        print("SE HA DETECTADO UN BOT, ABORTEN")
        self.Pause()
        exit()

    def Pause(self):
        input("Pulse enter para continuar")
    def Licencia(self):
        licencia = open('LICENSE')
        print(licencia.read())
        
    def Instalar(self):
        ## mirar que existe minecraft, claro esta
        try:
            os.listdir(self.path)
        except FileNotFoundError:
            print("ERROR: Minecraft no esta instalado o no esta en la ruta predeterminada\nAbortando...")
            self.Pause()
            exit()
        ##mirar que 1.x no instalada
        
        try:
            a = os.listdir(self.path+"/data")
            if "data.xml" in a:
                print("ADVERTENCIA: Version 1.x de ModManager ha sido encontrada, será desinstalada")
                print("Pulse ctrl+C para cancelar o")
                
                self.Desinstalar(v1x = True)
        except FileNotFoundError:
            pass
        except KeyboardInterrupt:
            self.__init__()
        
            
        print()
        print("Procediendo a instalar la version 2.x de ModManager")
        self.Pause()
        try:
            b = os.listdir(self.path+"/data")
            if "data.db" in b:
                print("ADVERTENCIA: Se ha encontrado datos guardados de ModManager 2.x\nSe recomienda utilizar (A)ctualizar para no perder datos")
                print("Pulse ctrl+C para cancelar o")
                self.Pause()
        except KeyboardInterrupt:
            return
        except FileNotFoundError:
            pass
        print("Copiando archivos del programa")
        shutil.copytree("Data/data", self.path+"/data")
        print("Copiando programa en si")
        if(self.modo == "EXE"):
            shutil.copy("Data/ModManager.exe", self.path)
        elif self.modo == "PY":
            shutil.copy("Data/FrontEnd.pyw", self.path)
            shutil.copy("Data/BackEnd.py", self.path)
            shutil.copy("Data/ModImporter.py", self.path)
            
        print("Creando acceso directo en el escritorio")
        ##shutil.copy("Mod_Manager.bat",f"C:/Users/{os.getlogin()}/Desktop")
        if(self.OS == "Windows"):
            link = open(f"C:/Users/{os.getlogin()}/Desktop/Mod Manager.bat", mode="w+")
            if(self.modo == "EXE"):
                link.write("@echo off \n%AppData%/.minecraft/mods/ModManager.exe")
            elif(self.modo == "PY"):
                link.write("@echo off \ncd %AppData%/.minecraft/mods/\nstart pythonw FrontEnd.pyw")
            link.close()
        else: ## linux
            link = open("/home/{os.getlogin()}/Desktop/Mod Manager.sh", mode="w+")
            if(self.mode == "EXE"):
                #link.write("@echo off \n ~/.minecraft/mods/ModManager.exe")
                pass
            elif(self.mode == "PY"):
                link.write("python3 /home/{os.getlogin()}//.minecraft/mods/FrontEnd.pyw")
            link.close()
            os.popen("chmod +x 'Mod Manager.sh'")
            
        print("Instalación completada")
        print("Ahora se saldrá del instalador, que disfrute del programa")
        self.Pause()
        exit()
            

    def Desinstalar(self, v1x = False, hasExit = False):
        self.Pause()
        if(v1x):
            print("procediendo a la desinstalación de 1.x ...")
            print("Borrando Python Embedido...")
            shutil.rmtree(self.path+"/python")
            shutil.rmtree(self.path+"/__pycache__")
            print("borrando archivos del programa")
            os.remove(self.path+"/FrontEnd.pyw")
            os.remove(self.path+"/BackEnd.pyw")
            os.remove(self.path+"/ModManager.bat")
        else:
            print("procediendo a la desinstalación de 2.x ...")
            try:
                shutil.rmtree(self.path+"/data")
            except FileNotFoundError:
                print("No hay nada que desintalar")
                return
            try:
                os.remove(self.path+"/ModManager.exe")
            except:
                pass
            try:
                os.remove(self.path+"/FrontEnd.pyw")
                os.remove(self.path+"/BackEnd.pyw")
                os.remove(self.path+"/ModManager.bat")
            except:
                pass
            
        

        if(self.OS == "Windows"):
            os.remove(f"C:/Users/{os.getlogin()}/Desktop/Mod Manager.bat")
        else:
            os.remove(f"/home/{os.getlogin()}/Desktop/Mod Manager.sh")
            
        print("Desinstalación completada")

        if(hasExit):
            print()
            r = input("Gracias por utilizar el instalador, desea hacer otra acción (S/N)").upper()
            if r == "S":
                pass
            elif r == "N":
                print("Saliendo")
                self.Pause()
                exit()
            
            

    def Actualizar(self):
        try:
            a = os.listdir(self.path+"/data")
            if "data.xml" in a:
                print("ADVERTENCIA: Version 1.x de ModManager ha sido encontrada, será desinstalada")
                print("Pulse ctrl+C para cancelar o")
                
                self.Desinstalar(v1x = True)
        except FileNotFoundError:
            print("No se ha encontrado ninguna instalación\nUtiliza (I)nstalar")
            return
        except KeyboardInterrupt:
            return
        print("Se va actualizar ModManager 2.x a una versión más actual")
        print("Los datos no se verán afectados, pero para cancelar pulse ctrl+C o...")
        self.Pause()
        print("Actualizando archivos de programa")
        if(self.modo == "EXE"):
            shutil.copy("Data/ModManager.exe", self.path)
        elif self.modo == "PY":
            shutil.copy("Data/FrontEnd.pyw", self.path)
            shutil.copy("Data/BackEnd.py", self.path)
            shutil.copy("Data/ModImporter.py", self.path)
            
        print("Actualización completada, que lo disfrute")
        self.Pause()
        exit()

if __name__ == "__main__":
    installer = Instalador()
