import user

'''
Move comments to user.py
'''

class user_ui(user):
    def __init__(self):
        pass

    def list_directory(self):
        '''
        header: LIST <no-argument> /for now
        required params
            working-directory
            selected-disk

        Send request to server asking for contents in working-directory
        '''
        return NotImplemented

    def navigate(self):
        '''
        header: CD directory
        can open only one folder /for now
        Send information that client is changing working-directory

        Server:
            confirms that folder still exists
            confirms that directory is folder even that it can check itself

        list_directory should be called after this, so user doesnt have to execute another command calling LIST
        '''
        return NotImplemented

    def parse_file(self):
        return NotImplemented