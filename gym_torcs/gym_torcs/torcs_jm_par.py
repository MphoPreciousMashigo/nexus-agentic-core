#!/usr/bin/env python3
import sys
import os
import math
import time
import socket

TARGET_SPEED_STRAIGHT = 175.0  
TARGET_SPEED_CORNER = 78.0     
KP_STEERING = 0.46             
KD_STEERING = 0.16             
BRAKE_MAX_GAIN = 0.80          

def clip(v, low, high):
    return max(low, min(v, high))

class CarState:
    def __init__(self, data_bytes):
        self.matrix = {}
        self.parse_telemetry(data_bytes)
        
    def parse_telemetry(self, data_bytes):
        try:
            raw_string = data_bytes.decode('utf-8').strip()
            elements = raw_string.strip('()').split(')(')
            for element in elements:
                parts = element.split()
                if not parts:
                    continue
                key = parts[0]
                if len(parts) == 2:
                    try:
                        self.matrix[key] = float(parts[1])
                    except ValueError:
                        self.matrix[key] = parts[1]
                elif len(parts) > 2:
                    self.matrix[key] = [float(x) for x in parts[1:]]
        except Exception:
            pass

    def get(self, key, default=None):
        return self.matrix.get(key, default)

def drive_control(carState_obj, memory):
    command = {'steer': 0.0, 'accelerate': 0.0, 'brake': 0.0, 'gear': 1}
    track_pos = carState_obj.get('trackPos', 0.0)
    angle = carState_obj.get('angle', 0.0)
    speed_x_ms = carState_obj.get('speedX', 0.0)       
    speed_kmh = abs(speed_x_ms) * 3.6                  
    track_sensors = carState_obj.get('track', [40.0] * 19)

    try:
        current_error = track_pos - angle
        derivative = current_error - memory.get('last_error', 0.0)
        memory['last_error'] = current_error
        raw_steer = (current_error * KP_STEERING) + (derivative * KD_STEERING)
        
        if speed_kmh < 15.0:
            command['steer'] = clip(raw_steer * 0.05, -0.1, 0.1)
        else:
            command['steer'] = clip(raw_steer, -1.0, 1.0)
    except Exception:
        command['steer'] = 0.0

    try:
        center_vision = track_sensors[9] if len(track_sensors) > 9 else 40.0
        left_vision = track_sensors[6] if len(track_sensors) > 6 else 40.0
        right_vision = track_sensors[12] if len(track_sensors) > 12 else 40.0
        shortest_path = min(center_vision, left_vision, right_vision)
        
        if shortest_path < 65.0:
            speed_scale = clip(shortest_path / 65.0, 0.0, 1.0)
            target_speed = TARGET_SPEED_CORNER + (speed_scale * (TARGET_SPEED_STRAIGHT - TARGET_SPEED_CORNER))
            brake_intensity = clip((65.0 - shortest_path) / 65.0, 0.1, BRAKE_MAX_GAIN)
        else:
            target_speed = TARGET_SPEED_STRAIGHT
            brake_intensity = 0.0
    except Exception:
        target_speed = TARGET_SPEED_CORNER
        brake_intensity = 0.0

    if speed_kmh < target_speed:
        if speed_kmh < 25.0:
            command['accelerate'] = 0.25  
        else:
            command['accelerate'] = clip(0.3 + (target_speed - speed_kmh) / 30.0, 0.1, 1.0)
        command['brake'] = 0.0
    else:
        command['accelerate'] = 0.0
        command['brake'] = clip(brake_intensity, 0.0, 0.9)

    try:
        current_gear = int(carState_obj.get('gear', 1))
        if speed_kmh < 35.0:
            command['gear'] = 1
        else:
            if current_gear == 1 and speed_kmh >= 35.0: command['gear'] = 2
            elif current_gear == 2 and speed_kmh >= 68.0: command['gear'] = 3
            elif current_gear == 3 and speed_kmh >= 98.0: command['gear'] = 4
            elif current_gear == 4 and speed_kmh >= 128.0: command['gear'] = 5
            elif current_gear == 5 and speed_kmh >= 148.0: command['gear'] = 6
            elif current_gear == 6 and speed_kmh < 143.0: command['gear'] = 5
            elif current_gear == 5 and speed_kmh < 122.0: command['gear'] = 4
            elif current_gear == 4 and speed_kmh < 92.0:  command['gear'] = 3
            elif current_gear == 3 and speed_kmh < 62.0:  command['gear'] = 2
            elif current_gear == 2 and speed_kmh < 28.0:  command['gear'] = 1
            else: command['gear'] = current_gear
    except Exception:
        command['gear'] = 1

    return command

class Client:
    def __init__(self, host="127.0.0.1", port=3001):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1.0)
        self.memory = {'last_error': 0.0}
        self.connect()

    def connect(self):
        init_packet = "(init 0 45 90 135 180 225 270 315)"
        try:
            self.socket.sendto(init_packet.encode(), (self.host, self.port))
            print("?? Establishing real-time telemetry link...")
            data, addr = self.socket.recvfrom(4096)
            if data:
                print("?? Handshake locked! Connected cleanly to TORCS server gateway on Port 3001.")
                self.run_telemetry_loop(addr)
        except socket.timeout:
            raise ConnectionResetError("TORCS server idle. Check if simulator is open on the blue screen.")

    def run_telemetry_loop(self, addr):
        while True:
            try:
                data, _ = self.socket.recvfrom(4096)
                if not data:
                    break
                if b"shutdown" in data:
                    print("?? Race lap tracking completed cleanly.")
                    break
                state_obj = CarState(data)
                cmd = drive_control(state_obj, self.memory)
                response = f"(gear {cmd['gear']})(steer {cmd['steer']})(accel {cmd['accelerate']})(brake {cmd['brake']})"
                self.socket.sendto(response.encode(), addr)
            except socket.timeout:
                continue

if __name__ == '__main__':
    print("?? Nexus Agentic Core: Deploying production racing matrix loop...")
    while True:
        try:
            Client(port=3001)
        except (ConnectionResetError, socket.error):
            time.sleep(1)
            continue
        except KeyboardInterrupt:
            print("\n?? Loop terminated safely by developer layout execution request.")
            sys.exit(0)
