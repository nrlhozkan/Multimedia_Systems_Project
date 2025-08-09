# Multimedia Drone Control System
## Complete Working Implementation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CoppeliaSim](https://img.shields.io/badge/CoppeliaSim-4.0+-green.svg)](https://www.coppeliarobotics.com/)
[![Status](https://img.shields.io/badge/Status-Working-brightgreen.svg)](README.md)

A complete multimedia drone control system featuring real-time video streaming, voice recognition, and web-based interface using CoppeliaSim simulation environment.

## 🎯 Project Overview

This project demonstrates the integration of simulation, multimedia processing, and real-time control systems. It provides a fully functional drone control system with:

- **Real-time drone simulation** using CoppeliaSim ZeroMQ Remote API
- **Live video streaming** from drone camera to web interface
- **Voice recognition** for natural language drone control
- **Multi-threaded architecture** for concurrent operations
- **WebSocket communication** for real-time updates
- **Professional web interface** for monitoring and control

## 🚀 Features

### Core Functionality
- ✅ **Complete CoppeliaSim Integration** - ZeroMQ Remote API implementation
- ✅ **Autonomous Drone Control** - Takeoff, landing, and directional movement
- ✅ **Real-time Camera System** - Live video capture and processing
- ✅ **Voice Command Recognition** - Natural language processing
- ✅ **Web-based Interface** - Remote monitoring and control
- ✅ **Multi-threading Support** - Concurrent voice and video processing

### Technical Highlights
- 🔧 **Robust Error Handling** - Graceful failure management
- 🔧 **Thread-safe Architecture** - Concurrent operations support
- 🔧 **Modular Design** - Clean, extensible codebase
- 🔧 **Professional Documentation** - Comprehensive code comments
- 🔧 **Cross-platform Compatible** - Windows, Linux, macOS support

## 🎥 Video Demonstration

See the system in action! The following video demonstrates the complete functionality:

<video width="800" controls>
  <source src="./example_video.mp4" type="video/mp4">
  Your browser does not support the video tag. <a href="./example_video.mp4">Download the video</a>
</video>

### What you'll see in the demo:
- ✅ **Voice Command Recognition** - Real-time speech-to-text processing
- ✅ **Drone Movement Control** - Responsive takeoff, landing, and directional commands  
- ✅ **Live Video Streaming** - Real-time camera feed from drone perspective
- ✅ **Web Interface** - Professional dashboard with status indicators
- ✅ **Multi-threading** - Simultaneous voice processing and video streaming
- ✅ **CoppeliaSim Integration** - Full simulation environment interaction

> **Note:** Make sure to have audio enabled to hear the voice commands being recognized in real-time!

## 📋 Requirements

### Software Dependencies
- **Python 3.8+** (recommended: Python 3.9 or higher)
- **CoppeliaSim 4.0+** (Education, Pro, or Player version)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

### Python Packages
```bash
# Core packages (automatically installed via requirements.txt)
coppeliasim-zmqremoteapi-client>=1.0.0    # CoppeliaSim API
opencv-python>=4.5.0                     # Computer vision
Flask>=2.0.0                             # Web framework
Flask-SocketIO>=5.0.0                    # Real-time communication
SpeechRecognition>=3.8.0                 # Voice recognition
pyaudio>=0.2.11                          # Audio processing
numpy>=1.21.0                            # Numerical computing
```

## 🔧 Installation & Setup

### 1. Environment Preparation
```bash
# Create and activate virtual environment (recommended)
python -m venv drone_env

# Windows:
drone_env\Scripts\activate
# Linux/Mac:
source drone_env/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. CoppeliaSim Configuration
1. **Download & Install CoppeliaSim**
   - Visit [CoppeliaSim Downloads](https://www.coppeliarobotics.com/downloads)
   - Install Education/Pro version (recommended)

2. **Load Drone Scene**
   - Start CoppeliaSim
   - File → Open Scene → `new_env.ttt`
   - Verify scene contains quadcopter with vision sensor
   - Press **Play** button to start simulation

### 3. Verification Test
```bash
# Quick connection test
python -c "from drone_simulation_base import DroneSimulationBase; print('✅ Setup OK' if DroneSimulationBase().connected else '❌ Check CoppeliaSim')"
```

## 📁 Project Structure

```
Published_Project/
├── 📄 README.md                     # Project documentation
├── 📄 requirements.txt              # Python dependencies
│
├── 🐍 **Core Implementation**
│   ├── drone_simulation_base.py     # CoppeliaSim integration infrastructure
│   └── multimedia_drone_working.py  # Complete working system
│
├── 🎮 **Simulation Files**
│   ├── new_env.ttt                  # CoppeliaSim scene file
│   ├── sim.py                       # CoppeliaSim API module
│   └── simConst.py                  # CoppeliaSim constants
│
└── 🌐 **Web Interface**
    └── templates/
        └── student_interface_template.html # Web UI template
```

## 🎮 Quick Start Guide

### Step 1: Launch Simulation
```bash
# 1. Start CoppeliaSim
# 2. Open scene: new_env.ttt
# 3. Press Play button ▶️
# 4. Verify drone is visible and responsive
```

### Step 2: Start the System
```bash
# In your activated Python environment
python multimedia_drone_working.py
```

**Expected Output:**
```
✅ CoppeliaSim ZeroMQ Remote API available
🎓 MULTIMEDIA SYSTEMS COURSE PROJECT - WORKING VERSION
🔌 Connecting to CoppeliaSim...
✅ Connected to CoppeliaSim successfully!
✅ Found drone: /Quadcopter
✅ Found target: /target
✅ Found vision sensor in drone hierarchy
🎤 Setting up voice recognition...
🌐 Starting web server...
 * Running on http://0.0.0.0:8080
```

### Step 3: Access Web Interface
- **Open browser** to: `http://localhost:8080`
- **View features:**
  - Live video feed from drone camera
  - Real-time drone status and position
  - Voice command feedback
  - Connection status monitoring

## 🎤 Voice Control Commands

Speak clearly into your microphone with natural pauses:

### Basic Flight Control
- **"take off"** or **"takeoff"** → Drone ascends to flight altitude
- **"land"** → Drone descends and lands safely

### Movement Commands
- **"forward"** or **"ahead"** → Move forward
- **"backward"** or **"back"** → Move backward  
- **"left"** → Move left
- **"right"** → Move right
- **"up"** → Increase altitude
- **"down"** → Decrease altitude

### Alternative Phrases (for better recognition)
- **"for"** → Recognized as "forward"
- **"lef"** → Recognized as "left"
- **"write"** → Recognized as "right"

## 🛠️ Technical Architecture

### System Components

#### 1. DroneSimulationBase Class
```python
# Core infrastructure providing:
- CoppeliaSim connection management
- Drone control methods (takeoff, land, move)
- Camera image processing
- Position monitoring
- Error handling and recovery
```

#### 2. MultimediaDroneSystem Class
```python
# Complete implementation featuring:
- Voice recognition engine
- Web server with Flask + SocketIO
- Multi-threaded video streaming
- Real-time status updates
- WebSocket communication
```

### Key Methods Reference

#### Connection & Setup
- `connect()` → Establish CoppeliaSim connection
- `disconnect()` → Clean resource cleanup

#### Drone Control
- `drone_takeoff()` → Execute takeoff sequence
- `drone_land()` → Execute landing sequence  
- `drone_move(direction)` → Move in specified direction

#### Multimedia Features
- `get_drone_camera_frame()` → Get processed video frame
- `execute_voice_command(command)` → Process voice input
- `generate_video_frames()` → Stream video to web interface

## 🔍 Troubleshooting Guide

### Common Issues & Solutions

#### 🔴 "Failed to connect to CoppeliaSim"
**Symptoms:** Connection timeout, API errors
**Solutions:**
1. Verify CoppeliaSim is running and scene is loaded
2. Ensure simulation is started (play button pressed)
3. Check firewall isn't blocking port 23000
4. Restart CoppeliaSim and try again

#### 🔴 "No camera found - some features may not work"
**Symptoms:** Black video feed, camera errors
**Solutions:**
1. Verify vision sensor exists in CoppeliaSim scene
2. Check vision sensor is attached to drone object
3. Ensure vision sensor is enabled and configured
4. Reload scene and restart simulation

#### 🔴 Voice commands not recognized
**Symptoms:** No response to voice input
**Solutions:**
1. Check microphone permissions in OS settings
2. Test microphone: `python -c "import speech_recognition as sr; print('Mic OK')"`
3. Reduce background noise environment
4. Speak clearly with 1-2 second pauses
5. Install/update: `pip install pyaudio --upgrade`

#### 🔴 Web interface not loading
**Symptoms:** Browser connection errors
**Solutions:**
1. Verify port 8080 is available
2. Check console output for Flask errors
3. Try different browser or incognito mode
4. Disable browser extensions temporarily
5. Check system firewall settings

### Performance Optimization

#### For Better Video Streaming
```python
# Adjust frame rate (in multimedia_drone_working.py)
self.frame_rate = 15  # Reduce from 30 for slower systems
```

#### For Voice Recognition
```python
# Tune recognition parameters
self.recognizer.energy_threshold = 300    # Increase for noisy environments
self.recognizer.pause_threshold = 0.8     # Adjust response time
```

## 📊 System Status Indicators

### Connection Status
- 🟢 **Connected** - CoppeliaSim integration active
- 🟡 **Connecting** - Attempting connection
- 🔴 **Disconnected** - No simulation connection

### Voice Recognition
- 🎤 **Listening** - Ready for voice commands
- 🗣️ **Processing** - Analyzing speech input
- ✅ **Command Executed** - Action completed
- ❌ **Command Failed** - Error in execution

### Video Streaming
- 📹 **Streaming** - Live video feed active
- ⏸️ **Paused** - Video temporarily stopped
- 📷 **No Signal** - Camera not available

## 🚀 Advanced Usage

### Extending the System
```python
# Example: Add custom voice commands
class CustomDroneSystem(MultimediaDroneSystem):
    def execute_voice_command(self, command):
        # Add your custom commands here
        if "circle" in command:
            return self.fly_circle_pattern()
        elif "home" in command:
            return self.return_to_home()
        else:
            # Use parent implementation
            return super().execute_voice_command(command)
```

### Integration Examples
- **Computer Vision**: Add object detection to camera feed
- **Path Planning**: Implement waypoint navigation
- **IoT Integration**: Connect to external sensors
- **Mobile Apps**: Create smartphone remote control
- **AI Enhancement**: Add machine learning capabilities

## 📈 Version Information

### Current Version: 1.0.0
**Features:**
- Complete CoppeliaSim integration
- Voice recognition system
- Web-based video streaming
- Multi-threaded architecture
- Professional documentation

**Tested Environments:**
- Windows 10/11 + Python 3.8-3.11
- CoppeliaSim 4.0-4.5
- Modern web browsers (Chrome, Firefox, Edge)

## 📞 Support & Contact

### Getting Help
1. **Check Troubleshooting** - Review common issues above
2. **Verify Requirements** - Ensure all dependencies installed
3. **Test Components** - Use verification commands provided
4. **Review Logs** - Check console output for errors

### Reporting Issues
When reporting problems, include:
- **Operating System** and version
- **Python version** (`python --version`)
- **CoppeliaSim version**
- **Complete error messages**
- **Steps to reproduce**

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Setup
pip install -r requirements.txt

# Run System
python multimedia_drone_working.py

# Access Interface
http://localhost:8080
```

### Voice Commands Quick List
```
"take off" | "land" | "forward" | "backward" | "left" | "right" | "up" | "down"
```

### Key Files
- `drone_simulation_base.py` → Core CoppeliaSim integration
- `multimedia_drone_working.py` → Complete working system
- `new_env.ttt` → CoppeliaSim scene file

---

**🚁 Ready to Fly! 🚁**

*This project showcases the seamless integration of simulation technology, multimedia processing, and real-time control systems. Perfect for demonstrating modern IoT and robotics capabilities.*
