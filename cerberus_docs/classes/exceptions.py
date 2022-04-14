class CerberusDocsException(Exception):
    def __init__(self, message='An error occurred'):
        self.message = message
