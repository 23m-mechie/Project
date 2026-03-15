import { FC } from 'react';
import { motion } from 'framer-motion';
import type { Meal } from '@/types/diet';
import { Dot } from 'lucide-react';

type MealCardProps = {
  meal: Meal;
  index: number;
};

export const MealCard: FC<MealCardProps> = ({ meal, index }) => {
  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.45, delay: index * 0.06, ease: 'easeOut' }}
      className={`relative flex flex-col gap-3 rounded-xl border-l-4 bg-zinc-900/80 border-zinc-800/80 px-4 py-4 sm:px-5 sm:py-5 shadow-[0_20px_60px_rgba(0,0,0,0.6)] backdrop-blur ${meal.accent.border}`}
    >
      <div className="absolute -left-[1.22rem] top-5 flex h-4 w-4 items-center justify-center">
        <div
          className={`h-3 w-3 rounded-full ring-4 ring-zinc-950 ${meal.accent.dot}`}
        />
      </div>

      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-zinc-800/80 text-lg">
            <span aria-hidden>{meal.icon}</span>
          </div>
          <div className="flex flex-col">
            <h3 className="text-sm font-semibold text-zinc-50 sm:text-base">
              {meal.name}
            </h3>
            <p className="text-xs text-zinc-500 sm:text-[13px]">
              Structured, balanced meal
            </p>
          </div>
        </div>

        <span className="inline-flex items-center rounded-full border border-zinc-800 bg-zinc-900/60 px-2 py-1 text-[11px] font-medium text-zinc-300 shadow-sm">
          <Dot className="mr-1 h-3 w-3 text-zinc-500" />
          {meal.time}
        </span>
      </div>

      <ul className="mt-1 space-y-1.5 text-sm text-zinc-400">
        {meal.items.map((item) => (
          <li key={item} className="flex gap-2">
            <span className="mt-[7px] h-1.5 w-1.5 flex-shrink-0 rounded-full bg-zinc-600" />
            <span className="leading-relaxed">{item}</span>
          </li>
        ))}
      </ul>

      <div className="mt-2 flex items-center justify-between text-xs">
        <span
          className={`inline-flex items-center rounded-full px-2.5 py-1 font-medium ${meal.accent.badge}`}
        >
          ~{meal.proteinG}g protein
        </span>
        <span className="text-[11px] text-zinc-500">
          Prioritize chewing & slow eating
        </span>
      </div>
    </motion.article>
  );
};

