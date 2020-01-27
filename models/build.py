class Build:
    def __init__(self, id, description, commands, node):
        self.id = id
        self.description = description
        self.commands = commands
        self.output = ""
        self.node = node

    def run_build(self):
        self.output = self.node.run_commands(self.commands)
        return self

