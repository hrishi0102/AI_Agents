import React, { useEffect } from "react";
import Vapi from "@vapi-ai/web";

function App() {
  const vapi_key = import.meta.env.VITE_VAPI_API_KEY;
  const assistant_id = import.meta.env.VITE_ASSISTANT_ID;
  const vapi = new Vapi(vapi_key);
  const startCall = () => {
    vapi.start(assistant_id);
  };

  return (
    <>
      <button onClick={startCall}>Start Call</button>
    </>
  );
}

export default App;
