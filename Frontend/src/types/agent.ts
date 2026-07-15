export type AgentAction =   | "answer"  | "clarify"  | "decline";


export interface AgentResponse {
  response: string;
  action: AgentAction;
  confidence?: number;
  source?: string;
  category?: string;
}


export interface Message {
  id: number;
  role: "user" | "bot";
  content: string;
  data?: AgentResponse;
}


export interface HealthResponse {
  vector_store_count: number;
}