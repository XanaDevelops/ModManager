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
print("########## INICIANDO INSTALADOR ################") ## para crear un enlace simbolico a ModManager.exe en ps New-Item -Path "rutaDestino" -ItemType SymbolicLink -Value "ruta\ModManager.exe"
import os, shutil,sys
import platform as pf
import subprocess as subp

print("Comprobando dependencias...")
needTkinter = True
needPillow = True
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox as mbox
    from tkinter import font as font
    import tkinter.filedialog as filed
    needTkinter = False
except:
    print("Tkinter no se encuentra instalado... se instalará posteriormente")
    
    
try:
    import PIL
    needPillow = False
except:
    print("Pillow no se encuentra instalado... se instalará posteriormente")
    
from Data.data.Custom import CustomFont_Label as FontLabel
from Data.data.Custom import CustomFont_Message as FontMessage

def PauseExit():
    input("Pulse enter para salir...")
    sys.exit()

def Pause():
    input("Pulse enter para continuar...")

def InstallTkinter(OS):
    if OS == "Windows":
        print("Actualmente no está soportado instalar Tkinter en Windows desde este instalador.\nCoprueba que a la hora de Instalar Python3 hayas marcado la opción de instalarlo")
        PauseExit()
    else:
        try:
            subp.run("sudo apt install python3-tk -y".split(" "))
            print("OK instalación")
        except:
            print("No se ha podido instalar Tkinter")
            PauseExit()
            
def InstallPip(OS):
    if OS == "Windows":
        print("Actualmente no está soportado instalar Pip3 en Windows desde este instalador.\nCoprueba que a la hora de Instalar Python3 hayas marcado la opción de instalarlo")
        PauseExit()
    else:
        try:
            subp.run("sudo apt install python3-pip -y".split(" "))
            print("OK instalación")
        except:
            print("No se ha podido instalar Pip3")
            PauseExit()

def InstallPillow(OS):
    print("Comprobando si esta pip3...")
    try:
        subp.run("pip3")
    except:
        print("Pip3, no se encuentra instalado, procediendo a su instalación...")
        InstallPip(OS)

    if OS == "Windows":
        try:
            subp.run("pip3 install Pillow".split(" "))
        except:
            print("Un error ha ocurrido durante la instalación...")
            PauseExit()
    else:
        try:
            subp.run("sudo pip3 install Pillow".split(" "))
        except:
            print("Un error ha ocurrido durante la instalación...")
            PauseExit()


