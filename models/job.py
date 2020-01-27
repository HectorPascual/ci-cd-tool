from models.build import Build

class Job:
    _id = 0
    def __init__(self, title, description):
        self.id = Job._id
        self.title = title
        self.description = description
        self.builds = []

        # Increment ID
        Job._id += 1

    def create_build(self, **kwargs):
        build = Build(id=len(self.builds), description=kwargs['description'],
                      commands=kwargs['commands'], node=kwargs['node'])
        self.builds.append(build)
        return build
