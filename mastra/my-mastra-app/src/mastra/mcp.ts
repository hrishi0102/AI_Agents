import { MCPClient } from "@mastra/mcp";
import { Agent } from "@mastra/core/agent";
import { google } from "@ai-sdk/google";

// Configure MCPClient to connect to your server(s)
export const mcp = new MCPClient({
  servers: {
    payman: {
      command: "node",
      args: [
        "/Users/hrishi0102/Developer/Experiments/payman_mcp/build/payman-server.js",
      ],
    },
  },
});
