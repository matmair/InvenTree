import { t } from '@lingui/macro';
import {
  ActionIcon,
  Alert,
  Divider,
  Drawer,
  LoadingOverlay,
  Space,
  Tooltip
} from '@mantine/core';
import { Group, Stack, Text } from '@mantine/core';
import { IconBellCheck, IconBellPlus } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { api } from '../../App';
import { ApiPaths, apiUrl } from '../../states/ApiState';

/**
 * Construct a notification drawer.
 */
export function NotificationDrawer({
  opened,
  onClose
}: {
  opened: boolean;
  onClose: () => void;
}) {
  const navigate = useNavigate();

  const notificationQuery = useQuery({
    enabled: opened,
    queryKey: ['notifications', opened],
    queryFn: async () =>
      api
        .get(apiUrl(ApiPaths.notifications_list), {
          params: {
            read: false,
            limit: 10
          }
        })
        .then((response) => response.data)
        .catch((error) => {
          console.error('Error fetching notifications:', error);
          return error;
        }),
    refetchOnMount: false,
    refetchOnWindowFocus: false
  });

  return (
    <Drawer
      opened={opened}
      size="md"
      position="right"
      onClose={onClose}
      withCloseButton={false}
      styles={{
        header: {
          width: '100%'
        },
        title: {
          width: '100%'
        }
      }}
      title={
        <Group position="apart" noWrap={true}>
          <Text size="lg">{t`Notifications`}</Text>
          <ActionIcon
            onClick={() => {
              onClose();
              navigate('/notifications/');
            }}
          >
            <IconBellPlus />
          </ActionIcon>
        </Group>
      }
    >
      <Stack spacing="xs">
        <Divider />
        <LoadingOverlay visible={notificationQuery.isFetching} />
        {notificationQuery.data?.results?.length == 0 && (
          <Alert color="green">
            <Text size="sm">{t`You have no unread notifications.`}</Text>
          </Alert>
        )}
        {notificationQuery.data?.results.map((notification: any) => (
          <Group position="apart">
            <Stack spacing="3">
              <Text size="sm">{notification.target?.name ?? 'target'}</Text>
              <Text size="xs">{notification.age_human ?? 'name'}</Text>
            </Stack>
            <Space />
            <ActionIcon
              color="gray"
              variant="hover"
              onClick={() => {
                let url = apiUrl(ApiPaths.notifications_list, notification.pk);
                api
                  .patch(url, {
                    read: true
                  })
                  .then((response) => {
                    notificationQuery.refetch();
                  });
              }}
            >
              <Tooltip label={t`Mark as read`}>
                <IconBellCheck />
              </Tooltip>
            </ActionIcon>
          </Group>
        ))}
      </Stack>
    </Drawer>
  );
}
