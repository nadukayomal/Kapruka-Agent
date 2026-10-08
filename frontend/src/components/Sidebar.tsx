/**
 * Session / recipient sidebar. Wired in Phase 8.
 */

export default function Sidebar() {
  return (
    <nav className="flex h-full flex-col gap-3 rounded-2xl bg-kapruka-maroon p-4 text-white">
      <p className="text-lg font-semibold">Kapruka Agent</p>
      <p className="text-sm text-white/80">Gift concierge for Sri Lanka</p>
      <div className="mt-4 text-sm">
        <p className="font-medium">Recipient</p>
        <p className="text-white/80">Mother · Kandy</p>
      </div>
    </nav>
  );
}
