import unittest
from main import get_one_to_many, get_many_to_many, get_dbs_starting_with_a, get_db_max_sizes, get_sorted_many_to_many, Database, DataTable, TableDatabase

class TestYourModule(unittest.TestCase):

    def test_get_one_to_many(self):
        databases = [Database(1, 'TestDB')]
        data_tables = [DataTable(1, 'TestTable', 10, 1)]
        expected_result = [('TestTable', 10, 'TestDB')]
        self.assertEqual(get_one_to_many(databases, data_tables), expected_result)


    def test_get_dbs_starting_with_a(self):
        one_to_many_result = [('Users', 50, 'AnalyticsDB'), ('Archive', 500, 'ArchiveDB')]
        expected_result = {'AnalyticsDB': ['Users'], 'ArchiveDB': ['Archive']}
        self.assertEqual(get_dbs_starting_with_a(one_to_many_result), expected_result)


    def test_get_db_max_sizes(self):
        one_to_many_result = [('Users', 50, 'AnalyticsDB'), ('Products', 100, 'ProductsDB'), ('Orders', 20, 'OrdersDB'),('Orders2', 200, 'OrdersDB')]
        expected_result = [('OrdersDB', 200), ('ProductsDB', 100), ('AnalyticsDB', 50)]
        self.assertEqual(get_db_max_sizes(one_to_many_result), expected_result)



if __name__ == '__main__':
    unittest.main()
