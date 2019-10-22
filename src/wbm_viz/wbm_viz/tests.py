
from django.test import TestCase
from django.apps import apps
Subbasin = apps.get_model('subbasin', 'Subbasin')

class SubbasinTestCase(TestCase):
    databases = ['argentina']

    def test_query_all(self):
        all_subbasin = Subbasin.objects.all()
        self.assertEqual(len(all_subbasin),48077)
