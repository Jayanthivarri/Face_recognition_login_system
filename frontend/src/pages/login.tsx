import React, { useState, useRef, useEffect } from 'react';
import * as faceapi from 'face-api.js';
import './login.css';

interface FaceDescriptor {
  descriptor: number[];
  length: number;
}

interface LoginState {
  facingDetected: boolean;
  isLoading: boolean;
  error: string | null;
  faceDescriptor: FaceDescriptor | null;
  isCameraActive: boolean;
  modelsLoaded: boolean;
  accuracy: number;
  capturedImage: string;
  loggedInUser: string;
 
}
export const Login: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [state, setState] = useState<LoginState>({
    facingDetected: false,
    isLoading: false,
    error: null,
    faceDescriptor: null,
    isCameraActive: false,
    modelsLoaded: false,
    accuracy: 0,
    capturedImage: "",
    loggedInUser: "",
  });

  // Load FaceAPI models on component mount
  useEffect(() => {
    const loadModels = async () => {
      try {
        setState(prev => ({ ...prev, isLoading: true, error: null }));

        // Load models from public/models directory
        const MODEL_URL = '/models';

        await Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
          faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
          faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
        ]);

        setState(prev => ({ ...prev, modelsLoaded: true, isLoading: false }));
        console.log('✓ FaceAPI models loaded successfully');
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load models';
        setState(prev => ({
          ...prev,
          error: `Error loading FaceAPI models: ${errorMessage}`,
          isLoading: false,
        }));
        console.error('✗ Error loading models:', err);
      }
    };

    loadModels();
  }, []);

  // Request camera access and start video stream
  const startCamera = async () => {
    try {
      setState(prev => ({ ...prev, error: null, isLoading: true }));

      if (!videoRef.current) {
        setState(prev => ({
          ...prev,
          isCameraActive: true,
        }));
        await new Promise(resolve => setTimeout(resolve, 300));
      }

      // Request camera access
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user',
        },
        audio: false,
      });

      // Attach stream to video element
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
}

      // Wait for video to load before playing
      await new Promise<void>((resolve, reject) => {
        const video = videoRef.current!;
        const onLoadedMetadata = () => {
          video.removeEventListener('loadedmetadata', onLoadedMetadata);
          video.play().then(resolve).catch(reject);
        };
        video.addEventListener('loadedmetadata', onLoadedMetadata);
      });

      setState(prev => ({
        ...prev,
        isCameraActive: true,
        isLoading: false,
      }));

      console.log('✓ Camera started successfully');
    } catch (err) {
      if (err instanceof DOMException) {
        // Handle specific camera permission errors
        if (err.name === 'NotAllowedError') {
          setState(prev => ({
            ...prev,
            error: 'Camera permission denied. Please allow camera access to continue.',
            isLoading: false,
          }));
        } else if (err.name === 'NotFoundError') {
          setState(prev => ({
            ...prev,
            error: 'No camera device found. Please connect a camera.',
            isLoading: false,
          }));
        } else if (err.name === 'NotReadableError') {
          setState(prev => ({
            ...prev,
            error: 'Camera is already in use by another application.',
            isLoading: false,
          }));
        } else {
          setState(prev => ({
            ...prev,
            error: `Camera error: ${err.message}`,
            isLoading: false,
          }));
        }
      } else {
        const errorMessage = err instanceof Error ? err.message : 'Unknown error';
        setState(prev => ({
          ...prev,
          error: `Failed to access camera: ${errorMessage}`,
          isLoading: false,
        }));
      }
      console.error('✗ Error accessing camera:', err);
    }
  };

  // Stop camera and clean up resources
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }

    setState(prev => ({
      ...prev,
      isCameraActive: false,
      facingDetected: false,
    }));

    console.log('✓ Camera stopped');
  };

  // Detect face in video stream
  const detectFace = async () => {
    if (!videoRef.current || !state.modelsLoaded) {
      return;
    }

    try {
      // Run detection with TinyFaceDetector for performance
      const detections = await faceapi
        .detectSingleFace(videoRef.current, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceDescriptor();
      if (detections) {

  const confidence = Math.round(
    detections.detection.score * 100
  );

  const canvas = canvasRef.current;

  if (canvas && videoRef.current) {
    const displaySize = {
      width: videoRef.current.videoWidth,
      height: videoRef.current.videoHeight,
    };

    canvas.width = displaySize.width;
    canvas.height = displaySize.height;

    faceapi.matchDimensions(canvas, displaySize);

    const resizedDetection = faceapi.resizeResults(
      detections,
      displaySize
    );

    const ctx = canvas.getContext("2d");
    ctx?.clearRect(0, 0, canvas.width, canvas.height);

    faceapi.draw.drawDetections(canvas, [resizedDetection]);
  }

  setState(prev => ({
    ...prev,
    facingDetected: true,
    accuracy: confidence,
  }));

} else {

  setState(prev => ({
    ...prev,
    facingDetected: false,
    accuracy: 0,
  }));

}
    } catch (err) {
      console.error('Error during face detection:', err);
    }
  };

  // Continuous face detection loop
  useEffect(() => {
    if (!state.isCameraActive || !state.modelsLoaded) {
      return;
    }

    const detectionInterval = setInterval(() => {
      detectFace();
    }, 300); // Run detection every 300ms

    return () => clearInterval(detectionInterval);
  }, [state.isCameraActive, state.modelsLoaded]);

  // Capture face descriptor
  const captureFace = async () => {
    if (!videoRef.current || !state.modelsLoaded || !state.facingDetected) {
      setState(prev => ({
        ...prev,
        error: 'No face detected. Please ensure your face is visible to the camera.',
      }));
      return;
    }

    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));

      // Detect face with descriptor
      const detections = await faceapi
        .detectSingleFace(videoRef.current, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceDescriptor();

      if (!detections) {
        
        setState(prev => ({
          ...prev,
          error: 'Failed to capture face. Please try again.',
          isLoading: false,
        }));
        return;
      }

      const descriptor = Array.from(detections.descriptor);
      const canvas = document.createElement("canvas");

      canvas.width = videoRef.current!.videoWidth;
      canvas.height = videoRef.current!.videoHeight;

      const ctx = canvas.getContext("2d");

      ctx?.drawImage(
      videoRef.current!,
      0,
      0,
      canvas.width,
      canvas.height
    );

const imageData = canvas.toDataURL("image/png");
      // Validate descriptor
      if (descriptor.length !== 128) {
        setState(prev => ({
          ...prev,
          error: `Invalid descriptor length: ${descriptor.length} (expected 128)`,
          isLoading: false,
        }));
        return;
      }

      // Store descriptor in state
      setState(prev => ({
        ...prev,
        faceDescriptor: {
          descriptor,
          length: descriptor.length,
        },
        capturedImage: imageData,
        isLoading: false,
      }));
      console.log("REQUEST BODY", {
 
  face_embedding_length: descriptor.length
});

      const response =await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        face_embedding: descriptor,
     }),
   });
    const data = await response.json();
    console.log("LOGIN RESPONSE:", data);
    const loginTime = new Date().toLocaleString();
    if (!response.ok) {
  alert("❌ Face Not Registered");
  return;
}
    if (data.success) {

  setState(prev => ({
    ...prev,
    loggedInUser: data.user.first_name,
  }));

  alert(
    `🎉 Welcome ${data.user.first_name}!\n\n` +
    `🕒 Login Time: ${loginTime}`
  );
}

