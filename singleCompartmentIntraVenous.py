from model import Model
from scipy.integrate import solve_ivp
import numpy as np

class SingleCompartmentintraVenous(Model):
    """single compartment model of per oral drug administration, first order kinetics assumed\n
    Ac: ammount of medication in central compartment\n
    Parameters required: \n
    k_e: rate constant of elimination\n
    enter parameters as dictionary, {"k_e": value}"""
    def __init__(self, parameters: dict[str,float|int]) -> None:
        super().__init__()
        self.k_e = parameters["k_e"]
        self.name_output = (["Concentration in central compartment"])

    def rhs(self,t,Ac:float|int) -> float|int:
        """returns the right hand sides of ODE describing this model\n
        output = dAc/dt"""
        dAcdt = -self.k_e*Ac
        return dAcdt
    
    def solve(self,start_t:float|int,stop_t:float|int,nsteps:int,init_conds:tuple[float|int]) -> tuple:
        """finds numerical solution for self.rhs system, returns tuple (solution.t, solution.A), A(t)\n
        start_t: initial time in hours\n
        stop_t: end time in hours\n
        nsteps: number of steps\n
        init_conds: initial conditions for the simulation as a tuple, for this model = (A_c_init)\n
        A_c_init: initial drug ammount in central compartment in mg(=dose)"""
        t_eval = np.linspace(start_t, stop_t, nsteps)
        sol = solve_ivp(
            self.rhs,
            (start_t, stop_t),
            [init_conds[0]],
            t_eval=t_eval,
            method='RK45',
            rtol=1e-8,
            atol=1e-10
        )
        return (sol.t, sol.y[0])