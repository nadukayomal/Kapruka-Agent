/**
 * HTTP client for the FastAPI backend.
 * Chat/memory calls are wired in Phase 7–8; health is available now.
 */

const BACKEND =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000";

export async function fetchHealth(): Promise<{ status: string; env: string }> {
  const response = await fetch(`${BACKEND}/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

export async function sendChat(_message: string): Promise<never> {
  throw new Error("Chat API is implemented in Phase 7.");
}
