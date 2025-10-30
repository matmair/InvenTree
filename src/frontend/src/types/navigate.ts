// Type alias for navigate function from TanStack Router
// This is used to maintain compatibility with code that expects NavigateFunction type
import { useNavigate } from '@tanstack/react-router';

export type NavigateFunction = ReturnType<typeof useNavigate>;
