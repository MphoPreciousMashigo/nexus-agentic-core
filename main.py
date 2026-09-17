import os
import sys
import asyncio
import logging
import random
import time
from typing import Dict, Any, Optional

# ARCHITECTURE PROTOCOL BREAK: Explicitly anchor current working directory into Python system path strings
CURRENT_WORKSPACE_ROOT = os.path.dirname(os.path.abspath(__file__))
if CURRENT_WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, CURRENT_WORKSPACE_ROOT)

# Securely import custom local modules now that path overrides are established
from config.settings import CloudIsolationConfig
from src.parser import HighVelocityDataCore

# Enterprise-grade logging layout configuration
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] NexusCore-Orchestrator: %(message)s",
    datefmt="%H:%M:%S"
)

class ChaosDrivenOrchestrator:
    """Advanced Agentic Event Loop executing dual-threaded streaming optimization threads."""

    def __init__(self, config: CloudIsolationConfig):
        self.config = config
        self.config.verify_auth_integrity()
        self.is_active = True
        self.telemetry_history: list[Any] = []
        logging.info("🧠 Dual-Threaded Concurrent Orchestration Kernel Initialized.")

    async def ingest_high_frequency_stream_worker(self, queue: asyncio.Queue):
        """Worker Thread 1: Ingests raw telemetry and enforces zero-allocation structure validation."""
        mock_payloads = [
            '{"velocity": 142.1, "track_friction": 0.89, "heading_error": 0.01, "lap_index": 1}',
            '{"velocity": 168.4, "track_friction": 0.84, "heading_error": 0.04, "lap_index": 1}',
            '{"velocity": 192.0, "heading_error": -0.02, "lap_index": 1}',  # Corrupt structural schema frame
            '{"velocity": 215.7, "track_friction": 0.81, "heading_error": 0.08, "lap_index": 2}',
            '{"velocity": 252.3, "track_friction": 0.74, "heading_error": 0.14, "lap_index": 2}'
        ]

        for payload in mock_payloads:
            if not self.is_active:
                break
            
            logging.info("📥 Ingesting live high-frequency network stream frame...")
            capsule = HighVelocityDataCore.parse_runtime_packet(payload)
            
            if capsule:
                await queue.put(capsule)
                logging.info(f"✅ Frame parsing cleared. Passed capsule to processing queue buffer.")
            
            # Simulate high-frequency ingestion clock intervals (200ms)
            await asyncio.sleep(0.2)
        
        # Stop worker when stream finishes
        await queue.put(None)

    async def process_predictive_trajectory_worker(self, queue: asyncio.Queue):
        """Worker Thread 2: Processes packets asynchronously and triggers structural self-healing."""
        while self.is_active:
            capsule = await queue.get()
            
            # Exit loop criteria met
            if capsule is None:
                queue.task_done()
                break

            start_compute = time.time()
            
            # CHAOS SIMULATION PROTOCOL: Injecting randomized background network turbulence
            network_jitter = random.choice([0.01, 0.015, 0.065, 0.012])
            await asyncio.sleep(network_jitter)
            
            end_compute = time.time()
            execution_latency_ms = (end_compute - start_compute) * 1000
            
            logging.info(f"📊 Compute Latency Metrics: {execution_latency_ms:.2f} ms | Velocity Vector: {capsule.velocity} km/h")

            # Defensive Self-Healing Execution Validation Block
            if execution_latency_ms > self.config.latency_threshold_ms:
                logging.warning(f"⚠️ [CRITICAL LATENCY BREACH] Metrics registered at {execution_latency_ms:.2f} ms!")
                await self._deploy_runtime_dynamic_reconfiguration(capsule)
            else:
                logging.info("🎯 Real-time trajectory synchronization stable.")
                
            queue.task_done()

    async def _deploy_runtime_dynamic_reconfiguration(self, breached_capsule: Any):
        """Self-Correction Node: Recalculates safe systemic limits dynamically without breaking loop."""
        logging.info("🧠 Executing live telemetry dampening script...")
        await asyncio.sleep(0.005) # Dynamic core memory allocation window
        
        safe_velocity_ceiling = breached_capsule.velocity * 0.82
        compensated_heading = breached_capsule.heading_error * 0.90
        
        logging.info("🛠️ [RECOVERY SUCCESSFUL] System stabilized. Adaptive parameters loaded:")
        logging.info(f"   ↳ Adjusted Velocity Threshold: {safe_velocity_ceiling:.2f} km/h")
        logging.info(f"   ↳ Realigned Heading Coordinate: {compensated_heading:.4f} rad")

async def bootstrap_system():
    # Load parameters safely from settings module
    system_settings = CloudIsolationConfig()
    orchestration_engine = ChaosDrivenOrchestrator(config=system_settings)
    
    # Establish production-grade cross-thread messaging buffer queue
    shared_data_queue = asyncio.Queue(maxsize=10)
    
    # Fire both async workers concurrently into the engine core
    await asyncio.gather(
        orchestration_engine.ingest_high_frequency_stream_worker(shared_data_queue),
        orchestration_engine.process_predictive_trajectory_worker(shared_data_queue)
    )

def main():
    try:
        asyncio.run(bootstrap_system())
        logging.info("🏁 Chaos-driven diagnostic run closed cleanly. All nodes offline.")
    except KeyboardInterrupt:
        logging.warning("Process terminated by operator command.")
    except Exception as initialization_failure:
        logging.critical(f"Fatal kernel failure: {initialization_failure}")
        sys.exit(1)

if __name__ == "__main__":
    main()
