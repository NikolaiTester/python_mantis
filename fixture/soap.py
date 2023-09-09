from suds.client import Client
from suds import WebFault
from model.project import Project

class SoapHelper:
    def __init__(self, app):
        self.app = app

    def get_project_list(self):
        client = Client(self.app.config['web']['baseUrl'] + "api/soap/mantisconnect.php?wsdl")
        project_list = []
        try:
            projects = client.service.mc_projects_get_user_accessible(
                self.app.config['webadmin']['username'], self.app.config['webadmin']['password'])
            for project in projects:
                project_list.append(Project(project_name=project.name, project_id=project.id))
            return project_list
        except WebFault:
            return False

    def can_login(self, username, password):
        client = Client(self.app.config['web']['baseUrl'] + "api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False