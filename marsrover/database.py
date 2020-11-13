from abc import ABC, abstractmethod

from .models import Rover


class RoverRepo(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_rover_by_name(self, rover_name: str, *args, **kwargs) -> 'Rover':
        pass

    @abstractmethod
    def register_new_rover(self, rover_name: str, new_rover_obj: Rover, *args,
                           **kwargs):
        pass

    @abstractmethod
    def report_all_rovers(self):
        pass


class RoverMemoryRepo(RoverRepo):
    def __init__(self):
        super().__init__()
        self.rover_registry = {}

    def get_rover_by_name(self, rover_name: str, *args, **kwargs) -> 'Rover':
        """Fetches a rover from registry by its name

        Args:
            rover_name (str): Name of the to look for from registry

        Returns:
            Rover: Rover object with provided name,
            None if the provided name cannot be found
        """
        return self.rover_registry.get(rover_name)

    def register_new_rover(self, rover_name: str, new_rover_obj: Rover, *args,
                           **kwargs):
        """Registers a new rover into registry.
        It will overwrite if an existing name is
        provided.

        Args:
            rover_name (str): Name of the new rover, will be used
            as ID (key) in registry
            rover_obj (Rover): New rover obj reference
        """
        self.rover_registry[rover_name] = new_rover_obj

    def report_all_rovers(self):
        """Reports status of all registered rovers.
        """
        for rover in self.rover_registry.values():
            print(rover.report_status())
