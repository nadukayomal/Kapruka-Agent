/**
 * Shared TypeScript types for the concierge UI.
 * Chat streaming shapes will expand in Phase 8.
 */

export type ChatRole = "user" | "assistant" | "system";

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
}

export interface ThinkingStep {
  stage: "draft" | "critique" | "revise" | "route" | "search";
  detail: string;
}

export interface MemoryRecall {
  recipientId: string;
  allergies: string[];
  preferences: string[];
  district?: string;
}
