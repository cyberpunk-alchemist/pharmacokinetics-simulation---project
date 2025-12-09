from plotter import Plotter
from singleCompartmentPerOral import SingleCompartmentPerOral
from singleCompartmentIntraVenous import SingleCompartmentintraVenous
from alvailableModels import AvailableModels
import numpy as np
import math

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
        self.plot_title = None
        ####
        self.data={}
        self.run_ID = 1
        self.plotter = Plotter()
    
    def clear_data(self) -> None:
        self.data = {}
        self.run_ID = 1
    
    def init_model(self) -> None:
        """initilizes desired pharmacokinetic model"""
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
        self.plot_title = kwargs.get("plot_title",self.plot_title)

    def run(self):
        init_conds = [self.D,0]
        if self.rep_D == False:
            sol = self.model.solve(self.start_t,self.stop_t,self.nsteps,init_conds) #type: ignore
            self.data.update({f"run{self.run_ID}: t": sol[0]})
            names=[]
            for index,out in enumerate(self.model.name_output): #type: ignore
                names.append(f"{out}") #run{self.run_ID}: 
                self.data.update({names[-1]: sol[index+1]})
                self.plotter.load_data(names[-1],sol[0],sol[index+1])
            self.plotter.plot_data(names,plot_title=self.plot_title)
        else:
            ndoses_float = (self.stop_t - self.start_t)/self.dose_int
            ndoses = math.floor(ndoses_float)
            steps_per_cycle = math.floor(self.nsteps/ndoses_float)
            sol = [np.array([])]
            for index,out in enumerate(self.model.name_output): #type: ignore
                sol.append(np.array([]))

            for i in range(0,ndoses):
                start = self.start_t+i*self.dose_int
                stop = self.start_t+(i+1)*self.dose_int
                sol_part = self.model.solve(start,stop,steps_per_cycle,init_conds) #type: ignore
                sol[0] = np.concatenate((sol[0], sol_part[0]))
                for index,out in enumerate(self.model.name_output): #type: ignore
                    sol[index+1] = np.concatenate((sol[index+1], sol_part[index+1]))
                    init_conds[index] = sol[index+1][-1]
                init_conds[0] = init_conds[0] + self.D
    
            if ndoses_float != ndoses: #remaining simulation time which is not divided
                start = self.start_t+ndoses*self.dose_int
                steps = self.nsteps - steps_per_cycle*ndoses
                sol_part = self.model.solve(start,self.stop_t,steps,init_conds) #type: ignore
                sol[0] = np.concatenate((sol[0], sol_part[0]))
                for index,out in enumerate(self.model.name_output): #type: ignore
                    sol[index+1] = np.concatenate((sol[index+1], sol_part[index+1]))
                    init_conds[index] = sol[index+1][-1]
                init_conds[0] = init_conds[0] + self.D
            
            names=[]
            for index,out in enumerate(self.model.name_output): #type: ignore
                names.append(f"{out}") #run{self.run_ID}: 
                self.data.update({names[-1]: sol[index+1]})
                self.plotter.load_data(names[-1],sol[0],sol[index+1])#type:ignore
            self.plotter.plot_data(names,plot_title=self.plot_title)
            



        self.run_ID +=1

