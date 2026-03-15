'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight, Briefcase, Salad } from 'lucide-react';

const containerVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: 'easeOut',
      when: 'beforeChildren',
      staggerChildren: 0.15
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.35, ease: 'easeOut' } }
};

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-zinc-950 px-4 text-zinc-50">
      <motion.section
        className="mx-auto flex w-full max-w-3xl flex-col gap-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.header variants={itemVariants}>
          <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Hi, I&apos;m Sonu 👋
          </h1>
          <p className="mt-2 text-base text-zinc-400 sm:text-lg">
            Let&apos;s keep track of your health &amp; education — one day at a time.
          </p>
        </motion.header>

        <motion.div
          className="grid gap-4 sm:grid-cols-2"
          variants={containerVariants}
        >
          <motion.div variants={itemVariants}>
            <Link
              href="/dietPlan"
              className="group block rounded-2xl border border-zinc-800 bg-zinc-900 p-5 transition-transform transition-colors duration-200 hover:scale-[1.02] hover:border-green-400/80"
            >
              <div className="flex gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-500/10 text-green-400">
                  <Salad className="h-5 w-5" aria-hidden="true" />
                </div>
                <div className="flex flex-1 flex-col">
                  <h2 className="text-sm font-semibold text-white sm:text-base">
                    Diet Plan
                  </h2>
                  <p className="mt-1 text-xs text-zinc-400 sm:text-sm">
                    Track your daily meals, protein intake and nutrition goals.
                  </p>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between text-xs sm:text-sm">
                <span className="font-medium text-green-400">Open /dietPlan</span>
                <ArrowRight className="h-4 w-4 text-green-400 transition-transform duration-200 group-hover:translate-x-0.5" />
              </div>
            </Link>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Link
              href="/switch"
              className="group block rounded-2xl border border-zinc-800 bg-zinc-900 p-5 transition-transform transition-colors duration-200 hover:scale-[1.02] hover:border-violet-400/80"
            >
              <div className="flex gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400">
                  <Briefcase className="h-5 w-5" aria-hidden="true" />
                </div>
                <div className="flex flex-1 flex-col">
                  <h2 className="text-sm font-semibold text-white sm:text-base">
                    Switch Tracker
                  </h2>
                  <p className="mt-1 text-xs text-zinc-400 sm:text-sm">
                    Track job applications, interview prep and your switch timeline.
                  </p>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between text-xs sm:text-sm">
                <span className="font-medium text-violet-400">Open /switch</span>
                <ArrowRight className="h-4 w-4 text-violet-400 transition-transform duration-200 group-hover:translate-x-0.5" />
              </div>
            </Link>
          </motion.div>
        </motion.div>
      </motion.section>
    </main>
  );
}

