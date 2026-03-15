export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-zinc-950 px-4 text-zinc-50">
      <div className="max-w-xl space-y-3 text-center">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
          Diet Plan Timeline
        </h1>
        <p className="text-sm text-zinc-400 sm:text-base">
          Open <span className="font-mono text-zinc-100">/diet-plan</span> to
          view your structured daily diet plan with a vertical timeline.
        </p>
      </div>
    </main>
  );
}

