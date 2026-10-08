/**
 * Main chat transcript. Full interaction lands in Phase 8.
 */

export default function ChatWindow() {
  return (
    <section className="flex h-full flex-col rounded-2xl border border-kapruka-maroon/15 bg-white p-4 shadow-sm">
      <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-kapruka-maroon">
        Concierge
      </h2>
      <p className="text-sm text-kapruka-ink/70">
        Chat is scaffolded. The live agent loop is implemented in Phases 6–8.
      </p>
    </section>
  );
}
