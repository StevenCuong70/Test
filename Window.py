#!/usr/bin/python
#-*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from Inspector import *
from widgets import *
from tkinter.filedialog import asksaveasfilename
import sys


class DragFrame(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.nomeVar = 'mainframe'
        self.resizing = False

    def drag_start(self, event):
        wg = event.widget
        wg.startX = event.x
        wg.startY = event.y

        if event.state & 0x0004:  # Check if Control key is pressed
            self.resizing = True
        else:
            self.resizing = False

        
    def drag_motion(self, event):
        wg = event.widget

        if self.resizing:
            delta_x = event.x - wg.startX
            delta_y = event.y - wg.startY

            new_width = wg.winfo_width() + delta_x
            new_height = wg.winfo_height() + delta_y

            if new_width > 0 and new_height > 0:
                wg.configure(width=new_width, height=new_height)
        else:
            x = wg.winfo_x() - wg.startX + event.x
            y = wg.winfo_y() - wg.startY + event.y
            wg.place(x=x, y=y)

    def on_release(self, event):
        self.resizing = False
        self.master.toolbox.inspector.inspect_widget(event.widget)



class WidgetWindow(Toplevel):
    def __init__(self, nomeVar='WindowDesigner'):
        super().__init__()
        self.geometry('450x550+230+20')
        self.title(nomeVar)
        self.filename = ''
        self.nomeVar = nomeVar

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainframe = DragFrame(self)
        self.mainframe.grid(sticky=(N, S, W, E))

        # pega as propriedades iniciais de window
        self.mainframe.props_inicial = {}
        for k in self.mainframe.keys():
            self.mainframe.props_inicial[k] = self.mainframe[k]

        # se fechar a janela abre dialogo de salvar arquivo
        self.protocol('WM_DELETE_WINDOW', self.close)

    def set_toolbox(self, toolbox):
        self.toolbox = toolbox

    def close(self):
        self.salvar()
        self.toolbox.inspector.withdraw()
        self.withdraw()

        for widget in self.mainframe.winfo_children():
            widget.destroy()

        self.toolbox.novo['state'] = 'normal'
        self.toolbox.salvar['state'] = 'disabled'
        self.toolbox.buttons_off()
        
    def salvar(self):        
        code = """#!/usr/bin/python
#-*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
"""

        code += """
%s = Tk()
%s.geometry('%s')
""" % (self.nomeVar, self.nomeVar, self.winfo_geometry())
        
        code += """
mainframe = ttk.Frame(%s)
mainframe.grid(row=0, column=0, sticky=(N,S,E,W))
%s.columnconfigure(0, weight=1)
%s.rowconfigure(0, weight=1)

""" % (self.nomeVar, self.nomeVar, self.nomeVar)
        
        code += self._parser_widget()
        code += "\n\n%s.mainloop()" % self.nomeVar
        
##        print(code)

        # message file dialog
        if self.filename:
            with open(self.filename,'w') as arq:
                arq.write(code)
        else:
            fn = asksaveasfilename(initialfile='app.py', defaultextension='*.py', filetypes=[('arquivos .py','*.py'),('todos arquivos','*.*')])
            with open(fn,'w') as arq:
                arq.write(code)

            self.title(fn)
            self.filename = fn

    def _parser_widget(self):
        wg_code = ''
        # pega todos os widgets dentro de window
        for wg in self.mainframe.children.values():
            props_atual = {}
            props_diff = {}
            
            # pega as propriedades atuais do widget
            for k in wg.keys():
                props_atual[k] = wg[k]

            # compara as propriedades iniciais e atuais do widget
            for p in props_atual.keys():
                if props_atual[p] != wg.props_inicial[p]:
                    props_diff[p] = props_atual[p]

            wg_code += wg.code(props_diff)
            
        return(wg_code)

        
if __name__=='__main__':
    Tk().withdraw()
    top = WidgetWindow()
    print('Widget Window ok')
##    top.mainloop()

    
