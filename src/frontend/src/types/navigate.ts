// Type alias for navigate function from TanStack Router
// This is used to maintain compatibility with code that expects NavigateFunction type
import type { UseNavigateResult } from '@tanstack/react-router';

export type NavigateFunction = UseNavigateResult<any>;
