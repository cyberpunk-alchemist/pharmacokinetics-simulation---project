import customtkinter as ctk
from simulator import Simulator
from alvailableModels import AvailableModels

class Interface(ctk.CTk):
    def __init__(self):
        """initialization of the basic layout"""
        super().__init__()
        self.simulator= Simulator()
        #####
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        self.title("Pharmacokineticks simulator")
        self.geometry("800x500")

        self.label = ctk.CTkLabel(self, text="Pharmacokineticks simulator v1.0",font=("Helvetica",18,"bold"))
        self.label.grid(row=0, column=1, columnspan=3, padx=10, pady=5, sticky="w")
        
        self.scrollable_frame = MyScrollableCheckboxFrame(self)
        self.scrollable_frame.grid(row=1, column=0, padx=(10,10), pady=10, sticky="nsew",columnspan=3)

        button_frame = ctk.CTkFrame(self,width=750,height=50)
        button_frame.grid(row=100, column=0, columnspan=3, padx=10,pady=10, sticky="nsew")

        run_button = ctk.CTkButton(button_frame, text="Run", command=self.run_button_callback)
        run_button.place(relx=0.5, rely=0.5, anchor="center")
        self.error_lable = ctk.CTkLabel(button_frame, text="", text_color="red")
        self.error_lable.place(in_=run_button, relx=1.0, x=10, rely=0.5, anchor="w")

    def run_button_callback(self):
        """callback function for running the simulation"""
        if self.scrollable_frame.chosen_model.get() == "IntraVenous":
            self.simulator.set_parameters(chosen_model=AvailableModels.intraVenousSC)
        elif self.scrollable_frame.chosen_model.get() == "PerOral":
            self.simulator.set_parameters(chosen_model=AvailableModels.perOralSC)
        else:
            raise ValueError("Unknown model")
        
        try:
            self.simulator.set_parameters(
                start_t = float(self.scrollable_frame.entry_1.get()),
                stop_t= float(self.scrollable_frame.entry_2.get()),
                nsteps = int(self.scrollable_frame.entry_3.get()),
                D = float(self.scrollable_frame.entry_4.get()),
                Vd = float(self.scrollable_frame.entry_5.get()),
                rep_D=self.scrollable_frame.cb_option1_var,
                dose_int = float(self.scrollable_frame.entry_6.get())
            )
            self.error_lable.configure(text="")
        except:
            self.error_lable.configure(text="Error: Wrong type of entry!")
            return



class MyScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    def __init__(self,master):
        super().__init__(master,width=750, height=350)
        self.master = master

        self.label = ctk.CTkLabel(self, text="Availible pharmacokinetic models:",font=("Helvetica",14,"bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.chosen_model = ctk.StringVar(value="IntraVenous")
        self.radio_a = ctk.CTkRadioButton(self, text="Intravenous single compartment model", variable=self.chosen_model, value="IntraVenous", command=self.show_intravenous_parameters)
        self.radio_a.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.radio_b = ctk.CTkRadioButton(self, text="Per oral single compartment model", variable=self.chosen_model, value="PerOral", command=self.show_peroral_parameters)
        self.radio_b.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label = ctk.CTkLabel(self, text="Simulation parameters:", font=("Helvetica",14,"bold"))
        self.label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.entry_label_1 = ctk.CTkLabel(self, text="Start time [h]:")
        self.entry_label_1.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_1 = ctk.CTkEntry(self, width=200, placeholder_text="start_t")
        self.entry_1.insert(0,str(self.master.simulator.start_t)) #type: ignore
        self.entry_1.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_2 = ctk.CTkLabel(self, text="Stop time [h]:")
        self.entry_label_2.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_2 = ctk.CTkEntry(self, width=200, placeholder_text="stop_t")
        self.entry_2.insert(0,str(self.master.simulator.stop_t)) #type: ignore
        self.entry_2.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_3 = ctk.CTkLabel(self, text="Number of steps:")
        self.entry_label_3.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.entry_3 = ctk.CTkEntry(self, width=200, placeholder_text="nsteps")
        self.entry_3.insert(0,str(self.master.simulator.nsteps))#type: ignore
        self.entry_3.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_4 = ctk.CTkLabel(self, text="Initial dose [mg]:")
        self.entry_label_4.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.entry_4 = ctk.CTkEntry(self, width=200, placeholder_text="D")
        self.entry_4.insert(0,str(self.master.simulator.D)) #type: ignore
        self.entry_4.grid(row=6, column=1, padx=10, pady=5, sticky="w") 

        self.entry_label_5 = ctk.CTkLabel(self, text="Volume of distribution [l]:")
        self.entry_label_5.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.entry_5 = ctk.CTkEntry(self, width=200, placeholder_text="Vd")
        self.entry_5.insert(0,str(self.master.simulator.Vd))#type: ignore
        self.entry_5.grid(row=7, column=1, padx=10, pady=5, sticky="w") 

        #### rep_ D
        self.cb_option1_var = ctk.BooleanVar(value=self.master.simulator.rep_D) #type: ignore
        self.entry_label_cb = ctk.CTkLabel(self, text="Repeated dose:")
        self.entry_label_cb.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.cb_option1 = ctk.CTkCheckBox(self, text="", variable=self.cb_option1_var,command=self.show_hide_rep_dose)
        self.cb_option1.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.entry_label_6 = ctk.CTkLabel(self, text="Time between doses [h]:")
        self.entry_label_6.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.entry_6 = ctk.CTkEntry(self, width=200, placeholder_text="dose_int")
        self.entry_6.insert(0,str(self.master.simulator.dose_int)) #type: ignore
        self.entry_6.grid(row=9, column=1, padx=10, pady=5, sticky="w") 

        self.label = ctk.CTkLabel(self, text="Model parameters:", font=("Helvetica",14,"bold"))
        self.label.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.entry_label_7 = ctk.CTkLabel(self, text="Rate constant of elimination [1/h]:")
        self.entry_label_7.grid(row=11, column=0, padx=10, pady=5, sticky="w")
        self.entry_7 = ctk.CTkEntry(self, width=200, placeholder_text="k_a")
        self.entry_7.insert(0,str(self.master.simulator.model_params["k_e"])) #type: ignore
        self.entry_7.grid(row=11, column=1, padx=10, pady=5, sticky="w") 

        self.entry_label_8 = ctk.CTkLabel(self, text="Rate constant of absorption [1/h]:")
        self.entry_label_8.grid(row=12, column=0, padx=10, pady=5, sticky="w")
        self.entry_8 = ctk.CTkEntry(self, width=200, placeholder_text="k_a")
        self.entry_8.insert(0,str(self.master.simulator.model_params["k_a"])) #type: ignore
        self.entry_8.grid(row=12, column=1, padx=10, pady=5, sticky="w") 
        
        self.remove_params()
        self.entry_label_6.grid_remove()
        self.entry_6.grid_remove()
        self.entry_label_7.grid()
        self.entry_7.grid()

    def remove_params(self):
        self.entry_7.grid_remove()
        self.entry_label_7.grid_remove()
        self.entry_8.grid_remove()
        self.entry_label_8.grid_remove()

    def show_intravenous_parameters(self):
        """callback function for showing right parameters for intra venous single compartment model"""
        self.remove_params()
        self.entry_7.grid()
        self.entry_label_7.grid()
    
    def show_peroral_parameters(self):
        """callback function for showing right parameters for per orals single compartment model"""
        self.remove_params()
        self.entry_7.grid()
        self.entry_label_7.grid()
        self.entry_8.grid()
        self.entry_label_8.grid()

    def show_hide_rep_dose(self):
        """callback function for showing/hiding time between doses parameter for repeated dose option"""
        if self.cb_option1_var.get():
            self.entry_6.grid()
            self.entry_label_6.grid()
        else:
            self.entry_6.grid_remove()
            self.entry_label_6.grid_remove()



app = Interface()
app.mainloop()
