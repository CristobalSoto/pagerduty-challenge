class IncidentBatchProcessor:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute_all(self):
        for command in self.commands:
            command.execute()
