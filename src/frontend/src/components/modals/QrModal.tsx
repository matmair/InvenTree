import {} from '@mantine/core';
import type { ContextModalProps } from '@mantine/modals';
import type { NavigateFunction } from '@tanstack/react-router';
import { ScanInputHandler } from '../barcodes/BarcodeScanDialog';

export function QrModal({
  context,
  id,
  innerProps
}: Readonly<
  ContextModalProps<{ modalBody: string; navigate: NavigateFunction }>
>) {
  function close() {
    context.closeModal(id);
  }
  function navigate() {
    context.closeModal(id);
  }

  return <ScanInputHandler navigate={innerProps.navigate} onClose={close} />;
}
