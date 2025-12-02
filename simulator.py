from plotter import Plotter
from singleCompartmentPerOral import SingleCompartmentPerOral
from singleCompartmentIntraVenous import SingleCompartmentintraVenous
from alvailableModels import AvailableModels
from scipy.integrate import solve_ivp
import numpy as np

class Simulator():
    def __init__(self) -> None:
        """setting default values for simulation parameters"""
        self.model = None
        ####
        self.start_t = 0 #h
        self.stop_t = 24 #h
        self.nsteps = 100
        self.D = 1 #mg
        self.Vd = 1 #l
        self.rep_D = False
        self.dose_int = 24 #h
        self.chosen_model = AvailableModels.intraVenousSC
        self.model_params={"k_e":1,"k_a":1}
    
    def init_model(self, type: AvailableModels,**kwargs) -> None:
        """initilizes desired pharmacokinetic model\n
        type: enumeration of available models\n
        kwargs: parameters of chosen model (rate konstants)"""
        if type.value == 1:
            k_e = kwargs.get("k_e",None)
            if k_e == None:
                raise ValueError("Parameter 'k_e' not specified")
            self.model = SingleCompartmentintraVenous(k_e=k_e)
        elif type.value == 2:
            k_e = kwargs.get("k_e",None)
            k_a = kwargs.get("k_a",None)
            if k_e == None:
                raise ValueError("Parameter 'k_e' not specified")
            if k_a == None:
                raise ValueError("Parameter 'k_a' not specified")
            self.model = SingleCompartmentPerOral(k_a=k_a,k_e=k_e)
        else:
            raise ValueError("Unknown pharmacokinetic model: cannot initialize")
        
    def set_parameters(self,**kwargs):
        """setting values for simulation parameters\n
        start_t: start time in hours; int|float\n
        start_t: stop time in hours; int|float\n
        nsteps: number of simulation steps\n
        D: dose in mg; int|float\n
        Vd: volume of distribution in liters; int|float\n
        rep_D: repeated dose; bool\n
        dose_int: time interval between doses in hours; int|float\n
        model_params: parameters for chosen pharmacokinetics model; dictionary\n
        chosen_model: chosen pharmacokinetic model; AvailableModels enumeration"""
        self.start_t = kwargs.get("start_t",self.start_t) #h
        self.stop_t= kwargs.get("stop_t",self.stop_t) #h
        self.nsteps = kwargs.get("nsteps",self.nsteps)
        self.D = kwargs.get("D",self.D) #mg
        self.Vd = kwargs.get("Vd",self.Vd) #l
        self.rep_D = kwargs.get("rep_D",self.rep_D)
        self.dose_int = kwargs.get("dose_int",self.dose_int) #h
        self.model_params=kwargs.get("model_params",self.model_params)
        self.chosen_model = kwargs.get("chosen_model",self.chosen_model)

    def run(self):
        self.init_model(self.chosen_model,k_a=self.model_params)
           #nejak to proiterovat aby to fungovalo 
        if self.rep_D == False:
            ...
        else:
            raise RuntimeError("repetition not implemented so far")


