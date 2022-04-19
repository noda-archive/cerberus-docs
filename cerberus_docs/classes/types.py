from typing import Dict, List, Any, OrderedDict, Union

Schema = Dict[str, Any]
SchemaMap = Dict[str, List[Schema]]
SortedAttribute = OrderedDict[str, Any]
FormattedAttribute = Dict[str, str]
Attribute = Union[Dict[str, Any], SortedAttribute, FormattedAttribute]
