/**
 * Custom hook that provides React Router v6-like useNavigate behavior
 * This makes migration from React Router to TanStack Router easier
 */

import { useNavigate as useTanstackNavigate } from '@tanstack/react-router';
import { useCallback } from 'react';

export type NavigateOptions = {
  replace?: boolean;
  state?: any;
};

export type NavigateFunction = (
  to: string | number,
  options?: NavigateOptions
) => void;

/**
 * Hook that returns a navigate function compatible with React Router v6
 */
export function useNavigate(): NavigateFunction {
  const tanstackNavigate = useTanstackNavigate();

  return useCallback(
    ((to: string | number, options?: NavigateOptions) => {
      if (typeof to === 'number') {
        window.history.go(to);
        return;
      }

      tanstackNavigate({
        to: to as any,
        replace: options?.replace,
        state: options?.state
      } as any);
    }) as NavigateFunction,
    [tanstackNavigate]
  );
}
