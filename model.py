from abc import ABC, abstractmethod


class Model(ABC): #abstract class
    def __init__(self) -> None:
        self.name_output = ...

    @abstractmethod 
    def rhs(self,t):
        """right hand side(s) of ODE(s system) dy/dt = f(t,y(t))"""
        pass
    
    @abstractmethod
    def solve():
        """finds numerical solution for desired system\n
        allways put the initial conditions as a tuple with 'Dose' as the first one"""
        pass