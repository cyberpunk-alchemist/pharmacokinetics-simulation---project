import matplotlib.pyplot as plt
from typing import List
import matplotlib.image as mpimg

class Plotter():
    def __init__(self):
        self.xs = {}
        self.ys = {}
        self.fig = None
        self.ax = None

    def load_data(self, name: str, x: List[int]|List[float]|List[float|int], y: List[int]|List[float]|List[float|int]) -> None:
        """loads data into memory, stores as dictionary wth name as a key """
        if len(x) != len(y):
            raise ValueError("list of data x and their dependent value list y must have the same length")
        else:
            self.xs[name] = x
            self.ys[name] = y

    def close_plot(self) -> None:
        """closes matplotlib window"""
        plt.close(self.fig)
        self.fig = None
        self.ax = None

    def plot_data(self,name: str|List[str], **kwargs) -> None:
        """opens the matplotlib window, plots data set from memory with name as a key
        name: string or list of strings if multiple datasets shall be plotted"""
        plot_title = kwargs.get("plot_title",None)
        self.fig, self.ax = plt.subplots()
        ####
        if plot_title == "fox":
                img = mpimg.imread("do_not_open.png")
                self.ax.imshow(img)
                self.ax.axis("off")
                plt.show()
                return
        ###
        self.ax.set_xlabel("t [h]")
        self.ax.set_ylabel("c(t) [mg/l]")
        #self.ax.set_title("Title of the graph")
        if isinstance(name,str):
            self.ax.plot(self.xs[name], self.ys[name], label=name)
        elif isinstance(name,list):
            for name_ in name:
                self.ax.plot(self.xs[name_], self.ys[name_], label=name_)
        else:
            raise ValueError("parameter name shall only be string or list of strings")
        self.ax.legend()
        if plot_title != None:
            self.ax.set_title(plot_title)
        plt.show()

    def remove_data(self, name: str) -> None:
        """removes data from memory"""
        self.xs.pop(name)
        self.ys.pop(name)
