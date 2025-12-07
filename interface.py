import customtkinter as ctk
from simulator import Simulator
from alvailableModels import AvailableModels

class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.simulator= Simulator()
        #####
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        self.title("Pharmacokineticks simulator")
        self.geometry("800x500")
        
        self.label = ctk.CTkLabel(self, text="Availible pharmacokinetic models:")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")


        self.chosen_model = ctk.StringVar(value="IntraVenous")
        self.radio_a = ctk.CTkRadioButton(self, text="Intravenous single compartment model", variable=self.chosen_model, value="IntraVenous")
        self.radio_a.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.radio_b = ctk.CTkRadioButton(self, text="Per oral single compartment model", variable=self.chosen_model, value="PerOral")
        self.radio_b.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label = ctk.CTkLabel(self, text="Simulation parameters:")
        self.label.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")
        
        self.entry_label_1 = ctk.CTkLabel(self, text="Start time [h]:")
        self.entry_label_1.grid(row=3, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_1 = ctk.CTkEntry(self, width=200, placeholder_text=str(self.simulator.start_t))
        self.entry_1.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_2 = ctk.CTkLabel(self, text="Stop time [h]:")
        self.entry_label_2.grid(row=4, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_2 = ctk.CTkEntry(self, width=200, placeholder_text=str(self.simulator.stop_t))
        self.entry_2.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_3 = ctk.CTkLabel(self, text="Number of steps:")
        self.entry_label_3.grid(row=5, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_3 = ctk.CTkEntry(self, width=200, placeholder_text=str(self.simulator.nsteps))
        self.entry_3.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_4 = ctk.CTkLabel(self, text="Initial dose [mg]:")
        self.entry_label_4.grid(row=6, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_4 = ctk.CTkEntry(self, width=200, placeholder_text=str(self.simulator.D))
        self.entry_4.grid(row=6, column=1, padx=10, pady=5, sticky="w") 

        self.entry_label_5 = ctk.CTkLabel(self, text="Volume of distribution [l]:")
        self.entry_label_5.grid(row=7, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_5 = ctk.CTkEntry(self, width=200, placeholder_text=str(self.simulator.Vd))
        self.entry_5.grid(row=7, column=1, padx=10, pady=5, sticky="w") 

        #### rep_ D
        self.cb_option1_var = ctk.BooleanVar(value=self.simulator.rep_D)
        self.entry_label_cb = ctk.CTkLabel(self, text="Repeated dose:")
        self.entry_label_cb.grid(row=8, column=0, padx=10, pady=(15, 0), sticky="w")
        self.cb_option1 = ctk.CTkCheckBox(self, text="", variable=self.cb_option1_var)
        self.cb_option1.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_6 = ctk.CTkLabel(self, text="Time between doses [h]:")
        self.entry_label_6.grid(row=9, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_6 = ctk.CTkEntry(self, width=200, placeholder_text=str(self.simulator.dose_int))
        self.entry_6.grid(row=9, column=1, padx=10, pady=5, sticky="w") 

        # self.label = ctk.CTkLabel(self, text="Model parameters:")
        # self.label.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")


        run_button = ctk.CTkButton(self, text="Run", command=self.run_button_callback)
        run_button.grid(row=10, column=1, padx=20, pady=20)
    
    def run_button_callback(self):
        if self.chosen_model.get() == "IntraVenous":
            self.simulator.set_parameters(chosen_model=AvailableModels.intraVenousSC)
        elif self.chosen_model.get() == "PerOral":
            self.simulator.set_parameters(chosen_model=AvailableModels.perOralSC)
        else:
            raise ValueError("Unknown model")
        
        try:
            self.simulator.set_parameters(
                start_t = float(self.entry_1.get()),
                stop_t= float(self.entry_2.get()),
                nsteps = int(self.entry_3.get()),
                D = float(self.entry_4.get()),
                Vd = float(self.entry_5.get()),
                rep_D=self.cb_option1_var,
                dose_int = float(self.entry_6.get())
            )
        except:
            print("fail")
            #self.error_lable = ctk.CTkLabel(self, text="Error: wrong type of variable entry!")
            #self.error_lable.grid(row=100, column=0, padx=10, pady=(15, 0), sticky="w")
            return



app = Interface()
app.mainloop()
