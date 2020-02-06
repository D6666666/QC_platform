from django.test import TestCase
from project_app.models import Project

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

# Create your tests here.

#模型测试
class ProjectTestCase(TestCase):
    def setUp(self):
        Project.objects.create(name ='单元测试项目',describe = '这里是模型的测试数据')

    def test_project_create(self):
        project = Project.objects.get(name='单元测试项目')
        print(project.describe)
        print(project.create_time)
        self.assertEqual(project.describe,'这里是模型的测试数据')
#ui测试
class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
