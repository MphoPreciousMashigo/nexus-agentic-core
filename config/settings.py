import os
from dataclasses import dataclass

@dataclass(frozen=True)
class CloudIsolationConfig:
    ibm_api_token: str = os.getenv("IBM_WATSONX_API_KEY", "DEMO_SECURE_TOKEN_NODE")
    ibm_project_id: str = os.getenv("IBM_PROJECT_ID", "PROD_PROJECT_NODE_771")
    google_gear_endpoint: str = os.getenv("GEAR_GATEWAY_URL", "https://googleapis.com")
    latency_threshold_ms: float = 40.0

    def verify_auth_integrity(self) -> bool:
        if not self.ibm_api_token or not self.ibm_project_id:
            raise ValueError("[FATAL] Critical cloud credentials missing from host system.")
        return True
