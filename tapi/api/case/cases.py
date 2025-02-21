from tapi.utils.types     import *
from tapi.api.http.client import Client
from .notes               import CaseNotesAPI
from .files               import CaseFilesAPI
from .fields              import CaseFieldsAPI
from .inputs              import CaseInputsAPI
from .actions             import CaseActionsAPI
from .linked_cases        import LinkedCasesAPI
from .records             import CaseRecordsAPI
from .metadata            import CaseMetadataAPI
from .comments            import CaseCommentsAPI
from .assignees           import CaseAssigneesAPI
from .activities          import CaseActivitiesAPI
from .subscribers         import CaseSubscribersAPI
from typing               import List, Any, Dict, Optional


class CaseAPI(Client):
    def __init__(self, domain, apiKey):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"
        self.files         = CaseFilesAPI(domain, apiKey)
        self.notes         = CaseNotesAPI(domain, apiKey)
        self.inputs        = CaseInputsAPI(domain, apiKey)
        self.fields        = CaseFieldsAPI(domain, apiKey)
        self.linked_cases  = LinkedCasesAPI(domain, apiKey)
        self.actions       = CaseActionsAPI(domain, apiKey)
        self.records       = CaseRecordsAPI(domain, apiKey)
        self.comments      = CaseCommentsAPI(domain, apiKey)
        self.metadata      = CaseMetadataAPI(domain, apiKey)
        self.assignees     = CaseAssigneesAPI(domain, apiKey)
        self.activities    = CaseActivitiesAPI(domain, apiKey)
        self.subscribers   = CaseSubscribersAPI(domain, apiKey)

    def create(
            self,
            team_id:            int,
            name:               str,
            description:        Optional[str]                  = None,
            priority:           Optional[CasePriority]         = CasePriority.LOW,
            status:             Optional[CaseStatus]           = CaseStatus.OPEN,
            sub_status_id:      Optional[int]                  = None,
            author_email:       Optional[str]                  = None,
            assignee_emails:    Optional[List[str]]            = None,
            tag_names:          Optional[List[str]]            = None,
            opened_at:          Optional[str]                  = None,
            resolved_at:        Optional[str]                  = None,
            metadata:           Optional[Dict[str, str]]       = None,
            closure_conditions: Optional[List[Dict[str, Any]]] = None,
            field_values:       Optional[Dict[str, Any]]       = None
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

    def download(
            self,
            case_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/pdf",
            "v2"
        )

    def update(
            self,
            case_id:                int,
            name:                   Optional[str]                  = None,
            team_id:                Optional[int]                  = None,
            description:            Optional[str]                  = None,
            priority:               Optional[CasePriority]         = None,
            status:                 Optional[CaseStatus]           = None,
            sub_status_id:          Optional[int]                  = None,
            author_email:           Optional[str]                  = None,
            assignee_emails:        Optional[List[str]]            = None,
            add_assignee_emails:    Optional[List[str]]            = None,
            remove_assignee_emails: Optional[List[str]]            = None,
            add_tag_names:          Optional[List[str]]            = None,
            remove_tag_names:       Optional[List[str]]            = None,
            opened_at:              Optional[str]                  = None,
            resolved_at:            Optional[str]                  = None,
            closure_conditions:     Optional[List[Dict[str, Any]]] = None
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
            team_id:  Optional[int]             = None,
            filters:  Optional[Dict[str, Any]]  = None,
            order:    Optional[CaseReturnOrder] = None,
            per_page: Optional[int]             = 10,
            page:     Optional[int]             = 1
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
