import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class TelemetryDataCapsule:
    velocity: float
    track_friction: float
    heading_error: float
    lap_index: int

class HighVelocityDataCore:
    @staticmethod
    def parse_runtime_packet(raw_payload: str) -> Optional[TelemetryDataCapsule]:
        try:
            parsed_json: Dict[str, Any] = json.loads(raw_payload)
            required_metrics = {"velocity", "track_friction", "heading_error", "lap_index"}
            if not required_metrics.issubset(parsed_json.keys()):
                missing_keys = required_metrics - parsed_json.keys()
                raise KeyError(f"Payload corrupted. Missing parameters: {missing_keys}")
                
            return TelemetryDataCapsule(
                velocity=float(parsed_json["velocity"]),
                track_friction=float(parsed_json["track_friction"]),
                heading_error=float(parsed_json["heading_error"]),
                lap_index=int(parsed_json["lap_index"])
            )
        except (json.JSONDecodeError, KeyError, TypeError) as parser_exception:
            logging.error(f"? [GATEWAY BLOCK] Corrupt stream isolated and dropped: {parser_exception}")
            return None
