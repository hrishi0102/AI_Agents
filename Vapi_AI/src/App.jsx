import React, { useState } from "react";
import VapiCallComponent from "./VapiCallComponent";

function App() {
  const apiKey = import.meta.env.VITE_VAPI_API_KEY;
  const assistantId = import.meta.env.VITE_ASSISTANT_ID;
  const [name, setName] = useState("");

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <header className="text-center mb-10">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Vapi AI Call Demo
          </h1>
          <div className="max-w-md mx-auto">
            <h2 className="text-xl font-medium text-gray-700 mb-3">
              Enter Your Name
            </h2>
            <input
              type="text"
              placeholder="John Doe"
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </header>
        <main>
          <VapiCallComponent
            apiKey={apiKey}
            assistantId={assistantId}
            name={name}
          />
        </main>
      </div>
    </div>
  );
}

export default App;
