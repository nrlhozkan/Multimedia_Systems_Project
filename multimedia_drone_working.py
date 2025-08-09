# Multimedia Systems Course Project: Complete Working Implementation
# This is a reference implementation showing how to build the complete system

import time
import numpy as np
import cv2
import threading
import speech_recognition as sr
import json
from datetime import datetime
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit

# Import the provided base infrastructure
from drone_simulation_base import DroneSimulationBase


class MultimediaDroneSystem(DroneSimulationBase):
    """
    Complete implementation of multimedia drone control system.
    
    Features:
    - Real-time voice recognition and control
    - Live video streaming to web interface
    - WebSocket communication for real-time updates
    - Multi-threaded architecture for concurrent operations
    """
    
    def __init__(self, web_port=8080):
        # Initialize the base drone simulation
        super().__init__()
        
        # Flask web application setup
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'multimedia_drone_course_2025'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Check component availability
        self.socketio_available = True  # SocketIO is available
        self.sr_available = True  # SpeechRecognition is available
        
        # Video streaming variables
        self.streaming = False
        self.frame_rate = 30
        self.current_frame = None
        self.frame_lock = threading.Lock()
        
        # Voice recognition system
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.voice_listening = False
        self.last_command = ""
        self.last_command_time = time.time()
        
        # Statistics and monitoring
        self.stats = {
            'connected_clients': 0,
            'total_commands': 0,
            'successful_commands': 0,
            'start_time': time.time(),
            'last_command': '',
            'drone_status': 'disconnected'
        }
        
        # Setup methods
        self.setup_voice_recognition()
        self.setup_web_server()
        
        print(f"✅ Multimedia Drone System initialized")
        print(f"🌐 Web interface will be available at: http://localhost:{web_port}")
    
    def setup_voice_recognition(self):
        """Setup voice recognition with optimized parameters"""
        try:
            print("🎤 Setting up voice recognition...")
            
            # Calibrate microphone for ambient noise
            with self.microphone as source:
                print("🔧 Calibrating microphone (please be quiet for 2 seconds)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("📊 Ambient noise level calibrated")
            
            # Configure recognition parameters for better accuracy
            self.recognizer.energy_threshold = 150  # Lower = more sensitive
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.6  # Shorter pause = faster response
            self.recognizer.phrase_threshold = 0.2  # Lower = better word detection
            self.recognizer.non_speaking_duration = 0.5
            
            print("✅ Voice recognition setup complete")
            print("🎤 Available voice commands:")
            print("   - 'take off' or 'takeoff'")
            print("   - 'land'")
            print("   - 'forward', 'back', 'left', 'right'")
            print("   - 'up', 'down', 'stop'")
            print("💡 Tips: Speak clearly, pause between commands")
            
        except Exception as e:
            print(f"⚠️ Voice recognition setup failed: {e}")
            print("🎤 Voice control will not be available")
    
    def start_voice_control(self):
        """Start listening for voice commands with improved recognition"""
        if not self.sr_available or not hasattr(self, 'recognizer') or not hasattr(self, 'microphone'):
            print("❌ Voice recognition not available")
            return
            
        self.voice_listening = True
        print("🎤 Voice control started - speak commands to control drone")
        print("🗣️ Speak clearly and wait for feedback...")
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while self.voice_listening:
            try:
                # Listen for audio input
                with self.microphone as source:
                    print("🎧 Listening for command...")
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=4)
                
                # Try multiple recognition attempts for better accuracy
                command = None
                recognition_attempts = 0
                max_attempts = 2
                
                while recognition_attempts < max_attempts and command is None:
                    try:
                        recognition_attempts += 1
                        print(f"🔍 Recognition attempt {recognition_attempts}/{max_attempts}...")
                        
                        # Try Google Speech Recognition
                        command = self.recognizer.recognize_google(
                            audio, 
                            language='en-US'
                        ).lower().strip()
                        
                        if command:
                            print(f"🗣️ Heard: '{command}' (attempt {recognition_attempts})")
                            break
                            
                    except sr.UnknownValueError:
                        if recognition_attempts < max_attempts:
                            print(f"🔄 Could not understand (attempt {recognition_attempts}), trying again...")
                        continue
                    except sr.RequestError as e:
                        print(f"⚠️ Speech recognition error: {e}")
                        break
                
                if command:
                    # Reset error counter on successful recognition
                    consecutive_errors = 0
                    
                    # Execute the command
                    result = self.execute_voice_command(command)
                    self.last_command = command
                    self.last_command_time = time.time()
                    
                    # Update statistics
                    self.stats['total_commands'] += 1
                    self.stats['last_command'] = command
                    if result['status'] == 'success':
                        self.stats['successful_commands'] += 1
                        print(f"✅ Command executed: {result['message']}")
                        
                        # Notify web clients
                        if self.socketio_available and self.socketio:
                            self.socketio.emit('command_executed', {
                                'command': command,
                                'status': 'success',
                                'message': result['message']
                            })
                    else:
                        print(f"❌ Command failed: {result['message']}")
                        
                        # Notify web clients of error
                        if self.socketio_available and self.socketio:
                            self.socketio.emit('command_executed', {
                                'command': command,
                                'status': 'error',
                                'message': result['message']
                            })
                else:
                    print("🤷 No clear command detected, please try again")
                        
            except sr.WaitTimeoutError:
                # No speech detected - this is normal
                pass
            except Exception as e:
                consecutive_errors += 1
                print(f"❌ Voice control error ({consecutive_errors}/{max_consecutive_errors}): {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print("⚠️ Too many errors, restarting voice recognition...")
                    time.sleep(2)
                    # Recalibrate microphone
                    try:
                        with self.microphone as source:
                            self.recognizer.adjust_for_ambient_noise(source, duration=1)
                        consecutive_errors = 0
                        print("🔧 Microphone recalibrated")
                    except:
                        print("❌ Failed to recalibrate microphone")
                else:
                    time.sleep(0.5)
    
    def setup_web_server(self):
        """Setup Flask web application and routes"""
        
        @self.app.route('/')
        def index():
            """Main web interface"""
            return render_template('drone_control.html')
        
        @self.app.route('/drone_control.html')
        def drone_control():
            """Simple drone control interface"""
            return render_template('drone_control.html')
        
        @self.app.route('/video_feed')
        def video_feed():
            """Video streaming route"""
            return Response(self.generate_video_frames(),
                          mimetype='multipart/x-mixed-replace; boundary=frame')
        
        @self.app.route('/stats')
        def get_stats():
            """Get real-time statistics"""
            # Update drone status
            status = self.get_drone_status()
            self.stats['drone_status'] = 'connected' if status['connected'] else 'disconnected'
            self.stats['drone_position'] = status.get('drone_position')
            self.stats['target_position'] = status.get('target_position')
            
            return jsonify(self.stats)
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            self.stats['connected_clients'] += 1
            print(f"📱 Client connected. Total: {self.stats['connected_clients']}")
            
            # Send welcome message to client
            emit('status_update', {
                'message': 'Connected to drone system',
                'drone_connected': self.connected
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            self.stats['connected_clients'] = max(0, self.stats['connected_clients'] - 1)
            print(f"📱 Client disconnected. Total: {self.stats['connected_clients']}")
        
        @self.socketio.on('request_drone_status')
        def handle_status_request():
            """Send current drone status to client"""
            status = self.get_drone_status()
            emit('drone_status', status)
        
        @self.socketio.on('manual_command')
        def handle_manual_command(data):
            """Handle manual commands from web interface"""
            command = data.get('command', '').lower().strip()
            if command:
                result = self.execute_voice_command(command)
                emit('command_result', {
                    'command': command,
                    'status': result['status'],
                    'message': result['message']
                })
    
    def generate_video_frames(self):
        """Generate video frames for web streaming"""
        while True:
            frame = None
            
            # Get current frame with thread safety
            with self.frame_lock:
                if self.current_frame is not None:
                    frame = self.current_frame.copy()
            
            if frame is not None:
                
                # Encode frame for web streaming
                _, buffer = cv2.imencode('.jpg', frame,
                                       [cv2.IMWRITE_JPEG_QUALITY, 85])
                frame_bytes = buffer.tobytes()
                
                # Yield frame in correct format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       frame_bytes + b'\r\n')
            else:
                # Generate a placeholder frame if no camera data
                placeholder = self.generate_placeholder_frame()
                _, buffer = cv2.imencode('.jpg', placeholder,
                                       [cv2.IMWRITE_JPEG_QUALITY, 85])
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       frame_bytes + b'\r\n')
            
            # Control frame rate (30 FPS)
            time.sleep(1/30)
    
    def generate_placeholder_frame(self):
        """Generate placeholder frame when camera is not available"""
        height, width = 480, 640
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Dark background
        frame.fill(50)
        
        # Add message
        cv2.putText(frame, "WAITING FOR CAMERA...", (width//2 - 150, height//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Check CoppeliaSim connection", (width//2 - 120, height//2 + 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
        
        return frame
    
    def add_telemetry_overlay(self, frame):
        """Add informational overlay to video frames"""
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, f"Time: {timestamp}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Add drone connection status
        status_text = "Connected" if self.connected else "Disconnected"
        color = (0, 255, 0) if self.connected else (0, 0, 255)  # Green/Red
        cv2.putText(frame, f"Drone: {status_text}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Add drone position (if available)
        try:
            status = self.get_drone_status()
            if status['connected'] and status['drone_position']:
                pos = status['drone_position']
                cv2.putText(frame, f"Position: X:{pos[0]:.1f} Y:{pos[1]:.1f} Z:{pos[2]:.1f}",
                           (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except:
            pass
        
        # Add voice command statistics
        cv2.putText(frame, f"Commands: {self.stats['total_commands']}", 
                   (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Add last voice command (if recent)
        time_since_command = time.time() - self.last_command_time
        if time_since_command < 5 and self.last_command:  # Show for 5 seconds
            cv2.putText(frame, f"Last Command: {self.last_command}",
                       (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0, 255, 255), 2)
        
        return frame
    
    def execute_voice_command(self, command):
        """Parse and execute voice commands with flexible matching"""
        command = command.lower().strip()
        
        if not self.connected:
            return {"status": "error", "message": "Drone not connected"}
        
        try:
            # Takeoff commands
            if any(phrase in command for phrase in ["take off", "takeoff", "lift off"]):
                return self.drone_takeoff()
            
            # Landing commands
            elif any(phrase in command for phrase in ["land", "landing"]):
                return self.drone_land()
            
            # Movement commands
            elif any(phrase in command for phrase in ["forward", "ahead"]):
                return self.drone_move("forward")
            
            elif any(phrase in command for phrase in ["back", "backward"]):
                return self.drone_move("backward")
            
            elif "left" in command:
                return self.drone_move("left")
            
            elif "right" in command:
                return self.drone_move("right")
            
            elif "up" in command:
                return self.drone_move("up")
            
            elif "down" in command:
                return self.drone_move("down")
            
            elif any(phrase in command for phrase in ["stop", "halt", "hover"]):
                return {"status": "success", "message": "Drone stopped (hovering)"}
            
            # Handle partial matches for better recognition
            elif "for" in command:  # "forward" might be heard as "for"
                return self.drone_move("forward")
            elif "lef" in command:  # "left" variations
                return self.drone_move("left")
            elif "righ" in command or "write" in command:  # "right" might be heard as "write"
                return self.drone_move("right")
            else:
                return {"status": "error", 
                       "message": f"Unknown command: '{command}'. Try: take off, land, forward, back, left, right, up, down, stop"}
        
        except Exception as e:
            return {"status": "error", "message": f"Command execution failed: {e}"}
    
    def video_capture_loop(self):
        """Continuous video capture loop"""
        print("🎬 Starting video capture...")
        self.streaming = True
        
        while self.streaming:
            frame = self.get_drone_camera_frame()
            if frame is not None:
                with self.frame_lock:
                    self.current_frame = frame
            time.sleep(1/self.frame_rate)
        
        print("🎬 Video capture stopped")
    
    def start_server(self):
        """Start the complete multimedia system"""
        print("🚀 Starting Multimedia Drone System...")
        
        # Start video capture in separate thread
        video_thread = threading.Thread(target=self.video_capture_loop)
        video_thread.daemon = True
        video_thread.start()
        print("🎬 Video capture thread started")
        
        # Start voice control in separate thread
        voice_thread = threading.Thread(target=self.start_voice_control)
        voice_thread.daemon = True
        voice_thread.start()
        print("🎤 Voice control thread started")
        
        print("✅ All systems started successfully!")
        print("🌐 Open browser to: http://localhost:8080")
        print("🎤 Voice control active - speak commands to control drone")
        print("📹 Video streaming active")
        
        # Start Flask web server (this will block)
        try:
            if self.socketio_available and self.socketio:
                self.socketio.run(self.app, host='0.0.0.0', port=8080, debug=False)
            else:
                self.app.run(host='0.0.0.0', port=8080, debug=False)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down system...")
            self.streaming = False
            self.voice_listening = False
            print("✅ System stopped")


def main():
    """Main function to start the multimedia drone system"""
    print("🎓 MULTIMEDIA SYSTEMS COURSE PROJECT - WORKING VERSION")
    print("=" * 60)
    print("📋 Complete Implementation: Drone Voice Control & Video Streaming")
    print()
    
    # Create and start the system
    system = MultimediaDroneSystem()
    system.start_server()


if __name__ == "__main__":
    main()
