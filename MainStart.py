from tkinter import *
from Window import *
from Toolbox import *
from Inspector import *

if __name__=='__main__':
    Tk().withdraw()

    inspector = WidgetInspector()
    window = WidgetWindow()
    toolbox = WidgetToolbox(window, inspector)

    window.set_toolbox(toolbox)
    inspector.set_toolbox(toolbox)

    inspector.inspect_widget(window)

    print('Ururau Tkinter GUI Designer ok')
    toolbox.mainloop()
    
        

