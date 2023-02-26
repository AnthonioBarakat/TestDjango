from rest_framework.throttling import UserRateThrottle 

class TenCallsPerMinute(UserRateThrottle):
    scope = 'ten' # this will be used in settings.py
