#!/usr/bin/env python
#

from protorpc import messages

class GPSLocation(messages.Message):
    """A GPS location specifier."""
    latitude = messages.FloatField(
        1, variant=messages.Variant.DOUBLE, required=True)
    longitude = messages.FloatField(
        2, variant=messages.Variant.DOUBLE, required=True)
        

class IssueType(messages.Enum):
    """The type of issue reported by passenger."""
    CROWDED = 1
    LATE = 2
    CLEANLINESS = 3
    OTHER = 4


class IncidentType(messages.Enum):
    """The type of incident reported by passenger."""
    TRAFFIC_INCIDENT = 1
    SICK_PASSENGER = 2
    ANTI_SOCIAL_BEHAVIOUR_PASSENGER = 3
    LOST_ITEM = 4
    OTHER = 5
    
class IncidentLevel(messages.Enum):
    """The type of incident reported by passenger."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3