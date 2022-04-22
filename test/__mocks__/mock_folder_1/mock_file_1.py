from cerberus_docs import CerberusSchema


class MockFileParent:
    schema = CerberusSchema({'name': {'type': 'string'}})


class MockFileChild(MockFileParent):
    schema = CerberusSchema({'name': {'type': 'string'}})
