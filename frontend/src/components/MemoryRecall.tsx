/**
 * Displays semantic memory (recipient allergies and preferences).
 */

import type { MemoryRecall } from "@/lib/types";

export default function MemoryRecallPanel({ memory }: { memory?: MemoryRecall }) {
  return (
    <aside className="rounded-2xl border border-kapruka-maroon/15 bg-white p-4">
      <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-kapruka-maroon">
        Memory Recall
      </h2>
      {memory ? (
        <ul className="space-y-1 text-sm">
          <li>Recipient: {memory.recipientId}</li>
          <li>District: {memory.district ?? "unknown"}</li>
          <li>Allergies: {memory.allergies.join(", ") || "none"}</li>
        </ul>
      ) : (
        <p className="text-sm text-kapruka-ink/60">
          Seed profile: mother in Kandy, nut-free (wired in Phase 3).
        </p>
      )}
    </aside>
  );
}
