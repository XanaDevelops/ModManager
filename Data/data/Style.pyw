# -*- coding: utf-8 -*-

######
## hoja de estilos ModManager
## Codigo por Daniel Garcia
########

import tkinter as tk
from tkinter import ttk as ttk
from tkinter import font as tfont

class Styles():
    def __init__(self):
        self.estilo = ttk.Style()

        self.estilo.configure("TSeparator", background = "#cccccc")
        self.estilo.configure("TLabel", font=tfont.Font(name="Minecraft.tff"))
        
        
