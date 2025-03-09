from tapi.client import Client


class RecordArtifactsAPI(Client):
    def __init__(self, domain: str, apiKey: str):
        super().__init__(domain, apiKey)
        self.base_endpoint = "records"

    def get(
            self,
            record_id:   int,
            artifact_id: int
    ):
        return self._http_request(
            "GET",
            f"{self.base_endpoint}/{record_id}/artifacts/{artifact_id}"
        )
