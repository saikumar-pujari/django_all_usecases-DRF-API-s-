class four_int:
    regex='[0-9]{4}'
    to_python=lambda self, value: int(value)
    to_url=lambda self, value: str(value)

class uuids:
    regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    to_python = lambda self, value: value
    to_url = lambda self, value: str(value)