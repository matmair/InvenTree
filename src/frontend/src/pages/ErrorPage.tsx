import { t } from '@lingui/core/macro';
import { useDocumentTitle } from '@mantine/hooks';
import { useState } from 'react';

import type { ErrorResponse } from '@lib/types/Auth';
import GenericErrorPage from '../components/errors/GenericErrorPage';

export default function ErrorPage() {
  const [title] = useState(t`Error`);
  useDocumentTitle(title);

  return (
    <GenericErrorPage
      title={title}
      message={t`An unexpected error has occurred`}
    />
  );
}
