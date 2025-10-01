from abc import ABC
from typing import Generic, TypeVar


T = TypeVar("T")  # Generic type for commands


class BaseService(ABC, Generic[T]):
    """
    Base class for all application services.  Provides a common abstraction.
    """

    pass


class DrivingSideService(BaseService[T], ABC, Generic[T]):
    """
    Application service called by a driving side infrastructure adapter - e.g. a controller or CLI - via an input port,
    responsible for selecting a command type, creating a command object,
    then sending it to a command dispatcher in the infrastructure layer via an output port.
    This service acts as an entry point to the application core, processing requests from the outside world.
    """

    pass


class CoreService(BaseService[T], ABC, Generic[T]):
    """
    Application service that orchestrates interactions between the domain model and infrastructure concerns.
    It handles commands, queries, and other operations, coordinating data flow and enforcing business rules.
    This service interacts with repositories - i.e. retrieving and saving aggregates -
    and other infrastructure services via output ports - e.g. pushing domain events to a domain event dispatcher.
    """

    pass


class DrivenSideService(BaseService[T], ABC, Generic[T]):
    """
    Application service that interacts with driven-side infrastructure adapters - e.g. message queues, etc. - via output ports.
    It handles domain events or requests originating from the core application and translates them into interactions with external systems.
    This type of service is responsible for handling domain events received from the domain event dispatcher in the infrastructure layer.
    e.g. Triggering another command by pushing a command out to the command dispatcher via an output port,
    translating a domain event into an Integration Event and using a pub-sub pattern, etc.
    """

    pass
