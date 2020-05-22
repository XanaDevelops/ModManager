# -*- coding: utf-8 -*-
'''
Script para mostrar fuentes externas de ModManager 2.x
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
# Modificado: Daniel García Vázquez
## bajo licencia GNU GPL v3
# Author: Miguel Martinez Lopez
## bajo la licencia MIT

from PIL import Image, ImageFont, ImageDraw, ImageTk

import textwrap

try:
    from Tkinter import Label
except ImportError:
    from tkinter import Label
    
def truetype_font(font_path, size):
    return ImageFont.truetype(font_path, size)

class CustomFont_Label(Label):
    def __init__(self, master, text, foreground="black", truetype_font=None, font_path="data/Minecraftia-Regular.ttf", family=None, size=14, **kwargs):   
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")
                
            # Initialize font
            
            truetype_font = ImageFont.truetype(font_path, size)
        
        width, height = truetype_font.getsize(text)

        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=truetype_font, fill=foreground)
        
        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)


class CustomFont_Message(Label):
    def __init__(self, master, text, width, foreground="black", truetype_font=None, font_path="data/Minecraftia-Regular.ttf", family=None, size=14, **kwargs):   
        if truetype_font is None:
            if font_path is None:
                raise ValueError("Font path can't be None")
                
            # Initialize font
            truetype_font = ImageFont.truetype(font_path, size)
    
        lines = textwrap.wrap(text, width=width)

        width = 0
        height = 0
        
        line_heights = []
        for line in lines:
            line_width, line_height = truetype_font.getsize(line)
            line_heights.append(line_height)
            
            width = max(width, line_width)
            height += line_height

        image = Image.new("RGBA", (width, height), color=(0,0,0,0))
        draw = ImageDraw.Draw(image)

        y_text = 0
        for i, line in enumerate(lines):
            draw.text((0, y_text), line, font=truetype_font, fill=foreground)
            y_text += line_heights[i]

        self._photoimage = ImageTk.PhotoImage(image)
        Label.__init__(self, master, image=self._photoimage, **kwargs)

if __name__ == "__main__":
    try:
        from Tkinter import Tk
    except ImportError:
        from tkinter import Tk
        
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    lorem_ipsum ="""Lorem ipsum dolor sit amet, 
consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore 
magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation 
ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril 
delenit augue duis dolore te feugait nulla facilisi."""

    # Use your font here: font_path
    CustomFont_Label(root, text="This is a text", font_path="Minecraftia-Regular.ttf", size=12).pack()
    CustomFont_Message(root, text=lorem_ipsum, width=40, font_path="Minecraftia-Regular.ttf", size=22).pack(pady=(30,0))
    
    root.mainloop()
