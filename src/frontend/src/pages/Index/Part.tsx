import { Trans } from '@lingui/macro';
import { Group } from '@mantine/core';

import { Text } from '@mantine/core';
import { DataTable } from 'mantine-datatable';

import { PlaceholderPill } from '../../components/items/Placeholder';
import { StylishText } from '../../components/items/StylishText';

import { PartTable } from '../../components/tables/PartTable';

export default function Part() {
  return (
    <>
    <Group>
      <StylishText>
        <Trans>Parts</Trans>
      </StylishText>
      <PlaceholderPill />
    </Group>
    <PartTable />
    </>
  );
}
