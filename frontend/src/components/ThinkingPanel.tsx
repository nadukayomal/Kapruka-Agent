/**
 * Shows Draft → Critique → Revise steps from the reflection loop (Phase 8).
 */

import type { ThinkingStep } from "@/lib/types";

export default function ThinkingPanel({ steps = [] }: { steps?: ThinkingStep[] }) {
  return (
    <aside className="rounded-2xl border border-kapruka-gold/40 bg-white p-4">
      <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-kapruka-maroon">
        Thinking
      </h2>
      {steps.length === 0 ? (
        <p className="text-sm text-kapruka-ink/60">Waiting for the reflection loop.</p>
      ) : (
        <ol className="space-y-2 text-sm">
          {steps.map((step, index) => (
            <li key={`${step.stage}-${index}`}>
              <span className="font-medium capitalize">{step.stage}:</span> {step.detail}
            </li>
          ))}
        </ol>
      )}
    </aside>
  );
}
