import { t } from '@lingui/macro';

import type {
  StatusCodeInterface,
  StatusCodeListInterface
} from '../components/render/StatusRenderer';
import { ApiEndpoints } from '../enums/ApiEndpoints';
import { ModelType } from '../enums/ModelType';
import { apiUrl } from '../states/ApiState';
import { useGlobalSettingsState } from '../states/SettingsState';
import { type StatusLookup, useGlobalStatusState } from '../states/StatusState';

/**
 * Interface for the table filter choice
 */
export type TableFilterChoice = {
  value: string;
  label: string;
};

/**
 * Available filter types
 *
 * boolean: A simple true/false filter
 * choice: A filter which allows selection from a list of (supplied)
 * date: A filter which allows selection from a date input
 * text: A filter which allows raw text input
 * api: A filter which fetches its options from an API endpoint
 */
export type TableFilterType = 'boolean' | 'choice' | 'date' | 'text' | 'api';

/**
 * Interface for the table filter type. Provides a number of options for selecting filter value:
 *
 * name: The name of the filter (used for query string)
 * label: The label to display in the UI (human readable)
 * description: A description of the filter (human readable)
 * type: The type of filter (see TableFilterType)
 * choices: A list of TableFilterChoice objects
 * choiceFunction: A function which returns a list of TableFilterChoice objects
 * defaultValue: The default value for the filter
 * value: The current value of the filter
 * displayValue: The current display value of the filter
 * active: Whether the filter is active (false = hidden, not used)
 * apiUrl: The API URL to use for fetching dynamic filter options
 * model: The model type to use for fetching dynamic filter options
 * modelRenderer: A function to render a simple text version of the model type
 */
export type TableFilter = {
  name: string;
  label: string;
  description?: string;
  type?: TableFilterType;
  choices?: TableFilterChoice[];
  choiceFunction?: () => TableFilterChoice[];
  defaultValue?: any;
  value?: any;
  displayValue?: any;
  active?: boolean;
  apiUrl?: string;
  model?: ModelType;
  modelRenderer?: (instance: any) => string;
};

/**
 * Return list of available filter options for a given filter
 * @param filter - TableFilter object
 * @returns - A list of TableFilterChoice objects
 */
export function getTableFilterOptions(
  filter: TableFilter
): TableFilterChoice[] {
  if (filter.choices) {
    return filter.choices;
  }

  if (filter.choiceFunction) {
    return filter.choiceFunction();
  }

  // Default fallback is a boolean filter
  return [
    { value: 'true', label: t`Yes` },
    { value: 'false', label: t`No` }
  ];
}

/*
 * Construct a table filter which allows filtering by status code
 */
export function StatusFilterOptions(
  model: ModelType
): () => TableFilterChoice[] {
  return () => {
    const statusCodeList: StatusLookup | undefined =
      useGlobalStatusState.getState().status;

    if (!statusCodeList) {
      return [];
    }

    const codes: StatusCodeListInterface | undefined = statusCodeList[model];

    if (codes) {
      return Object.keys(codes.values).map((key) => {
        const entry: StatusCodeInterface = codes.values[key];
        return {
          value: entry.key.toString(),
          label: entry.label?.toString() ?? entry.key.toString()
        };
      });
    }

    return [];
  };
}

// Define some commonly used filters

export function AssignedToMeFilter(): TableFilter {
  return {
    name: 'assigned_to_me',
    type: 'boolean',
    label: t`Assigned to me`,
    description: t`Show orders assigned to me`
  };
}

export function OutstandingFilter(): TableFilter {
  return {
    name: 'outstanding',
    label: t`Outstanding`,
    description: t`Show outstanding items`
  };
}

export function OverdueFilter(): TableFilter {
  return {
    name: 'overdue',
    label: t`Overdue`,
    description: t`Show overdue items`
  };
}

export function MinDateFilter(): TableFilter {
  return {
    name: 'min_date',
    label: t`Minimum Date`,
    description: t`Show items after this date`,
    type: 'date'
  };
}

export function MaxDateFilter(): TableFilter {
  return {
    name: 'max_date',
    label: t`Maximum Date`,
    description: t`Show items before this date`,
    type: 'date'
  };
}

export function CreatedBeforeFilter(): TableFilter {
  return {
    name: 'created_before',
    label: t`Created Before`,
    description: t`Show items created before this date`,
    type: 'date'
  };
}

