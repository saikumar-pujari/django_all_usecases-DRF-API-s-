from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class loginthrottle(UserRateThrottle):
    scope = 'loginthrottle'

class notloggedinthrottle(AnonRateThrottle):
    scope = 'notloggedin'