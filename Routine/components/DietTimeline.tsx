'use client';

import { FC, useMemo } from 'react';
import { Dumbbell, Target } from 'lucide-react';
import { meals, summary } from '@/data/meals';
import { MealCard } from '@/components/MealCard';

export const DietTimeline: FC = () => {
  const proteinRatio = useMemo(() => {
    if (!summary.targetProtein) return 0;
    return Math.min(1, summary.totalProtein / summary.targetProtein);
  }, []);

  const proteinPercent = Math.round(proteinRatio * 100);

  return (
    <main className="min-h-screen bg-zinc-950 px-4 py-10 text-zinc-50 sm:px-6 lg:px-8">
      <section className="mx-auto flex max-w-xl flex-col gap-8">
        <header className="space-y-3 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300">
            <Dumbbell className="h-3.5 w-3.5" />
            Daily Diet Plan Timeline
          </div>

          <div className="space-y-1">
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
              Structured High-Protein Day
            </h1>
            <p className="text-sm text-zinc-400 sm:text-[15px]">
              A simple, sustainable meal flow to support training, recovery, and
              overall energy across the day.
            </p>
          </div>
        </header>

        <section className="rounded-2xl border border-zinc-800 bg-zinc-900/80 p-4 shadow-[0_20px_60px_rgba(0,0,0,0.65)] backdrop-blur">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-300">
                <Target className="h-5 w-5" />
              </div>
              <div>
                <p className="text-xs font-medium text-zinc-400">
                  Protein coverage
                </p>
                <p className="text-sm font-semibold text-zinc-50">
                  {summary.totalProtein}g / {summary.targetProtein}g target
                </p>
              </div>
            </div>

            <span className="rounded-full bg-zinc-900 px-2.5 py-1 text-[11px] font-medium text-zinc-300">
              ~{proteinPercent}% of daily goal
            </span>
          </div>

          <div className="mt-3 h-2 rounded-full bg-zinc-800">
            <div
              className="h-full rounded-full bg-gradient-to-r from-emerald-500 via-cyan-500 to-rose-500 transition-[width]"
              style={{ width: `${proteinPercent}%` }}
            />
          </div>

          <p className="mt-2 text-xs text-zinc-500">
            Aim to hit or slightly exceed this range consistently over the week
            for best results.
          </p>
        </section>

        <section className="relative pb-6">
          <div className="pointer-events-none absolute left-3.5 top-1 bottom-4 w-px bg-gradient-to-b from-green-500 via-cyan-500 via-violet-500 via-amber-500 to-red-500" />

          <div className="space-y-4 pl-6">
            {meals.map((meal, idx) => (
              <MealCard key={meal.id} meal={meal} index={idx} />
            ))}
          </div>
        </section>

        <footer className="pb-2 text-center text-[11px] text-zinc-500">
          Listen to your hunger cues, hydrate well, and feel free to swap
          similar foods within each block.
        </footer>
      </section>
    </main>
  );
};

