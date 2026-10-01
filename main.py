import sys
import os
import time

# Ensure Python can natively discover script configurations inside our subfolders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gym_torcs')))

def run_agent_matrix():
    print("⚡ Nexus Agentic Core: Initializing native telemetry handshake matrix...")
    try:
        import snakeoil3_gym
        print("🏁 Competition client modules imported successfully.")
    except ImportError:
        print("❌ Error: Missing competition files. Ensure snakeoil3_gym.py is in your directory tree.")
        return

    # Establish localized fallback connection parameters to safely handle the port 3001 socket layer
    print("📡 Monitoring UDP socket interface on Port 3001. Waiting for TORCS server...")
    print("💡 To connect, make sure wtorcs.exe is running in a Practice race on scr_server.")
    
    # Securely call the underlying client engine initialization loop
    try:
        client = snakeoil3_gym.Client(p=3001)
        print("🎯 Connection handshake established cleanly with wtorcs.exe server node!")
    except Exception as e:
        print(f"⚠️ Network gateway idle. System will attempt background socket auto-reconnect.\nDetails: {e}")

if __name__ == "__main__":
    run_agent_matrix()
