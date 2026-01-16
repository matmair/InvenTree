import { t } from '@lingui/core/macro';
import { ActionIcon } from '@mantine/core';
import { forwardRef } from 'react';
import { Link } from '@tanstack/react-router';

import InvenTreeIcon from './inventree.svg';

export const InvenTreeLogoHomeButton = forwardRef<HTMLDivElement>(
  (props, ref) => {
    return (
      <div ref={ref} {...props}>
        <Link to={'/' as any}>
          <ActionIcon size={28} variant='transparent'>
            <InvenTreeLogo />
          </ActionIcon>
        </Link>
      </div>
    );
  }
);

export const InvenTreeLogo = () => {
  return <img src={InvenTreeIcon} alt={t`InvenTree Logo`} height={28} />;
};
