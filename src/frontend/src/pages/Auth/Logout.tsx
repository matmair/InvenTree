import { useEffect } from 'react';
import { useNavigate } from '@tanstack/react-router';

import { doLogout } from '../../functions/auth';
import { Wrapper } from './Layout';

/* Expose a route for explicit logout via URL */
export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    doLogout(navigate);
  }, []);

  return <Wrapper titleText='Logging out' loader />;
}
