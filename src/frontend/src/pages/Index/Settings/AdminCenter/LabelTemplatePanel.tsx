import { ApiEndpoints } from '../../../../enums/ApiEndpoints';
import { ModelType } from '../../../../enums/ModelType';
import { TemplateTable } from '../../../../tables/settings/TemplateTable';

function LabelTemplateTable() {
  return (
    <TemplateTable
      templateProps={{
        modelType: ModelType.labeltemplate,
        templateEndpoint: ApiEndpoints.label_list,
        printingEndpoint: ApiEndpoints.label_print,
        additionalFormFields: {
          width: {},
          height: {}
        }
      }}
    />
  );
}

export default function LabelTemplatePanel() {
  return <LabelTemplateTable />;
}
