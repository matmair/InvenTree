import { t } from '@lingui/macro';
import { Trans } from '@lingui/macro';

import { Group, Text } from '@mantine/core';

import { shortenString } from '../../functions/tables';

import { Thumbnail } from '../items/Thumbnail';

import { InvenTreeTable } from './InvenTreeTable';

export function PartTable({
    params={}
  }: {
    params?: any;
  }) {

    let tableParams = Object.assign({}, params);
    
    // Add required query parmeters
    tableParams.category_detail = true;

    return <InvenTreeTable
        url='part/'
        params={tableParams}
        tableKey='part-table'
        columns={[
          {
            accessor: 'name',
            sortable: true,
            title: t`Part`,
            render: function(record: any) {

              // TODO - Link to the part detail page

              return <Group position="left">
                <Thumbnail
                  src={record.thumbnail || record.image}
                  alt={record.name}
                />
                <Text>{record.name}</Text>
              </Group>;
            }
          },
          {
            accessor: 'IPN',
            title: t`IPN`,
            sortable: true,
          },
          {
            accessor: 'units',
            sortable: true,
            title: t`Units`
          },
          {
            accessor: 'description',
            title: t`Description`,
            sortable: true,
          },
          {
            accessor: 'category',
            title: t`Category`,
            sortable: true,
            render: function(record: any) {
              // TODO: Link to the category detail page
              return shortenString({
                str: record.category_detail.pathstring,
              });
            }
          },
          {
            accessor: 'total_in_stock',
            title: t`Stock`,
            sortable: true,
          },
          {
            accessor: 'price_range',
            title: t`Price Range`,
            sortable: false,
            render: function(record: any) {
              // TODO: Render price range
              return "-- price --";
            }
          },
          {
            accessor: 'link',
            title: t`Link`,
          }
        ]}
    />;

}