from .base_processing_node import BaseProcessingNode, ProcessingArtifact


class OutputToZipProcessingNode(BaseProcessingNode):
    def __init__(self, available_artifacts, outputs):
        super(OutputToZipProcessingNode, self).__init__(available_artifacts, outputs)
        self.outputs = outputs
        self.fmt = 'zip'

    def get_artifacts(self):
        zip_params = [out for out in self.outputs if out['kind'] == 'zip']
        if len(zip_params):
            out_file = zip_params[0]['parameters']['out-file']
            datahub_type = 'derived/{}'.format(self.fmt)
            resource_name = 'datapackage_zip'
            output = ProcessingArtifact(
                datahub_type, resource_name,
                [], self.available_artifacts,
                [('dump.to_zip', {
                    'out-file': out_file,
                    'force-format': False,
                    'handle-non-tabular': True}),
                 ('assembler.clear_resources', {}),
                 ('add_resource', {
                    'url': out_file,
                    'name': resource_name,
                    'format': self.fmt,
                    'path': 'data/{}.zip'.format(resource_name),
                    'datahub': {
                      'type': "derived/zip",
                    },
                    'description': 'Compressed versions of dataset. Includes normalized CSV and JSON data with original data and datapackage.json.' #noqa
                 })],
                False
            )
            yield output
