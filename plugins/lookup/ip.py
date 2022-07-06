import ansible.utils as utils
import ansible.errors as errors
from ansible.plugins.lookup import LookupBase
import socket

class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, variables=None, **kwargs):

        hostname = terms[0]

        if not isinstance(hostname, str):
            raise errors.AnsibleError("ip lookup expects a string (hostname)")

        return [socket.gethostbyname(hostname)]