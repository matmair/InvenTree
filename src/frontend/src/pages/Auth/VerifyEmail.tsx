import { t } from '@lingui/core/macro';
import { Trans } from '@lingui/react/macro';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { useNavigate, useParams } from '@tanstack/react-router';
import { useEffect } from 'react';

import { handleVerifyEmail } from '../../functions/auth';
import { Wrapper } from './Layout';

export default function VerifyEmail() {
  const { key } = useParams({ from: '/authLayout/verify-email/$key' });
  const navigate = useNavigate();

  // make sure we have a key
  useEffect(() => {
    if (!key) {
      notifications.show({
        title: t`Key invalid`,
        message: t`You need to provide a valid key.`,
        color: 'red'
      });
      navigate({ to: '/login' });
    }
  }, [key]);

  return (
    <Wrapper titleText={t`Verify Email`}>
      <Button type='submit' onClick={() => handleVerifyEmail(key, navigate)}>
        <Trans>Verify</Trans>
      </Button>
    </Wrapper>
  );
}
