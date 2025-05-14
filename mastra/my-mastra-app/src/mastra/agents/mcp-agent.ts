import { mcp } from "../mcp";
import { Agent } from "@mastra/core/agent";
import { Memory } from "@mastra/memory";
import { google } from "@ai-sdk/google";
import { LibSQLStore } from "@mastra/libsql";

// Create an agent and add tools from the MCP client
export const mcp_agent = new Agent({
  name: "Agent with Payman MCP Tools",
  instructions:
    "You can use tools from connected MCP servers to create payees, send payments, set up api key and search payees.",
  model: google("gemini-1.5-flash"),
  memory: new Memory({
    storage: new LibSQLStore({
      url: "file:../mastra.db", // path is relative to the .mastra/output directory
    }),
    options: {
      lastMessages: 10,
      semanticRecall: false,
      threads: {
        generateTitle: false,
      },
    },
  }),
  tools: await mcp.getTools(),
});
