from tapi.utils.types import *
from tapi.http.client import Client
from typing           import List, Any
from .files           import CaseFilesAPI
from .fields          import CaseFieldsAPI
from .inputs          import CaseInputsAPI
from .actions         import CaseActionsAPI
from .linked_cases    import LinkedCasesAPI
from .comments        import CaseCommentsAPI
from .assignees       import CaseAssigneesAPI
from .activities      import CaseActivitiesAPI


class CaseAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "/cases"
        self.files         = CaseFilesAPI(domain, apiKey)
        self.inputs        = CaseInputsAPI(domain, apiKey)
        self.fields        = CaseFieldsAPI(domain, apiKey)
        self.linked_cases  = LinkedCasesAPI(domain, apiKey)
        self.actions       = CaseActionsAPI(domain, apiKey)
        self.comments      = CaseCommentsAPI(domain, apiKey)
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
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key != "self"}
        )

    def get(
            self,
            case_id: int    
        ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}",
            "v2"
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
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key not in ("self", "case_id")}
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
            "v2",
            json = {key: value for key, value in locals().items() if
                    value is not None and key != "self"}
        )

    def delete(
            self,
            case_id: int
        ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}",
            "v2"
        )
