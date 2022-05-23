mock_schema = {
    'test1': {
        'required': True,
        'type': 'string',
        'meta': {'description': 'This is a description for test1'},
        'allowed': ['v0', 'v1'],
    },
    'test2': {
        'required': True,
        'type': 'string',
    },
    'test3': {
        'type': 'dict',
        'allow_unknown': True,
        'required': False,
        'valuesrules': {
            'type': 'string',
        },
    },
    'test4': {
        'type': 'dict',
        'allow_unknown': True,
        'required': False,
        'schema': {
            'test5': {
                'type': 'list',
                'required': False,
                'meta': {'description': 'This is a description for test5'},
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'test6': {
                            'type': 'string',
                            'required': True,
                        },
                        'test7': {
                            'type': 'string',
                            'required': True,
                        },
                    }
                },
            }
        },
    },
}
