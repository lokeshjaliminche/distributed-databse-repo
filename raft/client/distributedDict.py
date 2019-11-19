import collections
from raft.client.abstractClient import AbstractClient
from raft.client.refresh_policies import RefreshPolicyAlways


class DistributedDict(collections.UserDict, AbstractClient):
    """Client for raft instances with dictionary based state machines."""
    def __init__(self, addr, port, append_retry_attempts=3,
                 refresh_policy=RefreshPolicyAlways()):
        super().__init__()
        self.data['cluster'] = [(addr, port)]
        self.append_retry_attempts = append_retry_attempts
        self.refresh_policy = refresh_policy
        self.refresh(force=True)

    def __getitem__(self, key):
        self.refresh()
        return self.data[key]

    def __setitem__(self, key, value):
        self._append_log({'action': 'change', 'key': key, 'value': value})

    def __delitem__(self, key):
        self.refresh(force=True)
        #this indicates that the data is getting deleted from both local and remote.
        #checkout append_log_function

        del self.data[self.__keytransform__(key)]
        self._append_log({'action': 'delete', 'key': key})

    def __keytransform__(self, key):
        return key

    def __repr__(self):
        self.refresh()
        return super().__repr__()

    def refresh(self, force=False):

        print('distributed_dict', 'refresh', self.data)
        if force or self.refresh_policy.can_update():
            self.data = self._get_state()

    def _append_log(self, payload):
        print(payload)
        for attempt in range(self.append_retry_attempts):
            #this appendlog function call append_log function of the super class which is responsible for
            #taking appropriate action.
            #parent class of this function is AbstractClient checkout that class for details.
            response = super()._append_log(payload)
            if response['success']:
                break
        # TODO: logging
        print(response)
        return response

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        d = DistributedDict('127.0.0.1', 9111)
        d[sys.argv[1]] = sys.argv[2]
