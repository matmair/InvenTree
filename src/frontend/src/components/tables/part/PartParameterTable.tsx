import { t } from '@lingui/macro';
import { ActionIcon, Text, Tooltip } from '@mantine/core';
import { IconTextPlus } from '@tabler/icons-react';
import { useCallback, useMemo } from 'react';

import {
  openCreateApiForm,
  openDeleteApiForm,
  openEditApiForm
} from '../../../functions/forms';
import { useTableRefresh } from '../../../hooks/TableRefresh';
import { ApiPaths, apiUrl } from '../../../states/ApiState';
import { YesNoButton } from '../../items/YesNoButton';
import { TableColumn } from '../Column';
import { InvenTreeTable } from '../InvenTreeTable';

/**
 * Construct a table listing parameters for a given part
 */
export function PartParameterTable({ partId }: { partId: any }) {
  const { tableKey, refreshTable } = useTableRefresh('part-parameters');

  const tableColumns: TableColumn[] = useMemo(() => {
    return [
      {
        accessor: 'name',
        title: t`Parameter`,
        switchable: false,
        sortable: true,
        render: (record) => record.template_detail?.name
      },
      {
        accessor: 'description',
        title: t`Description`,
        sortable: false,
        switchable: true,
        render: (record) => record.template_detail?.description
      },
      {
        accessor: 'data',
        title: t`Value`,
        switchable: false,
        sortable: true,
        render: (record) => {
          let template = record.template_detail;

          if (template?.checkbox) {
            return <YesNoButton value={record.data} />;
          }

          if (record.data_numeric) {
            // TODO: Numeric data
          }

          // TODO: Units

          return record.data;
        }
      },
      {
        accessor: 'units',
        title: t`Units`,
        switchable: true,
        sortable: true,
        render: (record) => record.template_detail?.units
      }
    ];
  }, []);

  // Callback for row actions
  // TODO: Adjust based on user permissions
  const rowActions = useCallback((record: any) => {
    let actions = [];

    actions.push({
      title: t`Edit`,
      onClick: () => {
        openEditApiForm({
          name: 'edit-part-parameter',
          url: ApiPaths.part_parameter_list,
          pk: record.pk,
          title: t`Edit Part Parameter`,
          fields: {
            part: {
              hidden: true
            },
            template: {},
            data: {}
          },
          successMessage: t`Part parameter updated`,
          onFormSuccess: refreshTable
        });
      }
    });

    actions.push({
      title: t`Delete`,
      color: 'red',
      onClick: () => {
        openDeleteApiForm({
          name: 'delete-part-parameter',
          url: ApiPaths.part_parameter_list,
          pk: record.pk,
          title: t`Delete Part Parameter`,
          successMessage: t`Part parameter deleted`,
          onFormSuccess: refreshTable,
          preFormContent: (
            <Text>{t`Are you sure you want to remove this parameter?`}</Text>
          )
        });
      }
    });

    return actions;
  }, []);

  const addParameter = useCallback(() => {
    if (!partId) {
      return;
    }

    openCreateApiForm({
      name: 'add-part-parameter',
      url: ApiPaths.part_parameter_list,
      title: t`Add Part Parameter`,
      fields: {
        part: {
          hidden: true,
          value: partId
        },
        template: {},
        data: {}
      },
      successMessage: t`Part parameter added`,
      onFormSuccess: refreshTable
    });
  }, [partId]);

  // Custom table actions
  const tableActions = useMemo(() => {
    let actions = [];

    // TODO: Hide if user does not have permission to edit parts
    actions.push(
      <Tooltip label={t`Add parameter`}>
        <ActionIcon radius="sm" onClick={addParameter}>
          <IconTextPlus color="green" />
        </ActionIcon>
      </Tooltip>
    );

    return actions;
  }, []);

  return (
    <InvenTreeTable
      url={apiUrl(ApiPaths.part_parameter_list)}
      tableKey={tableKey}
      columns={tableColumns}
      props={{
        rowActions: rowActions,
        customActionGroups: tableActions,
        params: {
          part: partId,
          template_detail: true
        }
      }}
    />
  );
}
