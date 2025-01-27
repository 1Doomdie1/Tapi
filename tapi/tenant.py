from .client  import Client
from .teams   import TeamsAPI
from .cases   import CasesAPI
from .stories import StoriesAPI


class TenantAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.stories = StoriesAPI(domain, apiKey)
        self.teams = TeamsAPI(domain, apiKey)
        self.cases = CasesAPI(domain, apiKey)

    def info(self) -> dict:
        return self._http_request("GET", "/info")