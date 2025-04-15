import React, { useState, useEffect, useRef } from "react";
import Vapi from "@vapi-ai/web";

const VapiCallComponent = ({ apiKey, assistantId, name }) => {
  const [callActive, setCallActive] = useState(false);
  const [callEnded, setCallEnded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [volumeLevel, setVolumeLevel] = useState(0);

  const vapiRef = useRef(null);

  useEffect(() => {
    if (!vapiRef.current && apiKey) {
      vapiRef.current = new Vapi(apiKey);

      // Set up event listeners
      vapiRef.current.on("speech-start", () => {
        setIsSpeaking(true);
      });

      vapiRef.current.on("speech-end", () => {
        setIsSpeaking(false);
      });

      vapiRef.current.on("call-start", () => {
        setCallActive(true);
        setCallEnded(false);
        setLoading(false);
      });

      vapiRef.current.on("call-end", () => {
        setCallActive(false);
        setCallEnded(true);
        setLoading(false);
      });

      vapiRef.current.on("volume-level", (volume) => {
        setVolumeLevel(volume);
      });

      vapiRef.current.on("message", (message) => {
        console.log("Message received:", message);
      });

      vapiRef.current.on("error", (e) => {
        setError(e.message || "An error occurred");
        setLoading(false);
      });
    }

    return () => {
      // Cleanup on unmount
      if (vapiRef.current) {
        stopCall();
      }
    };
  }, [apiKey]);

  const startCall = async () => {
    if (!vapiRef.current) {
      setError("Vapi not initialized");
      return;
    }

    try {
      setLoading(true);
      setCallEnded(false);
      setError(null);
      const assistantOverrides = {
        recordingEnabled: false,
        variableValues: {
          name: name,
        },
      };
      const call = await vapiRef.current.start(assistantId, assistantOverrides);
      console.log("Call started:", call);
    } catch (err) {
      setError(err.message || "Failed to start call");
      setLoading(false);
    }
  };

  const stopCall = () => {
    if (vapiRef.current) {
      vapiRef.current.stop();
    }
  };

  // Create bars for volume visualization
  const renderVolumeBars = () => {
    const numberOfBars = 10;
    const bars = [];

    for (let i = 0; i < numberOfBars; i++) {
      const threshold = i / numberOfBars;
      const isActive = volumeLevel >= threshold;

      bars.push(
        <div
          key={i}
          className={`h-full w-2 mx-px rounded-sm transition-all duration-100 ${
            isActive ? "bg-blue-500" : "bg-gray-300"
          }`}
        />
      );
    }

    return bars;
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Vapi AI Call</h2>

      <div className="my-6">
        {!callActive ? (
          <button
            onClick={startCall}
            disabled={loading}
            className={`px-6 py-3 rounded-md font-semibold text-white transition-colors ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-green-600 hover:bg-green-700"
            }`}
          >
            {loading ? "Connecting..." : "Start Call"}
          </button>
        ) : (
          <button
            onClick={stopCall}
            className="px-6 py-3 rounded-md font-semibold text-white bg-red-600 hover:bg-red-700 transition-colors"
          >
            End Call
          </button>
        )}
      </div>

      {callActive && (
        <div className="my-6 p-4 bg-gray-100 rounded-lg">
          <div className="font-medium text-gray-800 mb-3">
            Call in progress
            {isSpeaking && (
              <span className="ml-2 text-blue-600">(AI speaking)</span>
            )}
          </div>

          {/* Volume visualization with bars */}
          <div className="h-8 flex items-end mb-2">{renderVolumeBars()}</div>
        </div>
      )}

      {callEnded && (
        <div className="my-6 p-4 bg-green-50 border-l-4 border-green-500 rounded text-green-700">
          Call has ended
        </div>
      )}

      {error && (
        <div className="my-6 p-4 bg-red-50 border-l-4 border-red-500 rounded text-red-700">
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default VapiCallComponent;
