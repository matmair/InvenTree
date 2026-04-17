import { t } from '@lingui/core/macro';
import { Stack } from '@mantine/core';
import {
  IconCalendar,
  IconListDetails,
  IconTable,
  IconTools
} from '@tabler/icons-react';
import { useMemo } from 'react';

import { PageDetail } from '@lib/components/nav/PageDetail';
import { PanelGroup } from '@lib/components/nav/PanelGroup';
import SegmentedControlPanel from '@lib/components/nav/SegmentedControlPanel';
import { ModelType } from '@lib/enums/ModelType';
import { UserRoles } from '@lib/enums/Roles';
import type { TableFilter } from '@lib/types/Filters';
import type { PanelType } from '@lib/types/Panel';
import { useLocalStorage } from '@mantine/hooks';
import OrderCalendar from '../../components/calendar/OrderCalendar';
import PermissionDenied from '../../components/errors/PermissionDenied';
import { useGlobalSettingsState } from '../../states/SettingsStates';
import { useUserState } from '../../states/UserState';
import { PartCategoryFilter } from '../../tables/Filter';
import BuildOrderParametricTable from '../../tables/build/BuildOrderParametricTable';
import { BuildOrderTable } from '../../tables/build/BuildOrderTable';

function BuildOrderCalendar() {
  const globalSettings = useGlobalSettingsState();

  const calendarFilters: TableFilter[] = useMemo(() => {
    return [
      {
        name: 'external',
        label: t`External`,
        description: t`Show external build orders`,
        active: globalSettings.isSet('BUILDORDER_EXTERNAL_BUILDS')
      },
      PartCategoryFilter()
    ];
  }, [globalSettings]);

  return (
    <OrderCalendar
      model={ModelType.build}
      role={UserRoles.build}
      params={{ outstanding: true }}
      filters={calendarFilters}
    />
  );
}

/**
 * Build Order index page
 */
export default function BuildIndex() {
  const user = useUserState();

  const [buildOrderView, setBuildOrderView] = useLocalStorage<string>({
    key: 'build-order-view',
    defaultValue: 'table'
  });

  const panels: PanelType[] = useMemo(() => {
    return [
      SegmentedControlPanel({
        name: 'buildorder',
        label: t`Build Orders`,
        icon: <IconTools />,
        selection: buildOrderView,
        onChange: setBuildOrderView,
        options: [
          {
            value: 'table',
            label: t`Table View`,
            icon: <IconTable />,
            content: <BuildOrderTable />
          },
          {
            value: 'calendar',
            label: t`Calendar View`,
            icon: <IconCalendar />,
            content: <BuildOrderCalendar />
          },
          {
            value: 'parametric',
            label: t`Parametric View`,
            icon: <IconListDetails />,
            content: <BuildOrderParametricTable />
          }
        ]
      })
    ];
  }, [user, buildOrderView]);

  if (!user.isLoggedIn() || !user.hasViewRole(UserRoles.build)) {
    return <PermissionDenied />;
  }

  return (
    <Stack>
      <PageDetail title={t`Manufacturing`} actions={[]} />
      <PanelGroup
        pageKey='build-index'
        panels={panels}
        model='manufacturing'
        id={null}
      />
    </Stack>
  );
}
