import customtkinter as ck
import pygetwindow as gw
from pywinauto import Application
from datetime import datetime
from amulet_and_ring_detector import AmuletAndRingDetector

ck.set_appearance_mode('Dark')
ck.set_default_color_theme('dark-blue')


class App(ck.CTk):
    def __init__(self):
        super().__init__()
        #Configure window
        self.geometry('400x450')
        self.resizable(False, False)
        self.title('GryzakBot 1.0')

        #STATIC variable
        self.amuRingThread = None
        self.AmuRingStop_event = None

        #Tab configuration
        self.tab = ck.CTkTabview(self, width=400, height=300)
        self.tab.grid(row=0, column=0)
        self.tab.add('Config')
        self.tab.add('BOT')
        self.logBox = ck.CTkTextbox(self, state='disabled', width=400, height=150)
        self.logBox.grid(row=1, column=0)

        #Configuration 
        self.ssLebale = self.create_label(self.tab.tab('Config'), text='Stone Skin')
        self.ssLebale.grid(row=0, column=0)
        self.ssButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.ssButton))
        self.ssButton.grid(row=0, column=1)
        self.mightLebale = self.create_label(self.tab.tab('Config'), text='Might Ring')
        self.mightLebale.grid(row=0, column=2)
        self.mightButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.mightButton))
        self.mightButton.grid(row=0, column=3)
        self.sioLebale = self.create_label(self.tab.tab('Config'), text='Sio')
        self.sioLebale.grid(row=1, column=0)
        self.sioButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.sioButton))
        self.sioButton.grid(row=1, column=1)
        self.uhLebale = self.create_label(self.tab.tab('Config'), text='Uh')
        self.uhLebale.grid(row=1, column=2)
        self.uhButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.uhButton))
        self.uhButton.grid(row=1, column=3)
        self.exuraVitaLebale = self.create_label(self.tab.tab('Config'), text='Exura Vita')
        self.exuraVitaLebale.grid(row=2, column=0)
        self.exuraVitaButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.exuraVitaButton))
        self.exuraVitaButton.grid(row=2, column=1)
        self.exuraMaxVitaLebale = self.create_label(self.tab.tab('Config'), text='Exura Max Vita')
        self.exuraMaxVitaLebale.grid(row=2, column=2)
        self.exuraMaxVitaButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.exuraMaxVitaButton))
        self.exuraMaxVitaButton.grid(row=2, column=3)
        self.UltimateManaLebale = self.create_label(self.tab.tab('Config'), text='Ultimate Mana')
        self.UltimateManaLebale.grid(row=3, column=0)
        self.UltimateButton = self.create_button(self.tab.tab('Config'), text='Assigne', command=lambda: self.start_key_assignment(self.UltimateButton))
        self.UltimateButton.grid(row=3, column=1)

        #BOTconfiguration
        self.amuAndRingLabel = self.create_label(self.tab.tab('BOT'), text="Auto Ring and Amulet:")
        self.amuAndRingLabel.grid(row=0, column=0, sticky="w")
        self.stoneskincheckbox = self.create_checkbox(self.tab.tab('BOT'), text='Stone Skin')
        self.stoneskincheckbox.grid(row=1, column=0, sticky="w", pady=2)
        self.mightringcheckbox = self.create_checkbox(self.tab.tab('BOT'), text='Might Ring')
        self.mightringcheckbox.grid(row=2, column=0, pady=2, sticky="w")
        self.healingLabel = self.create_label(self.tab.tab('BOT'), text="Auto Healing, Mana and Runs:")
        self.healingLabel.grid(row=3, column=0, sticky="w") 
        self.autoHealing = self.create_checkbox(self.tab.tab('BOT'), text='Healing')
        self.autoHealing.grid(row=4, column=0, pady=2, sticky="w")
        self.autoMana = self.create_checkbox(self.tab.tab('BOT'), text='Mana')
        self.autoMana.grid(row=5, column=0, pady=2, sticky="w")
        self.makeRuns = self.create_checkbox(self.tab.tab('BOT'), text='Make runs')
        self.makeRuns.grid(row=4, column=1, pady=2, sticky="w")
        self.startButton = self.create_button(self.tab.tab('BOT'), text='Start', command=self.startButton)
        self.startButton.grid(row=6, column=0, pady=2, padx=5, sticky="e")
        self.stopButton = self.create_button(self.tab.tab('BOT'), text='Stop', state='disabled', command=self.stopButton)
        self.stopButton.grid(row=6, column=1, pady=2, padx=5 )
    
    def create_button(self, parent, text, command=None, state='normal', width=70, height=30):
        return ck.CTkButton(parent, text=text, command=command, state=state, width=width, height=height)
    
    def create_label(self, parent, text, width=100, height=40):
        return ck.CTkLabel(parent, text=text, width=width, height=height)
    
    def create_entry(self, parent,  width=100, height=30):
        return ck.CTkEntry(parent, width=width, height=height)
    
    def create_checkbox(self, parent, text):
        return ck.CTkCheckBox(parent, text=text)

    # Assigne button to key
    def on_assign_key_press(self, event, button):
        print(button.winfo_name())
        assigned_key = event.keysym  # Pobranie nazwy naciśniętego klawisza
        button.configure(text=assigned_key)  # Zmiana tekstu klikniętego przycisku
        app.unbind("<KeyPress>")  # Odłączenie nasłuchiwania klawiatury
        self.logging(f"Key assigned: {assigned_key}")

    # start listening for keyboard
    def start_key_assignment(self, button):
        self.logging("Press key...")
        app.bind("<KeyPress>", lambda event: self.on_assign_key_press(event, button)) 

    def find_and_focus_tibia_window(self):
        #get all open windows
        all_widnows = gw.getAllTitles()
        #find Tibia window
        tibia_title_window = None
        for title in all_widnows:
            if title.startswith('Tibia'):
                tibia_title_window = title
                break
        if tibia_title_window:
            app = Application().connect(title=tibia_title_window)
            window = app[tibia_title_window]
            window.set_focus()
            self.logging(f"Program started")
        else:
            self.logging(f"Canot' find Tibia window")
    
    def logging(self, message):
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d/%m/%Y %H:%M:%S")
        self.logBox.configure(state='normal')
        self.logBox.insert('0.0', f"{self.dt_string} - {message}\n")
        self.logBox.configure(state='disabled')

    def startButton(self):
        self.startButton.configure(state='disabled')
        self.stopButton.configure(state='normal')
        buttonStatuses = [self.mightringcheckbox.get(), self.stoneskincheckbox.get(), self.autoMana.get(), self.makeRuns.get(), self.autoHealing.get()]
        assignedKeyStatus = [self.mightButton.cget('text'), self.ssButton.cget('text'), self.UltimateButton.cget('text'), self.exuraVitaButton.cget('text')] 
        print(assignedKeyStatus)
        obs_instance = AmuletAndRingDetector()
        self.amuRingThread, self.AmuRingStop_event = obs_instance.startAmuAndRingEvent(self, buttonStatuses, assignedKeyStatus)
        self.find_and_focus_tibia_window()

    def stopButton(self):
        self.startButton.configure(state='normal')
        self.stopButton.configure(state='disabled')
        obs_instance = AmuletAndRingDetector()
        obs_instance.stopAmuAndRingEvent(self.AmuRingStop_event, self.amuRingThread)
        self.logging(f"Stopped application")

if __name__ == "__main__":
    app = App()
    app.mainloop()