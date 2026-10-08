/**
 * Single chat bubble. Styling is finalized in Phase 8.
 */

import type { ChatMessage } from "@/lib/types";

export default function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-3 py-2 text-sm ${
          isUser
            ? "bg-kapruka-maroon text-white"
            : "bg-kapruka-cream text-kapruka-ink"
        }`}
      >
        {message.content}
      </div>
    </div>
  );
}
