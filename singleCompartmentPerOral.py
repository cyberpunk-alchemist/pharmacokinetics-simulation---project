from model import Model
from scipy.integrate import solve_ivp
import numpy as np


class SingleCompartmentPerOral(Model):
    """single compartment model of per oral drug administration, first order kinetics assumed\n
    Ag: ammount of medication in gastrointestinal compartment\n
    Ac: ammount of medication in central compartment\n
    Parameters required: \n
    k_a: rate constant of absorption\n
    k_e: rate constant of elimination\n
    enter parameters as dictionary, {"k_a": value, "k_e": value}"""
    def __init__(self,parameters: dict[str,float|int]) -> None:
        super().__init__()
        self.k_a = parameters["k_a"]
        self.k_e = parameters["k_e"]
        self.n_output = 3

    def rhs(self,t,A: tuple) -> tuple:
        """returns the right hand sides of ODEs system describing this model\n
        A is a touple of (Ag, Ac) (see class description)\n
        output = [dAg/dt,dAc/dt]"""
        Ag, Ac = A
        dAgdt = -self.k_a*Ag
        dAcdt = self.k_a*Ag-self.k_e*Ac
        return (dAgdt,dAcdt)
    
    def solve(self,start_t:float|int,stop_t:float|int,nsteps,A_g_init:float|int,A_c_init:float|int) -> tuple:
        """finds numerical solution for self.rhs system, returns tuple (solution.t, solution.A), A(t)\n
        start_t: initial time in hours\n
        stop_t: end time in hours\n
        nsteps: number of steps\n
        A_c_init: initial drug ammount in central compartment in mg\n
        A_g_init: initial drug ammount in gastrointestinal compartment in mg (=initial dose)"""
        t_eval = np.linspace(start_t, stop_t, nsteps)
        sol = solve_ivp(
            self.rhs,
            (start_t, stop_t),
            (A_g_init,A_c_init),
            t_eval=t_eval,
            method='RK45',
            rtol=1e-8,
            atol=1e-10
        )
        return (sol.x, sol.y[0], sol.y[1])