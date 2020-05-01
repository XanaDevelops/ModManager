# -*- coding: utf-8 -*-

### instalador Mod Manager 2.x
#### Daniel García

import os, shutil


class Instalador():
    def __init__(self):
        self.path = f"C:/Users/{os.getlogin()}/Appdata/Roaming/.minecraft/mods"
        print("Bienvenido al instalador de ModManager 2.x")
        print("Por favor, tomese su tiempo a leer lo siguiente")
        readme = open("conditions.txt")
        print(readme.read())
        print("")
        print("Por favor Selecciona una opción a continuación")
        for tries in range(3):
            respuestas = ["I","D","A","S"]
            r = input("(I)nstalar, (D)esinstalar, (A)ctualizar, (S)alir: ").upper()
            if r in respuestas:
                if r == "I":
                    self.Instalar()
                elif r == "D":
                    self.Desinstalar(hasExit = True) ## solo debug v1x = True
                elif r == "A":
                    self.Actualizar()
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
            self.__init__()
        except FileNotFoundError:
            pass
        print("Copiando archivos del programa")
        shutil.copytree("Data/data", self.path+"/data")
        print("Copiando programa en si")
        shutil.copy("Data/ModManager.exe", self.path)
        print("Creando acceso directo en el escritorio")
        shutil.copy("Mod_Manager.bat",f"C:/Users/{os.getlogin()}/Desktop")
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
            os.remove(self.path+"/ModManager.exe")
            
        shutil.rmtree(self.path+"/data")
        
        os.remove(f"C:/Users/{os.getlogin()}/Desktop/Mod_Manager.bat")
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
        print("Se va actualizar ModManager a una versión más actual")
        print("Los datos no se verán afectados, pero para cancelar pulse ctrl+C o...")
        self.Pause()
        print("Actualizando archivos de programa")
        shutil.copy("Data/ModManager.exe", self.path)
        print("Actualización completada, que lo disfrute")
        self.Pause()
        exit()

if __name__ == "__main__":
    installer = Instalador()
