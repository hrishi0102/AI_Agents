import { Mastra } from "@mastra/core/mastra";
import { createLogger } from "@mastra/core/logger";
import { LibSQLStore } from "@mastra/libsql";
import { weatherWorkflow } from "./workflows";
import { weatherAgent } from "./agents";
import { mcp_agent } from "./agents/mcp-agent";

export const mastra = new Mastra({
  workflows: { weatherWorkflow },
  agents: { weatherAgent, mcp_agent },
  storage: new LibSQLStore({
    // stores telemetry, evals, ... into memory storage, if it needs to persist, change to file:../mastra.db
    url: ":memory:",
  }),
  logger: createLogger({
    name: "Mastra",
    level: "info",
  }),
});
