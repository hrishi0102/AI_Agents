import React, { useState, useEffect, useRef } from "react";
import Vapi from "@vapi-ai/web";

const VapiCallComponent = ({ apiKey, assistantId, name }) => {
  const [callActive, setCallActive] = useState(false);
  const [callEnded, setCallEnded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [transcript, setTranscript] = useState([]);
  const [error, setError] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [volumeLevel, setVolumeLevel] = useState(0);

  const vapiRef = useRef(null);
  const transcriptRef = useRef(null);

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
        // Clear transcript for new call
        setTranscript([]);
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
        if (
          message.type === "transcript" &&
          message.transcriptType === "final"
        ) {
          const newMessage = {
            role: message.role,
            content: message.transcript,
          };
          setTranscript((prev) => [...prev, newMessage]);
        }
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

  // Scroll to bottom of transcript when it becomes visible after call ends
  useEffect(() => {
    if (callEnded && transcriptRef.current) {
      transcriptRef.current.scrollTop = 0; // Start at the top of the conversation
    }
  }, [callEnded]);

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
          name: name || "Guest",
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

  // Format the entire conversation as a combined transcript
  const renderFullTranscript = () => {
    if (transcript.length === 0) {
      return <p className="text-gray-500 italic">No transcript available</p>;
    }

    return transcript.map((message, index) => (
      <div
        key={index}
        className={`p-3 mb-3 rounded-lg ${
          message.role === "assistant"
            ? "bg-blue-50 border-l-4 border-blue-500"
            : "bg-gray-50 border-l-4 border-gray-500"
        }`}
      >
        <div className="font-semibold text-sm text-gray-700 mb-1">
          {message.role === "assistant" ? "AI Assistant" : "You"}
        </div>
        <div className="text-gray-800">{message.content}</div>
      </div>
    ));
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

      {/* Only show transcript after call has ended */}
      {callEnded && (
        <div>
          <div className="my-6 p-4 bg-green-50 border-l-4 border-green-500 rounded text-green-700">
            Call has ended
          </div>

          <div className="my-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Conversation Transcript
            </h3>
            <div
              ref={transcriptRef}
              className="max-h-96 overflow-y-auto p-4 border border-gray-200 rounded-lg bg-white shadow-sm"
            >
              {renderFullTranscript()}
            </div>
          </div>
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