class Instalador(object):
    def __init__ (self, parent):
        self.parent = parent
        self.parent.title("Instalador ModManager")

        self.ver = "2.6"
        
        self.parent.iconphoto(True, tk.PhotoImage(file="Data/data/icono.png"))
        #self.parent.iconphoto(True, tk.PhotoImage(file="data/icono.png"))

        self.OS = pf.system()

        self.rutaPre = ""

        if self.OS == "Windows":
            self.rutaPre = f"C:/Users/{os.getlogin()}/AppData/.minecraft/mods"
        else:
            self.rutaPre = f"~/.minecraft/mods"

        #self.bannerIMG = PIL.Image.open("tezt.png")
        self.bannerIMG = PIL.Image.open("Data/tezt.png")

        self.Pantalla()

        ## variables para centrar la ventana, no tienen self porque realmente
        ## no hace falta
        xOffset = int(self.parent.winfo_screenwidth()/3 - 400/2)
        yOffset = int(self.parent.winfo_screenheight()/2.5 - 320/2)
        self.parent.geometry(f"+{xOffset}+{yOffset}")

        self.installationStatus = 0 #Estado de la instalación, para poder revertir los cambios

    def CargarTexto(self,id): # intro, licencia, ruta, inta, finish
        try:
            self.textFrame.destroy()
        except:
            pass
        self.textFrame = ttk.Frame(self.pantalla)
        if id == 0:#
            self.titulo = FontLabel(self.textFrame, text = "Bienvenid@ al instalador de ModManager", size = 30)
            self.titulo.grid(row = 0, column = 0)

            self.intro = FontLabel(self.textFrame, text = f"Este asistente le ayudará con la instalación de ModManager {self.ver}")
            self.intro.grid(row = 1, column = 0)

            self.intro2 = FontLabel(self.textFrame, text = "Por favor, haga click en iniciar para proceder con la instalación")
            self.intro2.grid(row = 2, column = 0)

            self.copyr = FontLabel(self.textFrame, text = "Instalador de ModManager 2.x  Copyright ©2020  Daniel García Vázquez")
            self.copyr.grid(row = 3, column = 0, pady = 100)
            ## configurar botones
            self.botonVolver.config(text = "Volver")
            self.botonVolver.state((tk.DISABLED,))
            self.botonContinuar.config(text="Iniciar",
                                       command = lambda: self.CargarTexto(1))
            self.botonCancelar.config(text = "Cancelar")

        if id ==1:
            self.titulo = FontLabel(self.textFrame, text="Por favor, lea la licencia detenidamente antes de continuar", size = 20)
            self.titulo.grid(row = 0, column = 0)

            self.frameLista = ttk.Frame(self.textFrame)
        
            self.lista = tk.Listbox(self.frameLista, width = 100,
                             height = 20, activestyle = tk.NONE)
            self.lista.grid(row = 1, column = 0, sticky=("N","S","E","W"))

            self.scroll = ttk.Scrollbar(self.frameLista, orient = tk.VERTICAL,
                                command = self.lista.yview)
            self.scroll.grid(row = 1, column = 1, sticky = ("N","S"))
        
            self.lista["yscrollcommand"] = self.scroll.set
            
            #with open("../LICENSE", "r") as license:
            with open("LICENSE", "r") as license:
                for linea in license.readlines():
                    self.lista.insert(tk.END, " "*35 +linea)

            self.frameLista.grid(row= 1, column = 0)

            self.garantia = FontLabel(self.textFrame, text= "ACEPTA también que el programa viene sin NINGUNA GARANTÍA y que NO me hago")
            self.garantia.grid(row = 2, column = 0)
            self.garantia2 = FontLabel(self.textFrame, text ="responsable de ningún problema que pueda causar ModManager o su instalador")
            self.garantia2.grid(row = 3, column = 0)
            
            #botones
            self.botonVolver.config(command = lambda: self.CargarTexto(0))
            self.botonVolver.state(("!disabled",))
            self.botonContinuar.config(text = "Aceptar", command = lambda: self.CargarTexto(2))

        if id == 2:
            self.titulo = FontLabel(self.textFrame, text="Instalar ModManager", size = 30)
            self.titulo.grid(row = 0, column = 0, columnspan = 2)

            self.subtitulo = FontLabel(self.textFrame, text = "Introduzca la ruta donde instalar ModManager:", size = 20)
            self.subtitulo.grid(row = 1, column = 0, columnspan = 2)

            self.rutaInstalacion = tk.StringVar()

            self.c = font.Font(size=16)
            self.s = ttk.Style()
            self.s.configure("ruta.TEntry", foreground = "black")
            self.s.configure("rutaMal.TEntry", foreground = "red")

            self.entryRuta = ttk.Entry(self.textFrame, textvariable=self.rutaInstalacion,
                                       width = 50, font= self.c, style = "ruta.TEntry")
            self.entryRuta.grid(row = 2, column = 0)
            self.botonRuta = ttk.Button(self.textFrame, text = "...", command = lambda: self.PreguntarRuta())
            self.botonRuta.grid(row = 2, column  =1)

            self.mensaje = FontLabel(self.textFrame, text = "test")
            self.mensaje.grid(row = 3, column = 0, columnspan = 2)

            if self.OS == "Windows":
                self.rutaInstalacion.set(f"C:/Users/{os.getlogin()}/Appdata/Roaming/.minecraft/mods") ##arreglar Appdata de debug !!
            else:
                self.rutaInstalacion.set(f"/home/{os.environ['USER']}/.minecraft/mods")

            self.rutaInstalacion.trace("w", lambda a,e,i: self.ComprobarRuta())

            self.ComprobarRuta()

            #botones
            self.botonVolver.config(command = lambda: self.CargarTexto(1))
            
            self.botonContinuar.config(text = "Instalar", command = lambda: self.Instalar())

        self.textFrame.grid(row = 0, column = 1)

    def Instalar(self):
        modo = ""
        if "exe" in os.listdir("."):
            modo = "EXE"
        else:
            modo = "PY"
        if modo == "EXE":
            shutil.copy(sys._MEIPASS+"/ModManager.exe", self.rutaInstalacion.get())
            shutil.copytree(sys._MEIPASS+"/data", self.rutaInstalacion.get())
        elif modo == "PY":
            shutil.copytree("./Data", self.rutaInstalacion.get(), dirs_exist_ok=True)
            

    def PreguntarRuta(self):
        ruta = filed.askdirectory()
        print(ruta)
        if ruta != "":
            self.rutaInstalacion.set(ruta)

    def ComprobarRuta(self):
         try:
            os.listdir(self.rutaInstalacion.get())
            self.mensaje.destroy()
            mensaje = ""
            if "mods" in self.rutaInstalacion.get():
                mensaje = "ModManager se instalará en esa ruta"
            else:
                mensaje = "ModManager se instalará en esa ruta, pero no parece ser la carpeta 'mods'"
            self.mensaje = FontLabel(self.textFrame, text = mensaje)
            self.mensaje.grid(row = 3, column = 0, columnspan = 2)

            self.entryRuta.config(style = "ruta.TEntry")

            self.botonContinuar.state(("!disabled",))
             
         except FileNotFoundError:
            print("Minecraft no se encuentra en su ruta predeterminada")
            self.mensaje.destroy()
            self.mensaje = FontLabel(self.textFrame, text = "Esta ruta no existe. Introduzca la ruta de la carpeta 'mods' de Minecraft")
            self.mensaje.grid(row = 3, column = 0, columnspan = 2)
            
            self.entryRuta.config(style = "rutaMal.TEntry")

            self.botonContinuar.state(("disabled",))

        
         
            

    def Pantalla(self):
        self.pantalla = ttk.Frame(self.parent)

        self.banner = PIL.ImageTk.PhotoImage(self.bannerIMG, PIL.Image.ANTIALIAS)
        self.bannerLabel = ttk.Label(self.pantalla, image = self.banner)
        self.bannerLabel.grid(row = 0, column = 0)


        self.separador = ttk.Separator(self.pantalla)
        self.separador.grid(row = 1, column = 0, columnspan = 2)

        
        self.botones = ttk.Frame(self.pantalla)
        self.vacioBotones = ttk.Frame(self.botones, width=500).grid(row = 0, column = 0)
        self.botonVolver = ttk.Button(self.botones, text= "default")
        self.botonVolver.grid(row = 0, column = 1)
        self.botonContinuar = ttk.Button(self.botones, text= "dafault")
        self.botonContinuar.grid(row = 0, column = 2)
        self.botonCancelar = ttk.Button(self.botones, text = "difault",
                                        command = lambda: self.Salir())
        self.botonCancelar.grid(row = 0, column = 3)

        self.botones.grid(row = 2, column = 1)

        self.CargarTexto(0)
        

        self.pantalla.pack()



    def Salir(self):
        r = mbox.askyesno("ATENCIÓN", "¿Desea salir del instalador?")
        if r:
            if self.installationStatus == 0:
                sys.exit()


def init():
    vInsta = tk.Tk()
    installer = Instalador(vInsta)
    vInsta.mainloop()

if __name__  == "__main__":
    #print(needTkinter, needPillow)
    
    if not any([needPillow,needTkinter]):
        init()
        
    else:
        OS = pf.system()

        print("Ahora se va a instalar las dependencias", end="")
        if OS != "Windows" or "Instalador.exe" in os.listdir():
            print("Se le deberia pedir privilegios de adminstrador durante el proceso")
        else:
            print("\n")
        
        if needTkinter:
            InstallTkinter(OS)
        if needPillow:
            InstallPillow(OS)

        print("Comprobando que se han instalado correctamente las dependencias")

        try:
            import tkinter as tk
            import tkinter.ttk as ttk
            from tkinter import messagebox as mbox
            import tkinter.filedialog as filed
            import PIL
    
        except:
            print("No se ha podido importar las dependencias...")
            print(f"ERROR {sys.exc_info()[0]} ", sys.exc_info()[1])
            PauseExit()
        finally:
            init()

    
   
