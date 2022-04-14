from typing import Dict, List, Any, OrderedDict, Union

Schema = Dict[str, Any]
SchemaMap = Dict[str, List[Schema]]
Attribute = Union[Dict[str, Any], OrderedDict[str, Any]]
