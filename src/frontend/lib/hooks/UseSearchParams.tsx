/**
 * Custom hook that provides React Router v6-like useSearchParams behavior
 * This makes migration from React Router to TanStack Router easier
 */

import { useNavigate as useTanstackNavigate, useSearch } from '@tanstack/react-router';
import { useCallback, useMemo } from 'react';

/**
 * Hook that returns search params compatible with React Router v6
 * Returns [URLSearchParams, setSearchParams] tuple
 */
export function useSearchParams(): [URLSearchParams, (params: Record<string, any>) => void] {
  const search = useSearch({ strict: false }) as Record<string, any>;
  const navigate = useTanstackNavigate();

  const searchParams = useMemo(() => {
    const params = new URLSearchParams();
    if (search) {
      Object.entries(search).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.set(key, String(value));
        }
      });
    }
    return params;
  }, [search]);

  const setSearchParams = useCallback(
    (params: Record<string, any>) => {
      navigate({
        search: params as any
      } as any);
    },
    [navigate]
  );

  return [searchParams, setSearchParams];
}
