from plotter import Plotter
from singleCompartmentPerOral import SingleCompartmentPerOral
from singleCompartmentIntraVenous import SingleCompartmentintraVenous
from alvailableModels import AvailableModels
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
        ####
        self.data={}
        self.run_ID = 1
        self.plotter = Plotter()
    
    def clear_data(self) -> None:
        self.data = {}
        self.run_ID = 1
    
    def init_model(self) -> None:
        """initilizes desired pharmacokinetic model\n
        type: enumeration of available models\n
        parameters: parameters of chosen model (rate konstants) as a dictionary"""
        if self.chosen_model == AvailableModels.intraVenousSC:
            self.model = SingleCompartmentintraVenous(parameters=self.model_params) # type: ignore
        elif self.chosen_model == AvailableModels.perOralSC:
            self.model = SingleCompartmentPerOral(parameters=self.model_params) # type: ignore
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
        init_conds = (self.D,0)
        if self.rep_D == False:
            sol = self.model.solve(self.start_t,self.stop_t,self.nsteps,init_conds) #type: ignore
            self.data.update({f"run{self.run_ID}: t": sol[0]})
            names=[]
            for index,out in enumerate(self.model.name_output): #type: ignore
                names.append(f"run{self.run_ID}: {out}")
                self.data.update({names[-1]: sol[index+1]})
                self.plotter.load_data(names[-1],sol[0],sol[index+1])
            self.plotter.plot_data(names)
        else:
            raise RuntimeError("repetition not implemented so far")
            # chce to doimplementovat
        self.run_ID +=1


