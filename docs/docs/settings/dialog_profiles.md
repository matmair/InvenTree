# Dialog Profiles

Dialog Profiles allow administrators to customize the visibility of fields in various user interface dialogs. This feature is particularly useful for smaller InvenTree installations that may not require all the available fields, allowing for a cleaner and more focused user experience.

## Enabling Dialog Profiles

Dialog Profiles are an optional feature and must be enabled in the [Global Settings](global.md).

1. Navigate to the **Admin Center**.
2. Select **Dialog Profiles** from the **Data Management** group.
3. Toggle the **Enable Dialog Profiles** setting to **On**.

## Managing Profiles

Once enabled, you can create and manage dialog profiles from the same **Dialog Profiles** panel in the **Admin Center**.

### Creating a Profile

To create a new dialog profile:

1. Click on the **Add dialog profile** button.
2. Provide a **Name** and optional **Description** for the profile.
3. Define the visibility rules in the **Definition** field using JSON format.
4. Ensure the **Enabled** checkbox is checked.
5. Click **Submit**.

### Profile Definition

The profile definition uses a JSON format to specify which fields should be hidden for specific models.

```json
{
  "model_name": ["field_name_1", "field_name_2"]
}
```

- `model_name`: The internal name of the model (e.g., `part`, `stockitem`, `company`).
- `field_name`: The name of the field to hide (e.g., `link`, `notes`, `IPN`).

Multiple models and fields can be specified in a single profile.

#### Example

To hide the `link` field for parts and the `batch` field for stock items:

```json
{
  "part": ["link"],
  "stockitem": ["batch"]
}
```

## How it Works

When Dialog Profiles are enabled, InvenTree automatically applies the visibility rules from all **enabled** profiles to the API metadata. This metadata is used by the frontend to determine which fields to render in dialogs.

If a field is marked as hidden in **any** enabled profile, it will be hidden in the user interface.
