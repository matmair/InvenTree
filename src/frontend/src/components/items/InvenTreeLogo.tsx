import { t } from '@lingui/core/macro';
import { ActionIcon } from '@mantine/core';
import { Link } from '@tanstack/react-router';
import { forwardRef } from 'react';

import InvenTreeIcon from './inventree.svg';

export const InvenTreeLogoHomeButton = forwardRef<HTMLDivElement>(
  (props, ref) => {
    return (
      <div ref={ref} {...props}>
        <Link to={'/'}>
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
