import { t } from '@lingui/macro';
import { Text } from '@mantine/core';

import { ApiFormFieldSet } from '../../components/forms/fields/ApiFormField';
import { ApiPaths } from '../../states/ApiState';
import {
  openCreateApiForm,
  openDeleteApiForm,
  openEditApiForm
} from '../forms';

export function attachmentFields(editing: boolean): ApiFormFieldSet {
  let fields: ApiFormFieldSet = {
    attachment: {},
    comment: {}
  };

  if (editing) {
    delete fields['attachment'];
  }

  return fields;
}

/**
 * Add a new attachment (either a file or a link)
 */
export function addAttachment({
  endpoint,
  model,
  pk,
  attachmentType,
  callback
}: {
  endpoint: ApiPaths;
  model: string;
  pk: number;
  attachmentType: 'file' | 'link';
  callback?: () => void;
}) {
  let formFields: ApiFormFieldSet = {
    attachment: {},
    link: {},
    comment: {}
  };

  if (attachmentType === 'link') {
    delete formFields['attachment'];
  } else {
    delete formFields['link'];
  }

  formFields[model] = {
    value: pk,
    hidden: true
  };

  let title = attachmentType === 'file' ? t`Add File` : t`Add Link`;
  let message = attachmentType === 'file' ? t`File added` : t`Link added`;

  openCreateApiForm({
    name: 'attachment-add',
    title: title,
    url: endpoint,
    successMessage: message,
    fields: formFields,
    onFormSuccess: callback
  });
}

/**
 * Edit an existing attachment (either a file or a link)
 */
export function editAttachment({
  endpoint,
  model,
  pk,
  attachmentType,
  callback
}: {
  endpoint: ApiPaths;
  model: string;
  pk: number;
  attachmentType: 'file' | 'link';
  callback?: () => void;
}) {
  let formFields: ApiFormFieldSet = {
    link: {},
    comment: {}
  };

  if (attachmentType === 'file') {
    delete formFields['link'];
  }

  formFields[model] = {
    value: pk,
    hidden: true
  };

  let title = attachmentType === 'file' ? t`Edit File` : t`Edit Link`;
  let message = attachmentType === 'file' ? t`File updated` : t`Link updated`;

  openEditApiForm({
    name: 'attachment-edit',
    title: title,
    url: endpoint,
    pk: pk,
    successMessage: message,
    fields: formFields,
    onFormSuccess: callback
  });
}

export function deleteAttachment({
  endpoint,
  pk,
  callback
}: {
  endpoint: ApiPaths;
  pk: number;
  callback: () => void;
}) {
  openDeleteApiForm({
    url: endpoint,
    pk: pk,
    name: 'attachment-edit',
    title: t`Delete Attachment`,
    successMessage: t`Attachment deleted`,
    onFormSuccess: callback,
    fields: {},
    preFormContent: (
      <Text>{t`Are you sure you want to delete this attachment?`}</Text>
    )
  });
}
