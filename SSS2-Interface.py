import tkinter as tk
from tkinter import ttk
import serial as ser


class SSS2(ttk.Frame):
    """The SSS2 gui and functions."""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()
        
 
    def init_gui(self):
        """Builds GUI."""
        self.root.title('Smart Sensor Simulator Interface')

        self.pack(fill = tk.BOTH)
        #self.grid( column=0, row=0, sticky='nsew') #needed to display
       

        self.tabs = ttk.Notebook(self, name='tabs')
        self.tabs.enable_traversal()
        self.tabs.pack(fill=tk.BOTH,padx=2, pady=2)

        # create each Notebook tab in a Frame
        #Create a Settings Tab to amake the adjustments for sensors
        self.settings = tk.Frame(self.tabs, name='settings')
        tk.Label(self.settings,
                 text="Smart Sensor Simulator 2 Settings Adjustment").grid(row=0,
                     column=0,columnspan=2,sticky=tk.E)
        self.tabs.add(self.settings, text="SSS2 Settings") # add tab to Notebook
        self.adjust_settings()
        

        #Create a Networks Tab to make the adjustments for J1939, CAN amd J1708
        self.networks = tk.Frame(self.tabs, name='networks')
        tk.Label(self.networks,
                 text="Vehicle Newtorking").grid(row=0,column=0)
        self.tabs.add(self.networks, text="Vehicle Newtorking") # add tab to Notebook

        #Create a Connections Tab to interface with the SSS
        self.connections = tk.Frame(self.tabs, name='connections')
        tk.Label(self.connections,
                 text="SSS2 to PC Connection").grid(row=0,column=0)
        self.tabs.add(self.connections, text="USB connection with the SSS2") # add tab to Notebook

        self.root.option_add('*tearOff', 'FALSE')
        self.menubar = tk.Menu(self.root)
 
        self.menu_file = tk.Menu(self.menubar)
        self.menu_edit = tk.Menu(self.menubar)

        self.menu_file.add_command(label='Exit', command=self.root.quit)

        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')


        self.root.config(menu=self.menubar)

        ttk.Label(self, text='Synercon Technologies, LLC').pack(side='left')

    def adjust_settings(self):
        """Adjusts the potentiometers and other analog outputs"""
        # Button to do something on the right
        self.adjust_enable_button =  ttk.Checkbutton(self.settings, text="Enable Adjustment",
                                            command=self.send_enable_command)
        self.adjust_enable_button.grid(row=1,column=0,sticky=tk.W)
        self.adjust_enable_button.state(['!alternate']) #Clears Check Box
        self.adjust_enable = self.adjust_enable_button.instate(['selected'])

        self.potentiometer01 = potentiometer(self.settings,number = 1,row=2,connector="J24:1")
        self.potentiometer02 = potentiometer(self.settings,number = 2,row=3,connector="J24:2")

    def send_enable_command(self):
        print(self.adjust_enable_button.state())
        if self.adjust_enable_button.instate(['selected']):
            print("Checked")
        else:
            print("Not Checked")          
    
    def on_quit(self):
        """Exits program."""
        quit()

