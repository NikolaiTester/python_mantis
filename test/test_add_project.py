from model.project import Project


def test_add_project(app):
    old_projects = app.soap.get_project_list()
    project = Project(project_name="testproject")
    if project in old_projects:
        app.project.delete_project(project.project_name)
        old_projects = app.soap.get_project_list()
    app.project.create_project(project)
    old_projects.append(project)
    new_projects = app.soap.get_project_list()
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)