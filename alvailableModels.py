from enum import Enum

class AvailableModels(Enum):
    """enumeration of implemented pharmacokinetic models\n
    intraVenousSC: parameters k_e\n
    perOralSC: parameters k_e, k_a"""
    intraVenousSC = 1
    perOralSC = 2