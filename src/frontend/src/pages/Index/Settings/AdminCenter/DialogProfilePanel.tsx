import { t } from '@lingui/core/macro';
import { Stack } from '@mantine/core';

import { GlobalSettingList } from '../../../../components/settings/SettingList';
import DialogProfileTable from '../../../../tables/settings/DialogProfileTable';

/**
 * Panel for managing dialog profiles
 */
export default function DialogProfilePanel() {
  return (
    <Stack gap='xs'>
      <GlobalSettingList keys={['DIALOG_PROFILES_ENABLED']} />
      <DialogProfileTable />
    </Stack>
  );
}
