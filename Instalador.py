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

import os, shutil,sys
import platform as pf
import subprocess as subp


class Instalador():
    def __init__(self):
        self.path = ""
        self.desktop = "Desktop"
        ## Detectar SO y por ende si .py o exe
        self.OS = pf.system()
        
        self.version = "2.4.1"

        
        if self.OS == "Windows":
            self.path = f"C:/Users/{os.getlogin()}/Appdata/Roaming/.minecraft/mods"
            print("Corriendo en Windows")
        elif self.OS == "Linux":
            self.path = f"/home/{os.environ['USER']}/.minecraft/mods"
            
            check = open(os.environ["HOME"]+"/.config/user-dirs.dirs")
            while(True):
                line = check.readline()
                if("DESKTOP" in line):
                    partLine = line.split("=")[1]
                    self.desktop = os.path.expandvars(partLine[1:len(partLine)-2])
                    break
            check.close()
            print("ruta = " + self.path)	
            print("Linux based detectado")
        elif self.OS == "Darwin":
            self.path = f"/home/{os.getlogin()}/.minecraft/mods" ## a comprobar
            print("Mac detectado")
        else:
            self.path = f"~/.minecraft/mods"
            print("No se ha podido identificar el SO")
        ## detectar si ModManager esta en .exe o .py
            self.modo = "EXE"
        if "ModManager.exe" in os.listdir(os.getcwd()+"/Data"):
            self.modo = "EXE"
        elif "ModManager" in os.listdir(os.getcwd()+"/Data"):
            self.modo = "ELF"
        else:
            self.modo = "PY"
        print(self.modo)
            
        print(f"Bienvenido al instalador de ModManager {self.version}")
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
                    sys.exit()
                else: print("no se como hemos llegado aquí")
            else:
                print("Por favor, vuelvelo a intentar")
        print("SE HA DETECTADO UN BOT, ABORTEN")
        self.Pause()
        sys.exit()

    def Pause(self):
        input("Pulse enter para continuar")
    def Licencia(self):
        licencia = open('LICENSE')
        print(licencia.read())
        licencia.close()
        
    def Instalar(self):
        ## mirar que existe minecraft, claro esta
        try:
            os.listdir(self.path)
        except FileNotFoundError:
            print("ERROR: Minecraft no esta instalado o no esta en la ruta predeterminada\nAbortando...")
            self.Pause()
            sys.exit()
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
        ## Primero comprobar las dependencias (linux solo), despues instalar los archivos
        self.Pause()

        if self.Modo == "PY":
            print("Son necesarias 2 dependencias para ModManager, Tkinter y Pillow (mediante pip3)")
            print("Se va a comprobar que estan instaladas...")
            self.Pause()
            try:
                import tkinter
            except:
                print("Tkinter no se ha podido importar")
                print("Se procederá a su instalacion, se le pedira su contraseña")
                try:
                    if self.OS == "Linux":
                        subp.run("sudo apt install python3-tk".split(" "))
                    else:
                        print("Instalación en Windows no implementada...")
                        raise Exception
                except:
                    print("No se ha podido instalar Tkinter, abortando...")
                    self.Pause()
                    sys.exit()
            
            try:
                from PIL import Image, ImageFont, ImageDraw, ImageTk
            except ModuleNotFoundError:
                print("Pillow no se encuentra instalado, se instalará\n")
                try:
                    print("Instalando Pillow")
                    if self.OS == "Windows":
                        err = subp.run("powershell Start-Process pip3 'install Pillow' -Verb runAs".split(" "))
                        if err.returncode != 0:
                            raise PermissionError()
                    else:
                        subp.run("sudo pip3 install Pillow".split(" "))
                except Exception or PermissionError:
                    print("ERROR, pip3 no se encuentra instalado, se debe instalar para continuar")
                    print("Se le pedirá su contraseña para descargar 'python3-pip'")
                    try:
                        if self.OS == "Linux":
                            subp.run("sudo apt install python3-pip -y".split(" "))
                        if self.OS == "Windows":
                            print("Aun no he implementado la forma de instalar pip3 en Windows...")
                            raise Exception
                    except PermissionError:
                        print("No se tienen privilegios necesarios para la instalación")
                        print("Se le deberia pedir su contraseña")
                        try:
                            if self.OS == "Windows":
                                err = subp.run("powershell Start-Process pip3 'install Pillow' -Verb runAs".split(" "))
                                if err.returncode != 0:
                                    raise PermissionError()
                            if self.OS == "Linux":
                                err = subp.run("sudo pip3 install Pillow".split(" "))
                                if err.returncode != 0:
                                    raise PermissionError()
                        except:
                            print("ERROR, no se ha podido descargar pip3, abortando...")
                            self.Pause()
                            sys.exit()
                
                except:
                    print("Ha ocurrido un error, no se ha podido instalar Pillow")
                    self.Pause()
                    sys.exit()
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
            shutil.copy("Data/FrontEnd.py", self.path)
            shutil.copy("Data/BackEnd.py", self.path)
            shutil.copy("Data/ModImporter.py", self.path)
            
        print("Creando acceso directo en el escritorio")
        ##shutil.copy("Mod_Manager.bat",f"C:/Users/{os.getlogin()}/Desktop")
        if(self.OS == "Windows"):
            link = open(f"C:/Users/{os.getlogin()}/Desktop/Mod Manager.bat", mode="w+")
            if(self.modo == "EXE"):
                link.write("@echo off \ncd %AppData%/.minecraft/mods/\nstart ModManager.exe")
            elif(self.modo == "PY"):
                link.write("@echo off \ncd %AppData%/.minecraft/mods/\nstart pythonw FrontEnd.py")
            link.write("\necho Iniciando ModManager")
            link.close()
        else: ## linux
            link = open(f"{self.desktop}/Mod Manager.sh", mode="w+")
            if(self.modo == "EXE"):
                #link.write("@echo off \n ~/.minecraft/mods/ModManager.exe")
                pass
            elif(self.modo == "PY"):
                link.write(f"cd /home/{os.environ['USER']}/.minecraft/mods/\npython3 FrontEnd.py")
            link.write("\necho Iniciando ModManager")
            link.close()
            os.popen(f"chmod +x {self.desktop}/'Mod Manager.sh'")
            
                        
                   
        print("Instalación completada")
        print("Ahora se saldrá del instalador, que disfrute del programa")
        self.Pause()
        sys.exit()
            

    def Desinstalar(self, v1x = False, hasExit = False):
        self.Pause()
        if(v1x):
            print("procediendo a la desinstalación de 1.x ...")
            print("Borrando Python Embedido...")
            shutil.rmtree(self.path+"/python")
            shutil.rmtree(self.path+"/__pycache__")
            print("borrando archivos del programa")
            os.remove(self.path+"/FrontEnd.py")
            os.remove(self.path+"/BackEnd.py")
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
                os.remove(self.path+"/FrontEnd.py")
                os.remove(self.path+"/BackEnd.py")
                os.remove(self.path+"/ModImporter.py")
            except:
                pass
            
        

        if(self.OS == "Windows"):
            os.remove(f"C:/Users/{os.getlogin()}/Desktop/Mod Manager.bat")
        else:
            os.remove(f"{self.desktop}/Mod Manager.sh")
            
        print("Desinstalación completada") 

        if(hasExit):
            print()
            r = input("Gracias por utilizar el instalador, desea hacer otra acción (S/N)").upper()
            if r == "S":
                pass
            elif r == "N":
                print("Saliendo")
                self.Pause()
                sys.exit()
            
            

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
        print("Ten en cuenta que no es lo mismo que instalar")
        print("Los datos no se verán afectados, pero para cancelar pulse ctrl+C o...")
        self.Pause()
        print("Actualizando archivos de programa")
        if(self.modo == "EXE"):
            shutil.copy("Data/ModManager.exe", self.path)
        elif self.modo == "PY":
            shutil.copy("Data/FrontEnd.py", self.path)
            shutil.copy("Data/BackEnd.py", self.path)
            shutil.copy("Data/ModImporter.py", self.path)
            
        print("Actualización completada, que lo disfrute")
        self.Pause()
        sys.exit()

if __name__ == "__main__":
    installer = Instalador()
