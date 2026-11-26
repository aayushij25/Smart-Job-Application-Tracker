class AIError(Exception):
    """Base class for anything that goes wrong in the AI layer."""


class AIServiceError(AIError):
    """The provider could not be reached, refused the request, or is rate limited."""


class AIOutputError(AIError):
    """The provider answered, but not in a usable format."""