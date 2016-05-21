from commands import *

class ScriptRunner:
    def __init__(self, flavored, data):
        self.script = flavored['script']
        self._commands = flavored['commands']
        self._data = data

    def run(self):
        for command in self.script:
            if hasattr(self, command):
                getattr(self, command)(self._data)
            else:
                raise RuntimeError("unsupported script command '{0}' detected".format(command))

    def _getArgs(self, data_entity, params):
        args = set()
        for param in params:            
            args.add(data_entity[param])                 
        return args

    def _execute_command(self, data_entity, command):
        args = self._getArgs(data_entity, command['params'])
        result = Command(command['command_line'], args).execute()
        if result.return_code is not result.SUCCESS_CODE:
            raise RuntimeError("the command '{0}' returned error code '{1}'. The command output is '{2}'".format(result.command, result.return_code, result.output))

    def create_groups(self, data):
        create_group = self._commands['create_group']
        for group in data['groups']:
            self._execute_command(group, create_group)   

    def create_users(self, data):
        create_user = self._commands['create_user']
        add_user_to_group = self._commands['add_user_to_group']
        set_user_password = self._commands['set_user_password']
        lock_user = self._commands['lock_user']
        for user in data['users']:
            self._execute_command(user, create_user)
            self._execute_command(user, set_user_password)
            if user['is_locked']:
                self._execute_command(user, lock_user)
            for group in user['groups']:
                self._execute_command({'name': user['name'], 'group': group}, add_user_to_group)

    def create_dirs(self, data):
        create_directory = self._commands['create_directory']
        set_permissions = self._commands['set_permissions']
        set_owner = self._commands['set_owner']        
        for dir in data['dirs']:
            self._execute_command(dir, create_directory)
            self._execute_command(dir, set_permissions)
            self._execute_command(dir, set_owner)

    def create_files(self, data):
        create_text_file = self._commands['create_text_file']
        set_permissions = self._commands['set_permissions']
        set_owner = self._commands['set_owner']        
        for file in data['files']:
            self._execute_command(file, create_text_file)
            self._execute_command(file, set_permissions)
            self._execute_command(file, set_owner)
