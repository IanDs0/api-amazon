from rest_framework.test import APITestCase
from rest_framework import status
from api_lojas.models import Loja

class MeuTesteDeAPI(APITestCase):
    def setUp(self):
        self.loja = Loja.objects.create(loja_color='f0f0f0', loja_name='teste')
        self.url = '/'

    def test_list_stories(self):

        stories = Loja.objects.all()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(stories))

        i=0

        for story in stories:
            self.assertEqual(response.data[i]['loja_color'], story.loja_color)
            self.assertEqual(response.data[i]['loja_name'], story.loja_name)
            i+=1
