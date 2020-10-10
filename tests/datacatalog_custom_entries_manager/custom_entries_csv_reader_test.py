import unittest
from unittest import mock

import pandas as pd

from datacatalog_custom_entries_manager import custom_entries_csv_reader


@mock.patch('datacatalog_custom_entries_manager.custom_entries_csv_reader.pd.read_csv')
class CustomEntriesCSVReaderTest(unittest.TestCase):
    __EMPTY_VALUE = float('NaN')

    def test_read_file_multiple_user_specified_systems_should_succeed(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'user_specified_system': ['TestSystem1', 'TestSystem2'],
                'group_id': ['test-group-1', 'test-group-2'],
                'linked_resource': ['//test/linked-resource-1', '//test/linked-resource-2'],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        self.assertEqual(2, len(assembled_entry_groups))

        _, groups_system_1 = assembled_entry_groups[0]
        _, groups_system_2 = assembled_entry_groups[1]

        group_1 = groups_system_1[0]
        group_2 = groups_system_2[0]

        self.assertEqual('test-group-1', group_1['id'])
        self.assertEqual('test-group-2', group_2['id'])

        entry_1 = group_1['entries'][0]
        entry_2 = group_2['entries'][0]

        self.assertEqual('TestSystem1', entry_1['user_specified_system'])
        self.assertEqual('TestSystem2', entry_2['user_specified_system'])

    def test_read_file_missing_auto_fill_values_should_succeed(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'user_specified_system': ['TestSystem', self.__EMPTY_VALUE],
                'group_id': ['test-group', self.__EMPTY_VALUE],
                'linked_resource': ['//test/linked-resource-1', '//test/linked-resource-2'],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        self.assertEqual(1, len(assembled_entry_groups))

        _, groups = assembled_entry_groups[0]

        self.assertEqual(2, len(groups[0]['entries']))

    def test_read_file_should_not_set_optional_string_field_when_not_filled(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'user_specified_system': ['TestSystem'],
                'group_id': ['test-group'],
                'linked_resource': ['//test/linked-resource'],
                'description': [self.__EMPTY_VALUE],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertFalse('description' in entry)

    def test_read_file_should_set_optional_string_field_when_filled(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'user_specified_system': ['TestSystem'],
                'group_id': ['test-group'],
                'linked_resource': ['//test/linked-resource'],
                'description': ['Test description'],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertEqual('Test description', entry['description'])
