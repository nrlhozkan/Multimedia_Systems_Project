# Multimedia Systems Course Project: Base Infrastructure
# This file provides the core simulation and connection components
# Students should inherit from this class and extend it with their features

import time
import numpy as np
import cv2

try:
    from coppeliasim_zmqremoteapi_client import RemoteAPIClient
    print("✅ CoppeliaSim ZeroMQ Remote API available")
    SIMULATION_MODE = True
except ImportError:
    print("❌ CoppeliaSim ZeroMQ Remote API not found!")
    SIMULATION_MODE = False


class DroneSimulationBase:
    """
    Base class providing core drone simulation and connection functionality.
    This handles all CoppeliaSim integration and drone operations.
    Students should inherit from this class and add their own multimedia features.
    
    Example usage:
        class MyDroneController(DroneSimulationBase):
            def __init__(self):
                super().__init__()
                # Add your custom initialization here
                
            def my_custom_method(self):
                # Use self.move_target(), self.get_camera_image(), etc.
                pass
    """
    
    def __init__(self, port=23000):
        """Initialize the drone simulation base"""
        # CoppeliaSim connection
        self.client = None
        self.sim = None
        self.port = port
        self.connected = False
        
        # Drone objects
        self.drone_handle = None
        self.target_handle = None
        self.vision_sensor_handle = None
        
        # Initialize connection
        self.connect()
    
    def connect(self):
        """Connect to CoppeliaSim and setup drone objects"""
        if not SIMULATION_MODE:
            print("❌ CoppeliaSim not available - please install CoppeliaSim")
            return False
            
        try:
            print("🔌 Connecting to CoppeliaSim...")
            self.client = RemoteAPIClient()
            self.sim = self.client.getObject('sim')
            print("✅ Connected to CoppeliaSim successfully!")
            self.connected = True
            
            if self.setup_objects():
                print("✅ Drone base initialized successfully!")
                return True
            else:
                print("❌ Failed to setup drone objects")
                return False
                
        except Exception as e:
            print(f"❌ Failed to connect to CoppeliaSim: {e}")
            return False
    
    def setup_objects(self):
        """Find and setup drone and target objects in CoppeliaSim"""
        try:
            print("🔍 Searching for objects in the scene...")
            
            # Find the drone (quadcopter)
            drone_names = ['Quadcopter', 'Drone', 'quadcopter', 'Quadricopter']
            for name in drone_names:
                try:
                    self.drone_handle = self.sim.getObject(name)
                    print(f"✅ Found drone: {name}")
                    break
                except:
                    try:
                        self.drone_handle = self.sim.getObject(f'/{name}')
                        print(f"✅ Found drone: /{name}")
                        break
                    except:
                        continue
            
            if self.drone_handle is None:
                print("❌ Could not find drone object!")
                return False
            
            # Find the target object
            target_names = ['target', 'Target', 'goal', 'Goal']
            for name in target_names:
                try:
                    self.target_handle = self.sim.getObject(name)
                    print(f"✅ Found target: {name}")
                    break
                except:
                    try:
                        self.target_handle = self.sim.getObject(f'/{name}')
                        print(f"✅ Found target: /{name}")
                        break
                    except:
                        continue
            
            if self.target_handle is None:
                print("❌ Could not find target object!")
                return False
            
            # Setup camera/vision sensor
            self.setup_camera()
            
            return True
            
        except Exception as e:
            print(f"❌ Error setting up objects: {e}")
            return False
    
    def setup_camera(self):
        """Find and setup camera/vision sensor on drone"""
        try:
            # Try to find vision sensor
            camera_names = ['VisionSensor', 'Camera', 'camera', 'vision_sensor']
            for name in camera_names:
                try:
                    self.vision_sensor_handle = self.sim.getObject(name)
                    print(f"✅ Found camera: {name}")
                    break
                except:
                    try:
                        self.vision_sensor_handle = self.sim.getObject(f'/{name}')
                        print(f"✅ Found camera: /{name}")
                        break
                    except:
                        continue
            
            # If not found, check drone's children
            if self.vision_sensor_handle is None and self.drone_handle is not None:
                try:
                    children = self.sim.getObjectsInTree(self.drone_handle)
                    for child in children:
                        try:
                            obj_type = self.sim.getObjectType(child)
                            if obj_type == self.sim.object_visionsensor_type:
                                self.vision_sensor_handle = child
                                print("✅ Found vision sensor in drone hierarchy")
                                break
                        except:
                            continue
                except:
                    pass
            
            if self.vision_sensor_handle is None:
                print("⚠️  No camera found - some features may not work")
                
        except Exception as e:
            print(f"⚠️  Camera setup warning: {e}")
    
    def get_camera_image(self):
        """Get camera image from drone's vision sensor"""
        if self.vision_sensor_handle is not None:
            try:
                img, resolution = self.sim.getVisionSensorImg(self.vision_sensor_handle)
                return img, resolution
            except Exception as e:
                # Silent error - simulation may not be running
                pass
        return None, None
    
    def move_target(self, position):
        """Move the target object - drone will follow"""
        print(f"🎯 Attempting to move target to: {position}")
        print(f"🎯 Target handle: {self.target_handle}")
        
        if self.target_handle is not None:
            try:
                self.sim.setObjectPosition(self.target_handle, -1, position.tolist())
                print("✅ Target position set successfully")
                return True
            except Exception as e:
                print(f"❌ Failed to set target position: {e}")
                pass
        else:
            print("❌ Target handle is None!")
        return False
    
    def get_positions(self):
        """Get current drone and target positions"""
        print(f"📍 Getting positions - drone_handle: {self.drone_handle}, target_handle: {self.target_handle}")
        try:
            if self.drone_handle and self.target_handle:
                drone_pos = np.array(self.sim.getObjectPosition(self.drone_handle, -1))
                target_pos = np.array(self.sim.getObjectPosition(self.target_handle, -1))
                print(f"📍 Successfully got positions - drone: {drone_pos}, target: {target_pos}")
                return drone_pos, target_pos
        except Exception as e:
            print(f"❌ Failed to get positions: {e}")
            pass
        print("❌ Returning None positions")
        return None, None
    
    def get_drone_camera_frame(self):
        """Get camera frame for multimedia applications"""
        img_data, resolution = self.get_camera_image()
        if img_data and resolution:
            try:
                img_array = np.frombuffer(img_data, dtype=np.uint8)
                frame = img_array.reshape((resolution[1], resolution[0], 3))
                frame = cv2.flip(frame, 0)
                return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            except Exception as e:
                # Silent error - camera frame conversion issue
                return None
        return None
    
    def drone_takeoff(self):
        """Execute takeoff command"""
        try:
            _, current_target = self.get_positions()
            if current_target is not None:
                current_target[2] = max(1.0, current_target[2])
                if self.move_target(current_target):
                    return {"status": "success", "message": "Taking off"}
            return {"status": "error", "message": "Takeoff failed"}
        except Exception as e:
            return {"status": "error", "message": "Takeoff failed - check CoppeliaSim"}
    
    def drone_land(self):
        """Execute landing command"""
        try:
            _, current_target = self.get_positions()
            if current_target is not None:
                current_target[2] = 0.3
                if self.move_target(current_target):
                    return {"status": "success", "message": "Landing"}
            return {"status": "error", "message": "Landing failed"}
        except Exception as e:
            return {"status": "error", "message": "Landing failed - check CoppeliaSim"}
    
    def drone_move(self, direction):
        """Execute movement command"""
        try:
            print(f"🎯 Attempting to move {direction}...")
            print(f"🔗 Connection status: {self.connected}")
            
            drone_pos, current_target = self.get_positions()
            print(f"📍 Drone position: {drone_pos}")
            print(f"🎯 Target position: {current_target}")
            
            if current_target is not None:
                move_step = 0.2
                print(f"📏 Move step: {move_step}")
                
                if direction == "forward":
                    current_target[0] += move_step
                elif direction == "backward":
                    current_target[0] -= move_step
                elif direction == "left":
                    current_target[1] += move_step
                elif direction == "right":
                    current_target[1] -= move_step
                elif direction == "up":
                    current_target[2] += move_step
                elif direction == "down":
                    current_target[2] = max(0.3, current_target[2] - move_step)
                
                print(f"🎯 New target position: {current_target}")
                move_result = self.move_target(current_target)
                print(f"✅ Move target result: {move_result}")
                
                if move_result:
                    return {"status": "success", "message": f"Moving {direction}"}
                else:
                    return {"status": "error", "message": f"Move target failed for {direction}"}
            else:
                return {"status": "error", "message": f"Cannot get target position for {direction}"}
        except Exception as e:
            print(f"❌ Exception in drone_move: {e}")
            return {"status": "error", "message": f"Move failed - check CoppeliaSim: {e}"}
    
    def disconnect(self):
        """Disconnect from CoppeliaSim"""
        if self.connected:
            print("🔌 Disconnected from CoppeliaSim")
            self.connected = False
    
    def get_drone_status(self):
        """Get current drone position and status"""
        try:
            drone_pos, target_pos = self.get_positions()
            return {
                "connected": self.connected,
                "drone_position": drone_pos.tolist() if drone_pos is not None else None,
                "target_position": target_pos.tolist() if target_pos is not None else None
            }
        except Exception as e:
            # Silent error - simulation state issue
            pass
        return {"connected": False}
