/**
 * Navigation utilities for TanStack Router
 * Provides compatibility layer between React Router v6 and TanStack Router
 */

import type { UseNavigateResult } from '@tanstack/react-router';

/**
 * Type alias for navigate function to maintain compatibility
 * TanStack Router's UseNavigateResult is similar to React Router's NavigateFunction
 */
export type NavigateFunction = (
  to: string | number,
  options?: { replace?: boolean; state?: any }
) => void;

/**
 * Wrapper to make TanStack Router's navigate work like React Router v6
 * This allows existing code to call navigate(path) or navigate({options})
 */
export function wrapNavigate(navigate: UseNavigateResult<string>): NavigateFunction {
  return (to: string | number, options?: { replace?: boolean; state?: any }) => {
    if (typeof to === 'number') {
      // Handle back/forward navigation
      window.history.go(to);
      return;
    }
    
    navigate({
      to: to as any,
      replace: options?.replace,
      state: options?.state
    } as any);
  };
}

/**
 * Helper to call navigate with a string path (React Router v6 style)
 * Wraps TanStack Router's navigate which expects an options object
 */
export function navigateTo(
  navigate: UseNavigateResult<string>,
  to: string | number,
  options?: { replace?: boolean; state?: any }
) {
  if (typeof to === 'number') {
    // Handle back/forward navigation
    window.history.go(to);
    return;
  }
  
  navigate({
    to: to as any,
    replace: options?.replace,
    state: options?.state
  } as any);
}

/**
 * Type for Link 'to' prop
 */
export type To = string;
