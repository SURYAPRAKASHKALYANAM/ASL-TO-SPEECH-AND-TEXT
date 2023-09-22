# ASL To Speech 🤖🔊

ASL To Speech is a web application that converts American Sign Language (ASL) gestures into speech. This project uses Deep learning to recognize ASL signs, generate corresponding text, and then convert that text into speech.

## Features 🌟

- Real-time ASL gesture recognition using a deep learning model.
- Streaming video feed of ASL gestures.
- Text-to-speech synthesis for spoken language.
- Start and stop controls for capturing ASL gestures and generating speech.
- Interactive web interface for user interaction.




https://github.com/SURYAPRAKASHKALYANAM/ASL-TO-SPEECH-AND-TEXT/assets/115471106/d1c2a902-eb37-4b27-9129-3e2dbd0c33fb


1. 🌐 **Flask Web App Setup**:
   - Initializes a Flask web application for sign language recognition.
   - Renders HTML templates and sets up routes for web interactions.

2. 🧠 **Model Loading**:
   - Loads a pre-trained VGG16-based model for sign language gesture recognition.
   - Utilizes TensorFlow and Keras for deep learning.

3. 📜 **Label Dictionary**:
   - Defines a dictionary mapping numeric model outputs to sign language letters and symbols.

4. 📷 **Video Capture**:
   - Initializes webcam capture using OpenCV (cv2) for real-time video input.
   - Sets up a video capture object (cap) for processing frames.

5. 🚦 **Real-time Gesture Recognition**:
   - Captures video frames, processes them with the loaded model, and recognizes sign language gestures.
   - Handles continuous video feed processing and updates recognized gestures.

6. 🗣️ **Speech Synthesis**:
   - Utilizes pyttsx3 to convert recognized sign language gestures into speech.
   - Configures speech properties like rate and volume.

7. 📢 **Audio File Generation**:
   - Generates an audio file containing the synthesized speech.
   - Saves the audio file to a unique path in the "static" directory.

8. 🖥️ **Webpage Display**:
   - Renders an HTML webpage for user interaction and feedback.
   - Displays real-time video feed, recognized sign language, and synthesized speech.

9. 🖱️ **JavaScript Functions**:
   - Provides JavaScript functions for controlling the application's behavior.
   - Manages starting and stopping video capture, displaying images, and user interactions.

10. 🚦 **HTTP Routes**:
    - Defines Flask routes to serve video frames, start/stop video capture, and retrieve synthesized audio.
    - Handles HTTP requests and returns appropriate responses.

11. 🛠️ **Error Handling**:
    - Implements error handling to gracefully manage exceptions and potential issues.
    - Ensures robust performance and user experience.

12. 📦 **Static File Serving**:
    - Configures Flask to serve static files (e.g., CSS, JavaScript, audio) to enhance web application functionality.

13. 🏃‍♀️ **Application Run**:
    - Runs the Flask application in debug mode for testing and development.
    - Launches the web application, making it accessible through a web browser.

These functions collectively create a web application for real-time sign language recognition and speech synthesis, enhancing accessibility and communication.



