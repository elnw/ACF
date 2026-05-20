class EventFactory:
    @staticmethod
    def create_event() -> str:
        """
        Creates an event payload.
        According to requirements, the payload must consist exclusively of the string "1".
        """
        return "1"
