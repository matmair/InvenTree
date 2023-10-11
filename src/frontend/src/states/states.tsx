export interface Host {
  host: string;
  name: string;
}

export interface HostList {
  [key: string]: Host;
}

// Type interface fully defining the current user
export interface UserProps {
  name: string;
  email: string;
  username: string;
  is_staff?: boolean;
  is_superuser?: boolean;
  roles?: Record<string, string[]>;
}

// Type interface fully defining the current server
export interface ServerAPIProps {
  server: null | string;
  version: null | string;
  instance: null | string;
  apiVersion: null | number;
  worker_running: null | boolean;
  worker_pending_tasks: null | number;
  plugins_enabled: null | boolean;
  active_plugins: PluginProps[];
}

// Type interface defining a single 'setting' object
export interface Setting {
  pk: number;
  key: string;
  value: string;
  name: string;
  description: string;
  type: SettingType;
  units: string;
  choices: SettingChoice[];
  model_name: string | null;
  api_url: string | null;
  typ: SettingTyp;
  plugin?: string;
  method?: string;
}

export interface SettingChoice {
  value: string;
  display_name: string;
}

export enum SettingTyp {
  Inventree = 'inventree',
  Plugin = 'plugin',
  User = 'user',
  Notification = 'notification'
}

export enum SettingType {
  Boolean = 'boolean',
  Integer = 'integer',
  String = 'string'
}

export interface PluginProps {
  name: string;
  slug: string;
  version: null | string;
}

// Errors
export type ErrorResponse = {
  data: any;
  status: number;
  statusText: string;
  message?: string;
};