export function CreatedAfterFilter(): TableFilter {
  return {
    name: 'created_after',
    label: t`Created After`,
    description: t`Show items created after this date`,
    type: 'date'
  };
}

export function StartDateBeforeFilter(): TableFilter {
  return {
    name: 'start_date_before',
    label: t`Start Date Before`,
    description: t`Show items with a start date before this date`,
    type: 'date'
  };
}

export function StartDateAfterFilter(): TableFilter {
  return {
    name: 'start_date_after',
    label: t`Start Date After`,
    description: t`Show items with a start date after this date`,
    type: 'date'
  };
}

export function TargetDateBeforeFilter(): TableFilter {
  return {
    name: 'target_date_before',
    label: t`Target Date Before`,
    description: t`Show items with a target date before this date`,
    type: 'date'
  };
}

export function TargetDateAfterFilter(): TableFilter {
  return {
    name: 'target_date_after',
    label: t`Target Date After`,
    description: t`Show items with a target date after this date`,
    type: 'date'
  };
}

export function CompletedBeforeFilter(): TableFilter {
  return {
    name: 'completed_before',
    label: t`Completed Before`,
    description: t`Show items completed before this date`,
    type: 'date'
  };
}

export function CompletedAfterFilter(): TableFilter {
  return {
    name: 'completed_after',
    label: t`Completed After`,
    description: t`Show items completed after this date`,
    type: 'date'
  };
}

export function HasProjectCodeFilter(): TableFilter {
  const globalSettings = useGlobalSettingsState.getState();
  const enabled = globalSettings.isSet('PROJECT_CODES_ENABLED', true);

  return {
    name: 'has_project_code',
    type: 'boolean',
    label: t`Has Project Code`,
    description: t`Show orders with an assigned project code`,
    active: enabled
  };
}

export function OrderStatusFilter({
  model
}: { model: ModelType }): TableFilter {
  return {
    name: 'status',
    label: t`Status`,
    description: t`Filter by order status`,
    choiceFunction: StatusFilterOptions(model)
  };
}

export function ProjectCodeFilter(): TableFilter {
  const globalSettings = useGlobalSettingsState.getState();
  const enabled = globalSettings.isSet('PROJECT_CODES_ENABLED', true);

  return {
    name: 'project_code',
    label: t`Project Code`,
    description: t`Filter by project code`,
    active: enabled,
    type: 'api',
    apiUrl: apiUrl(ApiEndpoints.project_code_list),
    model: ModelType.projectcode,
    modelRenderer: (instance) => instance.code
  };
}

export function OwnerFilter({
  name,
  label,
  description
}: {
  name: string;
  label: string;
  description: string;
}): TableFilter {
  return {
    name: name,
    label: label,
    description: description,
    type: 'api',
    apiUrl: apiUrl(ApiEndpoints.owner_list),
    model: ModelType.owner,
    modelRenderer: (instance: any) => instance.name
  };
}

export function ResponsibleFilter(): TableFilter {
  return OwnerFilter({
    name: 'assigned_to',
    label: t`Responsible`,
    description: t`Filter by responsible owner`
  });
}

export function UserFilter({
  name,
  label,
  description
}: {
  name?: string;
  label?: string;
  description?: string;
}): TableFilter {
  return {
    name: name ?? 'user',
    label: label ?? t`User`,
    description: description ?? t`Filter by user`,
    type: 'api',
    apiUrl: apiUrl(ApiEndpoints.user_list),
    model: ModelType.user,
    modelRenderer: (instance: any) => instance.username
  };
}

export function CreatedByFilter(): TableFilter {
  return UserFilter({
    name: 'created_by',
    label: t`Created By`,
    description: t`Filter by user who created the order`
  });
}

export function IssuedByFilter(): TableFilter {
  return UserFilter({
    name: 'issued_by',
    label: t`Issued By`,
    description: t`Filter by user who issued the order`
  });
}

export function PartCategoryFilter(): TableFilter {
  return {
    name: 'category',
    label: t`Category`,
    description: t`Filter by part category`,
    apiUrl: apiUrl(ApiEndpoints.category_list),
    model: ModelType.partcategory,
    modelRenderer: (instance: any) => instance.name
  };
}
