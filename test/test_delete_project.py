from model.project import Project


def test_delete_project(app):
    old_projects = app.soap.get_project_list()
    project = Project(project_name="testProject")
    if project not in old_projects:
        app.project.create_project(project)
        old_projects = app.soap.get_project_list()
    app.project.delete_project(project.project_name)
    old_projects.remove(project)
    new_projects = app.soap.get_project_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)