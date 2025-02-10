import { Trans, t } from '@lingui/macro';
import { Button } from '@mantine/core';
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getTotpSecret, handleVerifyTotp } from '../../functions/auth';
import { QrRegistrationForm } from '../Index/Settings/AccountSettings/QrRegistrationForm';
import { Wrapper } from './LoginLayoutComponent';

export default function MfaSetup() {
  const navigate = useNavigate();
  const location = useLocation();

  const [totpQr, setTotpQr] = useState<{ totp_url: string; secret: string }>();
  const [value, setValue] = useState('');

  useEffect(() => {
    getTotpSecret(setTotpQr);
  }, []);

  return (
    <Wrapper titleText={t`MFA Setup Required`} logOff>
      <QrRegistrationForm
        url={totpQr?.totp_url ?? ''}
        secret={totpQr?.secret ?? ''}
        value={value}
        setValue={setValue}
      />
      <Button
        disabled={!value}
        onClick={handleVerifyTotp(value, navigate, location)}
      >
        <Trans>Add TOTP</Trans>
      </Button>
    </Wrapper>
  );
}