class potentiometer():
    def __init__(self, parent,number = 1, row=2,col=0,connector="J18:X",label="Potentiometer",*args, **kwargs):
        #ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.pot_row=row
        self.pot_col=col
        self.pot_number=number
        self.label = label+" "+str(number)
        self.name = self.label.lower()
        self.connector=connector
        self.setup_potentometer()
        
          
    def setup_potentometer(self):        
        self.potentiometer_frame = tk.LabelFrame(self.root, name=self.name,text=self.label)
        self.potentiometer_frame.grid(row=self.pot_row,column=self.pot_col,sticky=tk.W)

        self.terminal_A_voltage_frame = tk.LabelFrame(self.potentiometer_frame, name='terminalAvoltage'+str(self.pot_number),text="Terminal A Voltage")
        self.terminal_A_voltage_frame.grid(row=0,column=0,columnspan=3)

        self.terminal_A_setting = tk.StringVar()
        
        
        self.twelve_volt_switch = ttk.Radiobutton(self.terminal_A_voltage_frame, text="+12V", value="+12V",
                                            command=self.send_terminal_A_voltage_command,
                                                  variable = self.terminal_A_setting)
        self.twelve_volt_switch.grid(row=0,column = 0,sticky=tk.W)
        
        self.five_volt_switch = ttk.Radiobutton(self.terminal_A_voltage_frame, text="+5V", value="+5V",
                                            command=self.send_terminal_A_voltage_command,
                                                variable = self.terminal_A_setting)
        self.five_volt_switch.grid(row=0,column = 1)

        tk.Label(self.terminal_A_voltage_frame,text=self.connector).grid(row=0,column=2, sticky="NE")
        
        self.other_volt_switch = ttk.Radiobutton(self.terminal_A_voltage_frame, text="Other:", value="Other",
                                                 command=self.send_terminal_A_voltage_command,
                                             variable = self.terminal_A_setting)
        self.other_volt_switch.grid(row=1,column = 0,sticky=tk.W)

        self.other_volt_value = ttk.Entry(self.terminal_A_voltage_frame,width=5)
        self.other_volt_value.grid(row=1,column = 1)

        self.other_volt_button = ttk.Button(self.terminal_A_voltage_frame,text="Set Voltage",
                                            state=tk.DISABLED,
                                            command = self.send_terminal_A_voltage_command)
        self.other_volt_button.grid(row=1,column = 2)
        
        self.terminal_A_voltage = tk.Scale(self.terminal_A_voltage_frame,
                                              from_ = 0, to = 12000, digits = 1, resolution = 100,
                                              orient = tk.HORIZONTAL, length = 180,
                                              sliderlength = 10, showvalue = 0, 
                                              label = None,
                                              command = self.set_terminal_A_voltage)
        self.terminal_A_voltage.grid(row=2,column=0,columnspan=3)

        self.terminal_A_connect_button =  ttk.Checkbutton(self.potentiometer_frame, text="Terminal A Connected",
                                            command=self.set_terminals)
        self.terminal_A_connect_button.grid(row=1,column=1,columnspan=2,sticky=tk.NW)
        self.terminal_A_connect_button.state(['!alternate']) #Clears Check Box
        
        self.wiper_position_slider = tk.Scale(self.potentiometer_frame,
                                              from_ = 1000, to = 0, digits = 1, resolution = 1,
                                              orient = tk.VERTICAL, length = 120,
                                              sliderlength = 10, showvalue = 0, 
                                              label = None,
                                              command = self.set_wiper_value)
        self.wiper_position_slider.grid(row=1,column=0,columnspan=1,rowspan=5,sticky="E")

        tk.Label(self.potentiometer_frame,text="Wiper Position").grid(row=2,column=1, sticky="S",columnspan=2)
        self.wiper_position_value = ttk.Entry(self.potentiometer_frame,width=10)
        self.wiper_position_value.grid(row=3,column = 1,sticky="E")

        self.wiper_position_button = ttk.Button(self.potentiometer_frame,text="Set Position",
                                            command = self.set_wiper_slider)
        self.wiper_position_button.grid(row=3,column = 2,sticky="W")
       
        self.wiper_connect_button =  ttk.Checkbutton(self.potentiometer_frame, text="Wiper Connected",
                                            command=self.set_terminals)
        self.wiper_connect_button.grid(row=4,column=1,columnspan=2,sticky=tk.NW)
        self.wiper_connect_button.state(['!alternate']) #Clears Check Box
        self.wiper_connect_button.state(['selected']) #checks the Box
        

        self.terminal_B_connect_button =  ttk.Checkbutton(self.potentiometer_frame,
                                                          text="Terminal B Connected",
                                                          command=self.set_terminals)
        self.terminal_B_connect_button.grid(row=5,column=1,columnspan=2,sticky=tk.SW)
        self.terminal_B_connect_button.state(['!alternate']) #Clears Check Box
        self.terminal_B_connect_button.state(['selected']) #Clears Check Box
        
        
    
    def set_terminals(self):
        self.terminal_A_connect_state = self.terminal_A_connect_button.instate(['selected'])
        self.terminal_B_connect_state = self.terminal_B_connect_button.instate(['selected'])
        self.wiper_connect_state = self.wiper_connect_button.instate(['selected'])
        terminal_setting = self.terminal_B_connect_state + 2*self.wiper_connect_state + 4*self.terminal_A_connect_state
        print(self.label,end=' ')
        print(" Terminal Setting = ", end='')
        print(terminal_setting)
        
    def send_terminal_A_voltage_command(self):
        print(self.label,end=' ')
        print("Terminal Voltage: ",end='')
        print(self.terminal_A_setting.get())
        if self.terminal_A_setting.get() == "+12V":
            self.terminal_A_voltage.set(12000)
            self.other_volt_button['state']=tk.DISABLED
        elif self.terminal_A_setting.get() == "+5V":
            self.terminal_A_voltage.set(5000)
            self.other_volt_button['state']=tk.DISABLED
        elif self.terminal_A_setting.get() == "Other":
            self.other_volt_button.config(state=tk.NORMAL)
    
    def set_terminal_A_slider(self):
        entry_value = self.other_volt_value.get()
        #print(self.other_volt_value.config())
        self.other_volt_value['foreground'] = "black"
        try:
            print(float(entry_value))
        except ValueError:
            #print("Not a good value")
            self.root.bell()
            self.other_volt_value['foreground'] = "red"
            
    def set_terminal_A_voltage(self,scale):
        print(self.terminal_A_voltage.get())
        self.other_volt_value.delete(0,tk.END)
        self.other_volt_value.insert(0,self.terminal_A_voltage.get()/1000.0)

        


if __name__ == '__main__':
    root = tk.Tk()
    SSS2(root)
    root.mainloop()
    root.destroy() # if mainloop quits, destroy window
