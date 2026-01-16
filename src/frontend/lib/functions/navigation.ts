/**
 * Navigation utilities for TanStack Router
 * Provides compatibility layer between React Router v6 and TanStack Router
 */

// Export types and functions from custom hooks
export type { NavigateFunction, NavigateOptions } from '../hooks/UseNavigate';
export { useNavigate } from '../hooks/UseNavigate';
export { useSearchParams } from '../hooks/UseSearchParams';

/**
 * Type for Link 'to' prop
 */
export type To = string;
