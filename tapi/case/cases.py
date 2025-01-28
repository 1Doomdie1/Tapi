from utils.types import *
from .client     import Client
from typing      import List, Any

class CasesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"
        self.inputs        = CaseInputsAPI(domain, apiKey)
        self.actions       = CaseActionsAPI(domain, apiKey)
        self.assignees     = CaseAssigneesAPI(domain, apiKey)
        self.activities    = CaseActivitiesAPI(domain, apiKey)

    def create(
            self,
            team_id:            int,
            name:               str,
            description:        str          | None = None,
            priority:           CasePriority | None = CasePriority.LOW,
            status:             CaseStatus   | None = CaseStatus.OPEN,
            sub_status_id:      int          | None = None,
            author_email:       str          | None = None,
            assignee_emails:    List[str]    | None = None,
            tag_names:          List[str]    | None = None,
            opened_at:          str          | None = None,
            resolved_at:        str          | None = None,
            metadata:           dict         | None = None,
            closure_conditions: List[dict]   | None = None,
            field_values:       dict         | None = None
        ):
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value != None and key != "self"}
        )

    def get(
            self,
            case_id: int    
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}"
        )

    def update(
            self,
            case_id:                int,
            name:                   str          | None = None,
            team_id:                int          | None = None,
            description:            str          | None = None,
            priority:               CasePriority | None = None,
            status:                 CaseStatus   | None = None,
            sub_status_id:          int          | None = None,
            author_email:           str          | None = None,
            assignee_emails:        List[str]    | None = None,
            add_assignee_emails:    List[str]    | None = None,
            remove_assignee_emails: List[str]    | None = None,
            add_tag_names:          List[str]    | None = None,
            remove_tag_names:       List[str]    | None = None,
            opened_at:              str          | None = None,
            resolved_at:            str          | None = None,
            closure_conditions:     List[dict]   | None = None
        ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )

    def list(
            self,
            team_id:  int             | None = None,
            filters:  dict[str, Any]  | None = None,
            order:    CaseReturnOrder | None = None,
            per_page: int                    = 10,
            page:     int                    = 1
        ):
        return self._http_request(
            "GET",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value != None and key != "self"}
        )

    def delete(
            self,
            case_id: int
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )


class CaseActionsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"

    def create(
            self,
            case_id:     int,
            url:         str,
            label:       str,
            action_type: CaseActionType,
            action_text: str | None = None
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/actions",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )
    
    def get(
            self,
            case_id: int,
            id:      int
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/actions/{id}"
        )
    
    def update(
            self,
            case_id:     int,
            id:          int,
            url:         str            | None = None,
            label:       str            | None = None,
            action_type: CaseActionType | None = None,
            action_text: str            | None = None
        ):
        return self._http_request(
            "PUT",
            f"{self.base_endpoint}/{case_id}/actions/{id}",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id", "id")}
        )
    
    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1,
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/actions",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )
    
    def delete(
            self,
            case_id:  int,
            id:       int = 10
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/actions/{id}"
        )
    
    def batch_delete(
            self,
            case_id: int,
            actions: List[dict[str, str]]
        ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/actions/batch",
            json = {"actions": actions}
        )

class CaseActivitiesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"
    
    def get(
            self,
            case_id:     int,
            activity_id: int    
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/activities/{activity_id}"
        )
    
    def list(
            self,
            case_id:        int,
            activity_type:  CaseActivityType | None = None,
            per_page:       int                     = 10,
            page:           int                     = 1
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/activities",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )

class CaseAssigneesAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"
    
    def list(
            self,
            case_id: int,
            per_page: int = 10,
            page: int = 1,
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/assignees",
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )

class CaseInputsAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases_inputs"
    
    def create(
            self,
            name:               str,
            input_type:         CaseInputType,
            team_id:            int,
            validation_type:    CaseValidationType   | None                  = None,
            validation_options: dict[str, List[str]] | dict[str, str] | None = None
        ):
        # I have to actually build the data object here I can't just parse it by using the same trick.
        return self._http_request(
            "POST",
            self.base_endpoint,
            json = {key: value for key, value in locals().items() if value != None and key not in ("self", "case_id")}
        )