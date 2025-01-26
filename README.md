# Tapi (Tines API)
A simple Python wrapper for the Tines API.

## ⚠ Disclaimer 
Although the wrapper includes support for multiple endpoints, due to limited access to only a community tenant, I am unable to test all methods to ensure correct implementation. Contributions in the form of pull requests (PRs) are highly encouraged and appreciated!

## ⚙️Installation 
```bash
git clone https://github.com/1Doomdie1/Tapi.git
```

## 🔄 Usage

### ✨ Using the main `TinesAPI` class
This class provides access to all endpoints offered by the Tines API.

```python
from api.tines import TinesAPI

def main():
    tines   = TinesAPI(<DOMAIN>, <API_KEY>)
    tenant  = tines.tenant.info()
    cases   = tines.cases.list()
    stories = tines.stories.list()

if __name__ == "__main__":
    main()
```

### 🔧 Using specific endpoint classes
While the main `TinesAPI` class is convenient, using specific endpoint classes may be preferable in certain scenarios. Each class requires `DOMAIN` and `API_KEY` to be passed explicitly.

```python
from api.cases  import CasesAPI
from api.teams  import TeamsAPI
from api.tenant import TenantAPI

def main():
    DOMAIN  = "MY_COOL_DOMAIN"
    API_KEY = "DO_NOT_PUT_THIS_ON_GITHUB"

    cases_api  = CasesAPI(DOMAIN, API_KEY)
    teams_api  = TeamsAPI(DOMAIN, API_KEY)
    tenant_api = TenantAPI(DOMAIN, API_KEY)

if __name__ == "__name__":
    main()
```