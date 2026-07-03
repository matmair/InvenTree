import { t } from '@lingui/core/macro';
import { useCallback, useMemo, useState } from 'react';

import { AddItemButton } from '@lib/components/AddItemButton';
import {
  type RowAction,
  RowDeleteAction,
  RowEditAction
} from '@lib/components/RowActions';
import { ApiEndpoints } from '@lib/enums/ApiEndpoints';
import { UserRoles } from '@lib/enums/Roles';
import { apiUrl } from '@lib/functions/Api';
import useTable from '@lib/hooks/UseTable';
import type { TableFilter } from '@lib/index';
import type { TableColumn } from '@lib/types/Tables';
import {
  useCreateApiFormModal,
  useDeleteApiFormModal,
  useEditApiFormModal
} from '../../hooks/UseForm';
import { useUserState } from '../../states/UserState';
import { BooleanColumn, DescriptionColumn } from '../ColumnRenderers';
import { InvenTreeTable } from '../InvenTreeTable';

export function dialogProfileFields() {
  return {
    name: {},
    description: {},
    enabled: {},
    definition: {
      // Use a basic text field for JSON for now
    }
  };
}

/**
 * Table for displaying list of dialog profiles
 */
export default function DialogProfileTable() {
  const table = useTable('dialog-profiles');

  const user = useUserState();

  const columns: TableColumn[] = useMemo(() => {
    return [
      {
        accessor: 'name',
        sortable: true
      },
      DescriptionColumn({}),
      BooleanColumn({
        accessor: 'enabled'
      }),
      {
        accessor: 'definition',
        title: t`Definition`,
        render: (record: any) => JSON.stringify(record.definition)
      }
    ];
  }, []);

  const newDialogProfile = useCreateApiFormModal({
    url: ApiEndpoints.dialog_profile_list,
    title: t`Add Dialog Profile`,
    fields: dialogProfileFields(),
    table: table
  });

  const [selectedDialogProfile, setSelectedDialogProfile] = useState<
    number | undefined
  >(undefined);

  const editDialogProfile = useEditApiFormModal({
    url: ApiEndpoints.dialog_profile_list,
    pk: selectedDialogProfile,
    title: t`Edit Dialog Profile`,
    fields: dialogProfileFields(),
    table: table
  });

  const deleteDialogProfile = useDeleteApiFormModal({
    url: ApiEndpoints.dialog_profile_list,
    pk: selectedDialogProfile,
    title: t`Delete Dialog Profile`,
    table: table
  });

  const rowActions = useCallback(
    (record: any): RowAction[] => {
      return [
        RowEditAction({
          hidden: !user.hasChangeRole(UserRoles.admin),
          onClick: () => {
            setSelectedDialogProfile(record.pk);
            editDialogProfile.open();
          }
        }),
        RowDeleteAction({
          hidden: !user.hasDeleteRole(UserRoles.admin),
          onClick: () => {
            setSelectedDialogProfile(record.pk);
            deleteDialogProfile.open();
          }
        })
      ];
    },
    [user]
  );

  const tableFilters: TableFilter[] = useMemo(() => {
    return [
      {
        name: 'enabled',
        label: t`Enabled`,
        description: t`Show enabled items`,
        type: 'boolean'
      }
    ];
  }, []);

  const tableActions = useMemo(() => {
    return [
      <AddItemButton
        key='add'
        onClick={() => newDialogProfile.open()}
        tooltip={t`Add dialog profile`}
      />
    ];
  }, []);

  return (
    <>
      {newDialogProfile.modal}
      {editDialogProfile.modal}
      {deleteDialogProfile.modal}
      <InvenTreeTable
        url={apiUrl(ApiEndpoints.dialog_profile_list)}
        tableState={table}
        columns={columns}
        props={{
          rowActions: rowActions,
          tableActions: tableActions,
          tableFilters: tableFilters,
          enableDownload: true
        }}
      />
    </>
  );
}
