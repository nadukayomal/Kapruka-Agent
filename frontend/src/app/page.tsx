import ChatWindow from "@/components/ChatWindow";
import MemoryRecallPanel from "@/components/MemoryRecall";
import Sidebar from "@/components/Sidebar";
import ThinkingPanel from "@/components/ThinkingPanel";

export default function HomePage() {
  return (
    <main className="mx-auto grid min-h-screen max-w-6xl grid-cols-1 gap-4 p-4 md:grid-cols-[220px_1fr_280px]">
      <Sidebar />
      <ChatWindow />
      <div className="flex flex-col gap-4">
        <ThinkingPanel />
        <MemoryRecallPanel />
      </div>
    </main>
  );
}
