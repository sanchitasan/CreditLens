import httpx


class CreditLensAPIClient:
    """
    HTTP client for communicating with the CreditLens FastAPI backend.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ):
        self.base_url = base_url.rstrip("/")

    def create_application(
        self,
        payload: dict,
    ) -> dict:
        response = httpx.post(
            f"{self.base_url}/applications",
            json=payload,
            timeout=120.0,
        )

        response.raise_for_status()

        return response.json()

    def get_application(
        self,
        application_id: int,
    ) -> dict:
        response = httpx.get(
            f"{self.base_url}/applications/{application_id}",
        )

        response.raise_for_status()

        return response.json()

    def list_applications(
        self,
        skip: int = 0,
        limit: int = 100,
        risk_level: str | None = None,
        decision: str | None = None,
    ) -> list[dict]:

        params = {
            "skip": skip,
            "limit": limit,
        }

        if risk_level is not None:
            params["risk_level"] = risk_level

        if decision is not None:
            params["decision"] = decision

        response = httpx.get(
            f"{self.base_url}/applications",
            params=params,
        )

        response.raise_for_status()

        return response.json()