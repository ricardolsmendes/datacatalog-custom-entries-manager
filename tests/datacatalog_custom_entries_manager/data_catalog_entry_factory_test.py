import unittest

from datacatalog_custom_entries_manager import data_catalog_entry_factory


class DataCatalogEntryFactoryTest(unittest.TestCase):

    def setUp(self):
        self.__data_catalog_entry_factory = data_catalog_entry_factory.DataCatalogEntryFactory(
            'test-project', 'test-location')

    def test_make_entry_from_dict_should_set_mandatory_fields(self):
        data = {
            'linked_resource': '//test/linked-resource',
            'display_name': 'Test display name',
            'user_specified_type': 'Test specified type',
            'user_specified_system': 'Test specified system',
        }

        entry_id, entry = self.__data_catalog_entry_factory.make_entry_from_dict(
            'test-group', data)

        self.assertEqual('test_display_name', entry_id)
        self.assertEqual(
            'projects/test-project/locations/test-location/'
            'entryGroups/test-group/entries/test_display_name', entry.name)
        self.assertEqual('//test/linked-resource', entry.linked_resource)
        self.assertEqual('Test display name', entry.display_name)

    def test_make_entry_from_dict_missing_display_name_should_fail(self):
        data = {
            'linked_resource': '//test/linked-resource',
            'user_specified_type': 'Test specified type',
            'user_specified_system': 'Test specified system',
        }

        self.assertRaises(AttributeError, self.__data_catalog_entry_factory.make_entry_from_dict,
                          'test-group', data)

    def test_make_entry_from_dict_missing_other_mandatory_fields_should_fail(self):
        data = {
            'display_name': 'Test display name',
            'user_specified_type': 'Test specified type',
            'user_specified_system': 'Test specified system',
        }

        self.assertRaises(TypeError, self.__data_catalog_entry_factory.make_entry_from_dict,
                          'test-group', data)

    def test_make_entry_from_dict_should_set_optional_description(self):
        data = {
            'linked_resource': '//test/linked-resource',
            'display_name': 'Test display name',
            'description': 'Test description',
            'user_specified_type': 'Test specified type',
            'user_specified_system': 'Test specified system',
        }

        _, entry = self.__data_catalog_entry_factory.make_entry_from_dict('test-group', data)

        self.assertEqual('Test description', entry.description)

    def test_make_entry_from_dict_should_set_optional_timestamps(self):
        data = {
            'linked_resource': '//test/linked-resource',
            'display_name': 'Test display name',
            'user_specified_type': 'Test specified type',
            'user_specified_system': 'Test specified system',
            'created_at': '2020-10-10T17:25:00-0300',
            'updated_at': '2020-10-10T17:26:30-0300',
        }

        _, entry = self.__data_catalog_entry_factory.make_entry_from_dict('test-group', data)

        self.assertEqual(1602361500, entry.source_system_timestamps.create_time.seconds)
        self.assertEqual(1602361590, entry.source_system_timestamps.update_time.seconds)

    def test_make_entry_from_dict_invalid_timestamp_format_should_fail(self):
        data = {
            'linked_resource': '//test/linked-resource',
            'display_name': 'Test display name',
            'user_specified_type': 'Test specified type',
            'user_specified_system': 'Test specified system',
            'created_at': '2020-10-10T17:25:00Z',
        }

        self.assertRaises(ValueError, self.__data_catalog_entry_factory.make_entry_from_dict,
                          'test-group', data)
