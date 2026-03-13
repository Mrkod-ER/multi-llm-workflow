import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Utility for safely merging Tailwind classes */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
