from model.project import Project
import time


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.project_name)
        if project.status is not None:
            wd.find_element_by_name("status").click()
            wd.find_element_by_link_text(project.status).click()
        if project.view_status is not None:
            wd.find_element_by_name("view_state").click()
            wd.find_element_by_link_text(project.view_status).click()
        self.change_field_value("description", project.description)

    def create_project(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector("input[value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_css_selector("input[value='Add Project']").click()
        time.sleep(3)
        self.project_cache = None

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_project_page()
            self.project_cache = []
#            element = wd.find_elements_by_css_selector("tr.row-1")
#            text = element[0].find_element_by_css_selector("td:nth-child(4)").text
#            print(text)
            for s in ["1", "2"]:
                for element in wd.find_element_by_css_selector("table[cellspacing='1']").\
                        find_elements_by_css_selector("tr.row-%s" % s):
                    text = element.find_element_by_css_selector("a").text
                    project_id = element.find_element_by_css_selector("a").get_attribute("href")\
                        .rsplit('project_id=')[1]
                    self.project_cache.append(Project(project_name=text, project_id=int(project_id)))
        return list(self.project_cache)

    def delete_project(self, project_name):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_link_text(project_name.rstrip()).click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.project_cache = None