from .teams   import TeamsAPI
from .cases   import CasesAPI
from .tenant  import TenantAPI
from .stories import StoriesAPI

class TinesAPI:
    def __init__(self, domain: str, apiKey: str) -> None:
        self.tenant = TenantAPI(domain, apiKey)
        self.stories = StoriesAPI(domain, apiKey)
        self.teams = TeamsAPI(domain, apiKey)
        self.cases = CasesAPI(domain, apiKey)
