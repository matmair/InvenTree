import { t } from '@lingui/macro';
import { SimpleGrid, Stack } from '@mantine/core';
import { ReactNode, useMemo } from 'react';
import {
  Bar,
  BarChart,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';

import { CHART_COLORS } from '../../../components/charts/colors';
import { tooltipFormatter } from '../../../components/charts/tooltipFormatter';
import { formatCurrency } from '../../../defaults/formatters';
import { ApiEndpoints } from '../../../enums/ApiEndpoints';
import { ModelType } from '../../../enums/ModelType';
import { useTable } from '../../../hooks/UseTable';
import { apiUrl } from '../../../states/ApiState';
import { TableColumn } from '../../../tables/Column';
import { DateColumn, PartColumn } from '../../../tables/ColumnRenderers';
import { InvenTreeTable } from '../../../tables/InvenTreeTable';
import { NoPricingData } from './PricingPanel';

export default function VariantPricingPanel({
  part,
  pricing
}: {
  part: any;
  pricing: any;
}): ReactNode {
  const table = useTable('pricing-variants');

  const columns: TableColumn[] = useMemo(() => {
    return [
      {
        accessor: 'name',
        title: t`Variant Part`,
        sortable: true,
        switchable: false,
        render: (record: any) => PartColumn(record, true)
      },
      {
        accessor: 'pricing_min',
        title: t`Minimum Price`,
        sortable: true,
        switchable: false,
        render: (record: any) =>
          formatCurrency(record.pricing_min, { currency: pricing?.currency })
      },
      {
        accessor: 'pricing_max',
        title: t`Maximum Price`,
        sortable: true,
        switchable: false,
        render: (record: any) =>
          formatCurrency(record.pricing_max, { currency: pricing?.currency })
      },
      DateColumn({
        accessor: 'pricing_updated',
        title: t`Updated`,
        sortable: true,
        switchable: true
      })
    ];
  }, []);

  // Calculate pricing data for the part variants
  const variantPricingData: any[] = useMemo(() => {
    const pricing = table.records.map((variant: any) => {
      return {
        part: variant,
        name: variant.full_name,
        pmin: variant.pricing_min ?? variant.pricing_max ?? 0,
        pmax: variant.pricing_max ?? variant.pricing_min ?? 0
      };
    });

    return pricing;
  }, [table.records]);

  return (
    <Stack gap="xs">
      <SimpleGrid cols={2}>
        <InvenTreeTable
          tableState={table}
          url={apiUrl(ApiEndpoints.part_list)}
          columns={columns}
          props={{
            params: {
              ancestor: part?.pk,
              has_pricing: true
            },
            enablePagination: true,
            modelType: ModelType.part
          }}
        />
        {variantPricingData.length > 0 ? (
          <ResponsiveContainer width="100%" height={500}>
            <BarChart data={variantPricingData}>
              <XAxis dataKey="name" />
              <YAxis
                tickFormatter={(value, index) =>
                  formatCurrency(value, {
                    currency: pricing?.currency
                  })?.toString() ?? ''
                }
              />
              <Tooltip
                formatter={(label, payload) =>
                  tooltipFormatter(label, pricing?.currency)
                }
              />
              <Legend />
              <Bar
                dataKey="pmin"
                fill={CHART_COLORS[0]}
                label={t`Minimum Price`}
              />
              <Bar
                dataKey="pmax"
                fill={CHART_COLORS[1]}
                label={t`Maximum Price`}
              />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <NoPricingData />
        )}
      </SimpleGrid>
    </Stack>
  );
}
