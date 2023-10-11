import { t } from '@lingui/macro';
import { useMemo } from 'react';

import { ApiPaths, url } from '../../../states/ApiState';
import { TableColumn } from '../Column';
import { InvenTreeTable } from '../InvenTreeTable';
import { RowAction } from '../RowActions';

export function NotificationTable({
  params,
  tableKey,
  actions
}: {
  params: any;
  tableKey: string;
  actions: (record: any) => RowAction[];
}) {
  const columns: TableColumn[] = useMemo(() => {
    return [
      {
        accessor: 'age_human',
        title: t`Age`,
        sortable: true
      },
      {
        accessor: 'category',
        title: t`Category`,
        sortable: true
      },
      {
        accessor: `name`,
        title: t`Notification`
      },
      {
        accessor: 'message',
        title: t`Message`
      }
    ];
  }, []);

  return (
    <InvenTreeTable
      url={url(ApiPaths.notifications_list)}
      tableKey={tableKey}
      columns={columns}
      props={{
        rowActions: actions,
        enableSelection: true,
        params: params
      }}
    />
  );
}
