from .base_processing_node import BaseProcessingNode, ProcessingArtifact


class ReportProcessingNode(BaseProcessingNode):
    def __init__(self, available_artifacts, outputs):
        super(ReportProcessingNode, self).__init__(available_artifacts, outputs)
        self.outputs = outputs
        self.fmt = 'json'

    def get_artifacts(self):
        datahub_type = 'derived/report'
        resource_name = 'datapackage_report'
        out_path = '{}.{}'.format(resource_name, self.fmt)
        tabular_artifacts = [
            artifact for artifact in self.available_artifacts
                if artifact.datahub_type == 'source/tabular'
        ]
        output = ProcessingArtifact(
            datahub_type, resource_name,
            tabular_artifacts, [],
            [('assembler.validate_resource', {}),
             ('dump.to_path', {
                'out-path': out_path,
                'force-format': False,
                'handle-non-tabular': True
            }),
             ('add_resource', {
                'url': out_path,
                'name': resource_name,
                'format': 'json',
                'path': 'data/{}.json'.format(resource_name),
                'datahub': {
                  'type': "derived/report",
                },
                'description': 'Validation report for tabular data'
             })],
            False)
        yield output
