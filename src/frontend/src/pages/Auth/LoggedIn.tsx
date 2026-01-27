import { t } from '@lingui/core/macro';
import { useDebouncedCallback } from '@mantine/hooks';
import { useLocation, useNavigate } from '@tanstack/react-router';
import { useEffect } from 'react';

import { checkLoginState } from '../../functions/auth';
import { Wrapper } from './Layout';

export default function Logged_In() {
  const navigate = useNavigate();
  const location = useLocation();
  const checkLoginStateDebounced = useDebouncedCallback(checkLoginState, 300);

  useEffect(() => {
    checkLoginStateDebounced(navigate, location?.state);
  }, [navigate]);

  return (
    <Wrapper titleText={t`Checking if you are already logged in`} loader />
  );
}
