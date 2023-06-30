# Open API Slicer

Open API slicer is simple library that can help you to split one big open api specification into small parts using tags of paths.

It uses tags of path's action. It's compatible with references to components/schemas.

## Example

Fo example you can open swagger specification and split it by controllers
```python
import json
from openapi_slicer import OpenApiSlicer


with open('swagger.json', encoding='utf-8-sig') as swagger_file:
    swagger = json.load(swagger_file)

slicer = OpenApiSlicer(swagger)
foo_controller_specification = slicer.slice(['FooController'])
bar_controller_specification = slicer.slice(['BarController'])

print(foo_controller_specification)
print(bar_controller_specification)
```