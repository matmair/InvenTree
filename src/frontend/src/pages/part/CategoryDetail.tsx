import { t } from '@lingui/macro';
import { LoadingOverlay, Stack, Text } from '@mantine/core';
import {
  IconCategory,
  IconListDetails,
  IconSitemap
} from '@tabler/icons-react';
import { useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';

import { PlaceholderPanel } from '../../components/items/Placeholder';
import { PageDetail } from '../../components/nav/PageDetail';
import { PanelGroup, PanelType } from '../../components/nav/PanelGroup';
import { PartCategoryTree } from '../../components/nav/PartCategoryTree';
import { PartCategoryTable } from '../../components/tables/part/PartCategoryTable';
import { PartListTable } from '../../components/tables/part/PartTable';
import { ApiPaths } from '../../enums/ApiEndpoints';
import { useInstance } from '../../hooks/UseInstance';

/**
 * Detail view for a single PartCategory instance.
 *
 * Note: If no category ID is supplied, this acts as the top-level part category page
 */
export default function CategoryDetail({}: {}) {
  const { id } = useParams();

  const [treeOpen, setTreeOpen] = useState(false);

  const {
    instance: category,
    refreshInstance,
    instanceQuery
  } = useInstance({
    endpoint: ApiPaths.category_list,
    pk: id,
    params: {
      path_detail: true
    }
  });

  const categoryPanels: PanelType[] = useMemo(
    () => [
      {
        name: 'parts',
        label: t`Parts`,
        icon: <IconCategory />,
        content: (
          <PartListTable
            props={{
              params: {
                category: id
              }
            }}
          />
        )
      },
      {
        name: 'subcategories',
        label: t`Part Categories`,
        icon: <IconSitemap />,
        content: (
          <PartCategoryTable
            params={{
              parent: id
            }}
          />
        )
      },
      {
        name: 'parameters',
        label: t`Parameters`,
        icon: <IconListDetails />,
        content: <PlaceholderPanel />
      }
    ],
    [category, id]
  );

  const breadcrumbs = useMemo(
    () => [
      { name: t`Parts`, url: '/part' },
      ...(category.path ?? []).map((c: any) => ({
        name: c.name,
        url: `/part/category/${c.pk}`
      }))
    ],
    [category]
  );

  return (
    <Stack spacing="xs">
      <LoadingOverlay visible={instanceQuery.isFetching} />
      <PartCategoryTree
        opened={treeOpen}
        onClose={() => {
          setTreeOpen(false);
        }}
        selectedCategory={category?.pk}
      />
      <PageDetail
        title={t`Part Category`}
        detail={<Text>{category.name ?? 'Top level'}</Text>}
        breadcrumbs={breadcrumbs}
        breadcrumbAction={() => {
          setTreeOpen(true);
        }}
      />
      <PanelGroup pageKey="partcategory" panels={categoryPanels} />
    </Stack>
  );
}
