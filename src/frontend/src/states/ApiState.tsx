import { create } from 'zustand';

import { api } from '../App';
import { emptyServerAPI } from '../defaults/defaults';
import { ServerAPIProps, UserProps } from './states';

interface ServerApiStateProps {
  server: ServerAPIProps;
  setServer: (newServer: ServerAPIProps) => void;
  fetchServerApiState: () => void;
}

export const useServerApiState = create<ServerApiStateProps>((set, get) => ({
  server: emptyServerAPI,
  setServer: (newServer: ServerAPIProps) => set({ server: newServer }),
  fetchServerApiState: async () => {
    // Fetch server data
    await api.get('/').then((response) => {
      set({ server: response.data });
    });
  }
}));

export enum ApiPaths {
  // User information
  user_me = 'api-user-me',
  user_roles = 'api-user-roles',
  user_token = 'api-user-token',
  user_simple_login = 'api-user-simple-login',
  user_reset = 'api-user-reset',
  user_reset_set = 'api-user-reset-set',

  settings_global_list = 'api-settings-global-list',
  settings_user_list = 'api-settings-user-list',
  notifications_list = 'api-notifications-list',

  barcode = 'api-barcode',

  // Build order URLs
  build_order_list = 'api-build-list',
  build_order_attachment_list = 'api-build-attachment-list',

  // Part URLs
  part_list = 'api-part-list',
  category_list = 'api-category-list',
  related_part_list = 'api-related-part-list',
  part_attachment_list = 'api-part-attachment-list',

  // Company URLs
  company_list = 'api-company-list',
  supplier_part_list = 'api-supplier-part-list',

  // Stock Item URLs
  stock_item_list = 'api-stock-item-list',
  stock_location_list = 'api-stock-location-list',
  stock_attachment_list = 'api-stock-attachment-list',

  // Purchase Order URLs
  purchase_order_list = 'api-purchase-order-list',

  // Sales Order URLs
  sales_order_list = 'api-sales-order-list'
}

/**
 * Return the endpoint associated with a given API path
 */
export function endpoint(path: ApiPaths): string {
  switch (path) {
    case ApiPaths.user_me:
      return 'user/me/';
    case ApiPaths.user_roles:
      return 'user/roles/';
    case ApiPaths.user_token:
      return 'user/token/';
    case ApiPaths.user_simple_login:
      return 'email/generate/';
    case ApiPaths.user_reset:
      return '/auth/password/reset/';
    case ApiPaths.user_reset_set:
      return '/auth/password/reset/confirm/';
    case ApiPaths.settings_global_list:
      return 'settings/global/';
    case ApiPaths.settings_user_list:
      return 'settings/user/';
    case ApiPaths.notifications_list:
      return 'notifications/';
    case ApiPaths.barcode:
      return 'barcode/';
    case ApiPaths.build_order_list:
      return 'build/';
    case ApiPaths.build_order_attachment_list:
      return 'build/attachment/';
    case ApiPaths.part_list:
      return 'part/';
    case ApiPaths.category_list:
      return 'part/category/';
    case ApiPaths.related_part_list:
      return 'part/related/';
    case ApiPaths.part_attachment_list:
      return 'part/attachment/';
    case ApiPaths.company_list:
      return 'company/';
    case ApiPaths.supplier_part_list:
      return 'company/part/';
    case ApiPaths.stock_item_list:
      return 'stock/';
    case ApiPaths.stock_location_list:
      return 'stock/location/';
    case ApiPaths.stock_attachment_list:
      return 'stock/attachment/';
    case ApiPaths.purchase_order_list:
      return 'order/po/';
    case ApiPaths.sales_order_list:
      return 'order/so/';

    default:
      return '';
  }
}

/**
 * Construct an API URL with an endpoint and (optional) pk value
 */
export function url(path: ApiPaths, pk?: any): string {
  let _url = endpoint(path);

  if (_url && pk) {
    _url += `${pk}/`;
  }

  return _url;
}
