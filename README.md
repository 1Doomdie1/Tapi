# Tapi (Tines API)
A simple Python wrapper for the Tines API.

## ⚠ Disclaimer 
The library is still under development so major changes and bugs are to be expected. Please feel free to open issues if you encounter any!
## ⚙️Installation 
```bash
git clone https://github.com/1Doomdie1/Tapi.git
```

## 🔄 Usage

### ✨ Using the main `TenantAPI` class
This class provides access to all endpoints offered by the Tines API.

```python
from tapi import TenantAPI

def main():
    tenant = TenantAPI(<DOMAIN>, <API_KEY>)
    teams = tenant.teams.list()
    cases = tenant.cases.list()
    stories = tenant.stories.list()

if __name__ == "__main__":
    main()
```

### 🔧 Using specific endpoint classes
While the main `TenantAPI` class is convenient, using specific endpoint classes may be preferable in certain scenarios. Each class requires `DOMAIN` and `API_KEY` to be passed explicitly.

```python
from tapi import CaseAPI, TeamsAPI, StoriesAPI

def main():
    DOMAIN = "MY_COOL_DOMAIN"
    API_KEY = "DO_NOT_PUT_THIS_ON_GITHUB"

    cases_api = CaseAPI(DOMAIN, API_KEY)
    teams_api = TeamsAPI(DOMAIN, API_KEY)
    stories_api = StoriesAPI(DOMAIN, API_KEY)

if __name__ == "__name__":
    main()
```