from abc import ABC


class DomainService(ABC):
    """
    Base class for domain services.
    Domain services encapsulate domain logic that doesn't naturally fit within
    an entity or value object.  They often involve interactions between multiple
    domain objects.
    """
