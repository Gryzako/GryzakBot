import customtkinter as ck
from datetime import datetime
from amulet_and_ring_detector import AmuletAndRingDetector
import time

ck.set_appearance_mode('Dark')
ck.set_default_color_theme('dark-blue')


class App(ck.CTk):
    def __init__(self):
        super().__init__()
        #Configure window
        self.geometry('400x450')
        self.resizable(False, False)
        self.title('Gryzak bot 1.0')

        #STATIC variable
        self.OBSCONNECTED = False
        self.host = "localhost"
        self.amuRingThread = None
        self.AmuRingStop_event = None

        #Tab configuration
        self.tab = ck.CTkTabview(self, width=400, height=300)
        self.tab.grid(row=0, column=0)
        self.tab.add('AutoHealing')
        self.tab.add('Ring&Amu')
        self.logBox = ck.CTkTextbox(self, state='disabled', width=400, height=150)
        self.logBox.grid(row=1, column=0)

        #AutoHealing configuration


        #Ring&Amu configuration
        self.stoneskincheckbox = self.create_checkbox(self.tab.tab('Ring&Amu'), text='Stone Skin')
        self.stoneskincheckbox.grid(row=0, column=0, pady=5)
        self.mightringcheckbox = self.create_checkbox(self.tab.tab('Ring&Amu'), text='Might Ring')
        self.mightringcheckbox.grid(row=1, column=0, pady=5)
        self.amuAndRingEnableButton = self.create_button(self.tab.tab('Ring&Amu'), text='Start', command=self.amuAndRingEnableButtonFunc)
        self.amuAndRingEnableButton.grid(row=2, column=0, pady=5, padx=5)
        self.amuAndRingDisableButton = self.create_button(self.tab.tab('Ring&Amu'), text='Stop', state='disabled', command=self.amuAndRingDisableButtonFunc)
        self.amuAndRingDisableButton.grid(row=2, column=1, pady=5, padx=5 )
    
    def create_button(self, parent, text, command=None, state='normal', width=100, height=40):
        return ck.CTkButton(parent, text=text, command=command, state=state, width=width, height=height)
    
    def create_label(self, parent, text, width=100, height=40):
        return ck.CTkLabel(parent, text=text, width=width, height=height)
    
    def create_entry(self, parent,  width=100, height=30):
        return ck.CTkEntry(parent, width=width, height=height)
    
    def create_checkbox(self, parent, text):
        return ck.CTkCheckBox(parent, text=text)
    
    def logging(self, message):
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.logBox.configure(state='normal')
        self.logBox.insert('0.0', f"{self.dt_string} - {message}\n")
        self.logBox.configure(state='disabled')

    def amuAndRingEnableButtonFunc(self):
        self.amuAndRingEnableButton.configure(state='disabled')
        self.amuAndRingDisableButton.configure(state='normal')
        stoneSkinStatus = self.stoneskincheckbox.get()
        mightRingStatus = self.mightringcheckbox.get()

        obs_instance = AmuletAndRingDetector()
        self.amuRingThread, self.AmuRingStop_event = obs_instance.startAmuAndRingEvent(self)
        self.logging(f"Started auto amulet and ring")

    def amuAndRingDisableButtonFunc(self):
        self.amuAndRingEnableButton.configure(state='normal')
        self.amuAndRingDisableButton.configure(state='disabled')
        obs_instance = AmuletAndRingDetector()
        obs_instance.stopAmuAndRingEvent(self.AmuRingStop_event, self.amuRingThread)
        self.logging(f"Stopped auto amulet and ring")


if __name__ == "__main__":
    app = App()
    app.mainloop()