console.log("FULL RESPONSE");
console.log(data);

if (!response.ok) {
  console.log("ERROR RESPONSE:", JSON.stringify(data, null, 2));

  throw new Error(JSON.stringify(data, null, 2));
}



      console.log('✓ Face captured successfully');
      console.log(`✓ Descriptor captured: ${descriptor.length} dimensions`);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message   : JSON.stringify(err, null, 2); 
      setState(prev => ({
        ...prev,
        error: `Failed to capture face: ${errorMessage}`,
        isLoading: false,
      }));
      console.error('✗ Error capturing face:', err);
    }
  };

  // Clear captured descriptor
  const clearCapture = () => {
    setState(prev => ({
      ...prev,
      faceDescriptor: null,
      error: null,
    }));
    console.log('✓ Capture cleared');
  };

  return (
    <div className="register-container">
      {/* Header */}
      <header className="register-header">
        <h1>🔐 Face Recognition Login System</h1>
        
      </header>

      {/* Main Content */}
      <div className="register-content">
        {/* Left Panel - Camera */}
        <div className="camera-panel">
          <div className="camera-wrapper">
            {state.modelsLoaded ? (
              <>
                {state.isCameraActive ? (
                  <div className="video-container">
                    <video
                      ref={videoRef}
                      className="video-element"
                      autoPlay
                      playsInline
                      muted
                    />
                    <canvas
                      ref={canvasRef}
                      className="detection-canvas"
                    />

                    {/* Face Status Indicator */}
                    <div
                      className={`face-status ${
                        state.facingDetected ? 'detected' : 'not-detected'
                      }`}
                    >
                      <div className="status-dot" />
                      <span className="status-text">
                        {state.facingDetected ? '✓ Face Detected' : '✗ No Face Detected'}
                      </span>
                    </div>
                  </div>
                ) : (
                  <div className="camera-placeholder">
                    <div className="placeholder-icon">📷</div>
                    <p>Camera is off</p>
                    <p className="placeholder-hint">
                      Click "Start Camera" to begin
                    </p>
                  </div>
                )}
              </>
            ) : (
              <div className="camera-placeholder">
                <div className="placeholder-icon loading">⚙️</div>
                <p>Loading models...</p>
                <p className="placeholder-hint">
                  This may take a moment on first load
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Info */}
        <div className="info-panel">
          {/* Status Section */}
          <div className="status-section">
            <h2>Status</h2>
            <div className="status-grid">
              <div className="status-item">
                <span className="status-label">Models</span>
                <span
                  className={`status-value ${
                    state.modelsLoaded ? 'success' : 'pending'
                  }`}
                >
                  {state.modelsLoaded ? '✓ Loaded' : '⏳ Loading'}
                </span>
              </div>
              <div className="status-item">
                <span className="status-label">Camera</span>
                <span
                  className={`status-value ${
                    state.isCameraActive ? 'success' : 'pending'
                  }`}
                >
                  {state.isCameraActive ? '✓ Active' : '○ Inactive'}
                </span>
              </div>
              <div className="status-item">
                <span className="status-label">Face</span>
                <span
                  className={`status-value ${
                    state.facingDetected ? 'success' : 'pending'
                  }`}
                >
                  {state.facingDetected ? '✓ Detected' : '○ Waiting'}
                </span>
              </div>
              <div className="status-item">
                <span className="status-label">Captured</span>
                <span
                  className={`status-value ${
                    state.faceDescriptor ? 'success' : 'pending'
                  }`}
                >
                  {state.faceDescriptor ? '✓ Yes' : '○ No'}
                </span>
              </div>
            </div>
          </div>
          {state.capturedImage && (
  <div className="captured-preview">
    <h3>📷 Captured Face</h3>

    <img
      src={state.capturedImage}
      alt="Captured Face"
      className="captured-image"
    />

    <p>🎯 Accuracy: {state.accuracy}%</p>
  </div>
)}

          {/* Descriptor Section */}
          {state.faceDescriptor && (
            <div className="descriptor-section">
              <h3>Face Descriptor</h3>
              <div className="descriptor-info">
                <p>
                  <strong>Dimensions:</strong> {state.faceDescriptor.length}
                </p>
                <p className="descriptor-hint">
                  128-dimensional vector representing your face
                </p>
                <div className="descriptor-preview">
                  <p>Sample values (first 10):</p>
                  <code>
                    {`[${state.faceDescriptor.descriptor
                      .slice(0, 10)
                      .map(v => v.toFixed(4))
                      .join(', ')}, ...]`}
                  </code>
                </div>
              </div>
            </div>
          )}

          {/* Error Section */}
          {state.error && (
            <div className="error-section">
              <p className="error-message">⚠️ {state.error}</p>
            </div>
          )}   

          {/* Controls Section */}
          <div className="controls-section">
            {!state.isCameraActive ? (
              <button
                className="btn btn-primary"
                onClick={startCamera}
                disabled={!state.modelsLoaded || state.isLoading}
              >
                {state.isLoading ? 'Starting...' : 'Start Camera'}
              </button>
            ) : (
              <>
                <button
                  className="btn btn-success"
                  onClick={captureFace}
                  disabled={!state.facingDetected || state.isLoading}
                >
                  {state.isLoading ? 'Capturing...' : 'Capture Face'}
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={stopCamera}
                  disabled={state.isLoading}
                >
                  Stop Camera
                </button>
              </>
            )}

            {state.faceDescriptor && (
              <button
                className="btn btn-outline"
                onClick={clearCapture}
                disabled={state.isLoading}
              >
                Clear Capture
              </button>
            )}
          </div>

          
        </div>
      </div>
    </div>
  );
};

export default Login;
