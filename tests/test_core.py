import sys
import os
import pytest

# Ensure workspace root anchoring matches runtime protocols
CURRENT_WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CURRENT_WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, CURRENT_WORKSPACE_ROOT)

from config.settings import CloudIsolationConfig
from src.parser import HighVelocityDataCore

def test_cloud_config_initialization():
    """Verifies that the secure environmental registry initializes with safe metrics."""
    config = CloudIsolationConfig()
    assert config.latency_threshold_ms == 40.0
    assert config.verify_auth_integrity() is True

def test_telemetry_parser_valid_schema():
    """Verifies that valid JSON packages convert flawlessly to strongly-typed data capsules."""
    valid_payload = '{"velocity": 150.0, "track_friction": 0.85, "heading_error": 0.02, "lap_index": 1}'
    capsule = HighVelocityDataCore.parse_runtime_packet(valid_payload)
    
    assert capsule is not None
    assert capsule.velocity == 150.0
    assert capsule.lap_index == 1

def test_telemetry_parser_corrupt_schema():
    """Verifies that incomplete configurations are isolated and dropped immediately at the gateway."""
    corrupt_payload = '{"velocity": 120.0, "lap_index": 2}' # Missing friction and heading variables
    capsule = HighVelocityDataCore.parse_runtime_packet(corrupt_payload)
    
    assert capsule is None
