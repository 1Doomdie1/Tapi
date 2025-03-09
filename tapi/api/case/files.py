from tapi.client import Client
from typing      import Optional


class CaseFilesAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "cases"

    def create(
            self,
            case_id:       int,
            filename:      str,
            file_contents: str,
            value:         Optional[str] = None,
            author_email:  Optional[str] = None,

    ):
        return self._http_request(
            "POST",
            f"{self.base_endpoint}/{case_id}/files",
            "v2",
            json = {
                "filename": filename,
                "file_contents": file_contents,
                "value": value,
                "author_email": author_email
            }
        )

    def get(
            self,
            case_id: int,
            file_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/files/{file_id}",
            "v2"
        )

    def list(
            self,
            case_id:  int,
            per_page: int = 10,
            page:     int = 1
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/files",
            "v2",
            params = {"per_page": per_page, "page": page}
        )

    def delete(
            self,
            case_id: int,
            file_id: int
    ):
        return self._http_request(
            "DELETE",
            f"{self.base_endpoint}/{case_id}/files/{file_id}",
            "v2"
        )

    def download(
            self,
            case_id: int,
            file_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{case_id}/files/{file_id}/download",
            "v2"
        )
