import { t } from '@lingui/core/macro';
import { Trans } from '@lingui/react/macro';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { useEffect } from 'react';
import { useParams } from '@tanstack/react-router';
import { useNavigate } from '@lib/functions/navigation';

import { handleVerifyEmail } from '../../functions/auth';
import { Wrapper } from './Layout';

export default function VerifyEmail() {
  const { key } = useParams({ strict: false });
  const navigate = useNavigate();

  // make sure we have a key
  useEffect(() => {
    if (!key) {
      notifications.show({
        title: t`Key invalid`,
        message: t`You need to provide a valid key.`,
        color: 'red'
      });
      navigate('/login');
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
