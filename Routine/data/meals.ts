import type { Meal, DietSummary } from '@/types/diet';

export const meals: Meal[] = [
  {
    id: 'pre-gym',
    name: 'Pre-Gym',
    time: '6:30 AM',
    icon: '🌅',
    items: [
      'Chia seeds in lukewarm water',
      '2 tbsp peanut butter + 1 slice whole wheat bread'
    ],
    proteinG: 12,
    accent: {
      border: 'border-green-500',
      badge: 'bg-green-500/10 text-green-400',
      dot: 'bg-green-500'
    }
  },
  {
    id: 'post-gym',
    name: 'Post-Gym Breakfast',
    time: '8:15 AM',
    icon: '💪',
    items: [
      'Oats + full fat milk',
      'Seeds mix (flax, chia, pumpkin)',
      '2 tbsp peanut butter stirred in'
    ],
    proteinG: 22,
    accent: {
      border: 'border-cyan-500',
      badge: 'bg-cyan-500/10 text-cyan-400',
      dot: 'bg-cyan-500'
    }
  },
  {
    id: 'lunch',
    name: 'Lunch',
    time: '1:00 PM',
    icon: '🍱',
    items: [
      'Soya chunks curry',
      '1 bowl dal',
      '3 chapatis',
      'Seasonal vegetables + raw salad'
    ],
    proteinG: 40,
    accent: {
      border: 'border-violet-500',
      badge: 'bg-violet-500/10 text-violet-400',
      dot: 'bg-violet-500'
    }
  },
  {
    id: 'evening',
    name: 'Evening Snack',
    time: '5:00 PM',
    icon: '🌿',
    items: ['Small handful roasted peanuts (20–25g)'],
    proteinG: 7,
    accent: {
      border: 'border-amber-500',
      badge: 'bg-amber-500/10 text-amber-400',
      dot: 'bg-amber-500'
    }
  },
  {
    id: 'dinner',
    name: 'Dinner',
    time: '8:30 PM',
    icon: '🌙',
    items: [
      '100g paneer bhurji or rajma',
      'Curd (as side)',
      '2–3 chapatis or 1 small bowl rice',
      'Seasonal vegetables'
    ],
    proteinG: 28,
    accent: {
      border: 'border-red-500',
      badge: 'bg-red-500/10 text-red-400',
      dot: 'bg-red-500'
    }
  }
];

export const summary: DietSummary = {
  totalProtein: 109,
  targetProtein: 120
};

