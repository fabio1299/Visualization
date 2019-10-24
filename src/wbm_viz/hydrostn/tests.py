from django.test import TestCase
from .models import Hydrostn30Subbasin

# Create your tests here.
class SubbasinTestCase(TestCase):
    databases = ['argentina_01min']

    def test_query_all(self):

        #Test can query Subbasin model (maps to database view)
        self.assertEqual(Hydrostn30Subbasin.objects.count(), 48077)