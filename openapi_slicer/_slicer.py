from jsonpath_ng import parse


class OpenApiSlicer:
    def __init__(self, spec: dict):
        self.spec = spec
        self.schema_ref_expression = parse('$..schema..["$ref"]')
        self.all_ref_expression = parse('$..["$ref"]')

    def slice(self, tags: list):
        schemas = {}
        paths = {}
        result, spec_paths, spec_schemas, spec_definitions = self._copy_common_parts(paths, schemas)
        if not spec_paths:
            raise ValueError("Specification doesn't have 'paths' node")
        if not spec_schemas:
            raise ValueError("Specification doesn't have 'components/schemas' node")
        schemas_to_add = self._fill_paths(paths, tags, spec_paths)
        self._fill_schemas(schemas, schemas_to_add, spec_schemas)
        return result

    def _copy_common_parts(self, paths: dict, schemas: dict):
        result = {}
        spec_paths = None
        spec_schemas = None
        for key, value in self.spec.items():
            match key:
                case 'paths':
                    spec_paths = value
                    result[key] = paths
                case 'components':
                    result[key] = {}
                    for component_key, component in value.items():
                        if component_key == 'schemas':
                            spec_schemas = component
                            result[key][component_key] = schemas
                        else:
                            result[key][component_key] = component
                case _:
                    result[key] = value

        return result, spec_paths, spec_schemas

    def _fill_paths(self, paths: dict, tags: list, spec_paths: dict):
        schemas_to_add = set()
        for path_key in spec_paths:
            path_actions = {}
            path = spec_paths[path_key]
            for action_key in path:
                action = path[action_key]
                if any(tag in tags for tag in action['tags']):
                    path_actions[action_key] = action
                    for ref in self.schema_ref_expression.find(action):
                        schemas_to_add.add(ref.value)

            if len(path_actions) > 0:
                paths[path_key] = path_actions

        return schemas_to_add

    def _fill_schemas(self, schemas, schemas_to_add, spec_schemas):
        added_schemas = set()
        while len(schemas_to_add) > 0:
            schema_ref = schemas_to_add.pop()
            if not ref.startswith('#/components/schemas/'):
                # open api slicer can work only with components schema references
                continue

            schema_key = schema_ref.replace('#/components/schemas/', '')
            if schema_key not in spec_schemas:
                raise ValueError(f"Schema '{schema_key}' was not found in specification")
            schemas[schema_key] = spec_schemas[schema_key]
            added_schemas.add(schema_ref)
            for ref in self.all_ref_expression.find(schemas[schema_key]):
                if ref.value not in added_schemas:
                    schemas_to_add.add(ref.value)
