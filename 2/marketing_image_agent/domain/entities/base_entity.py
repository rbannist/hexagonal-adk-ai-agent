from abc import ABC
from typing import List, Optional
import uuid
from datetime import datetime

from ..events.base_domain_event import DomainEvent


class Entity(ABC):
    """Base class for all entities in the domain."""

    def __init__(self, id: uuid.UUID = None):
        self.id = id if id is not None else uuid.uuid4()

    def __post_init__(self):
        if not self.id:
            raise ValueError("Entity must have an id.")
        if not isinstance(self.id, uuid.UUID):
            raise ValueError("Entity id must be a UUID.")

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)



class AggregateRoot(Entity, ABC):
    """Base class for all aggregate roots in the domain."""

    def __init__(self, id: uuid.UUID = None):
        super().__init__(id)
        self.events_list: List["DomainEvent"] = []

    def add_domain_event(self, event: "DomainEvent"):
        self.events_list.append(event)

    def pull_all_domain_events(self) -> List["DomainEvent"]:
        """
        Pulls all non-cleared domain events.
        """
        events = self.events_list[:]
        return events

    def pull_and_clear_domain_events(self) -> List["DomainEvent"]:
        """
        Pulls and clears all of the domain events.  This is used when
        persisting changes, to ensure events are dispatched only once.
        """
        events = self.events_list[:]
        self.clear_domain_events()
        return events

    def clear_domain_events(self):
        """
        Clears all domain events (does not pull before or afterwards).
        """
        self.events_list.clear()

    def pull_domain_events_after_time(
        self, occurred_after: datetime
    ) -> List["DomainEvent"]:
        """
        Pulls the domain events that occurred after a specific time (does not clear).
        """
        events = [
            event for event in self.events_list if event.occurredAt > occurred_after
        ]
        return events

    def pull_and_clear_domain_events_after_time(
        self, occurred_after: datetime
    ) -> List["DomainEvent"]:
        """
        Pulls and clears the domain events that occurred after a specific time (assuming event.occurredAt is a datetime).
        """
        events = [
            event for event in self.events_list if event.occurredAt > occurred_after
        ]
        self.events_list = [
            event for event in self.events_list if event.occurredAt <= occurred_after
        ]
        return events

    def pull_latest_domain_event(self) -> Optional[DomainEvent]:
        """
        Pulls the latest domain event (does not clear).
        """
        if not self.events_list:
            return None
        latest_event = max(self.events_list, key=lambda event: event.occurredAt)
        return latest_event

    def pull_and_clear_latest_domain_event(self) -> Optional[DomainEvent]:
        """
        Pulls and clears the latest domain event.
        """
        if not self.events_list:
            return None
        latest_event = max(self.events_list, key=lambda event: event.occurredAt)
        self.events_list.remove(latest_event)
        return latest_event

    def pull_domain_event_by_id(self, event_id: uuid.UUID) -> Optional[DomainEvent]:
        """
        Pulls a specific domain event by its ID (does not clear the event).
        """
        if not self.events_list:
            return None

        for event in self.events_list:
            if event.id == event_id:
                return event
        return None

    def pull_and_clear_domain_event_by_id(
        self, event_id: uuid.UUID
    ) -> Optional[DomainEvent]:
        """
        Pulls and clears a specific domain event by its ID.
        """
        if not self.events_list:
            return None

        for event in self.events_list:
            if event.id == event_id:
                self.events_list.remove(event)
                return event
        return None
