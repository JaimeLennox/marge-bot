from . import gitlab


GET, POST, PUT, DELETE = gitlab.GET, gitlab.POST, gitlab.PUT, gitlab.DELETE


class Pipeline(gitlab.Resource):
    def __init__(self, api, info, project_id):
        info['project_id'] = project_id
        super().__init__(api, info)

    @classmethod
    def fetch_by_id(cls, project_id, pipeline_id, api):
        info = api.call(
            GET(
                '/projects/{project_id}/pipelines/{pipeline_id}'.format(
                    project_id=project_id,
                    pipeline_id=pipeline_id,
                ),
            ),
        )
        return cls(api, info, project_id)

    @classmethod
    def fetch_all_pipelines(cls, api, project_id, params):
        pipelines_info = api.call(
            GET('/projects/{project_id}/pipelines'.format(project_id=project_id), params),
        )
        return [cls(api, pipeline, project_id) for pipeline in pipelines_info]

    @property
    def project_id(self):
        return self.info['project_id']

    @property
    def id(self):
        return self.info['id']

    @property
    def status(self):
        return self.info['status']

    @property
    def ref(self):
        return self.info['ref']

    @property
    def sha(self):
        return self.info['sha']

    def cancel(self):
        return self._api.call(POST(
            '/projects/{0.project_id}/pipelines/{0.id}/cancel'.format(self),
        ))
