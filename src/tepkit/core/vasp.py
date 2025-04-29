from enum import Enum


class VaspState(str, Enum):
    """
    VASP State Enum.
    """

    Unstarted = "Unstarted"
    Uncompleted = "Uncompleted"
    Finished = "Finished"

    def __bool__(self):
        return self == VaspState.Finished
