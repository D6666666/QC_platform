from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

# Create your tests here.

#测试视图
class ViewsTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        User.objects.create_user('test01','test01@mail.com','test123456') #测试数据，实际不会入库
        self.client = Client()

    def test_index(self):
        # Issue a GET request.
        response = self.client.get('/')
        print(response.content.decode('utf-8'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'index.html')

        # # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)

    def test_login(self):
        # Issue a POSR request.
        login_data = {'username':'test01','password':'test123456'}
        response = self.client.post('/login_action/',data=login_data)
        # print(response.content.decode('utf-8'))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)