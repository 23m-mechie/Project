export type Meal = {
  id: string;
  name: string;
  time: string;
  icon: string;
  items: string[];
  proteinG: number;
  accent: {
    border: string;
    badge: string;
    dot: string;
  };
};

export type DietSummary = {
  totalProtein: number;
  targetProtein: number;
};

