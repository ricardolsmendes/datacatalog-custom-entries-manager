import math
import unittest
from unittest import mock

import pandas as pd

from datacatalog_custom_entries_manager import custom_entries_csv_reader


@mock.patch('datacatalog_custom_entries_manager.custom_entries_csv_reader.pd.read_csv')
class CustomEntriesCSVReaderTest(unittest.TestCase):
    # Pandas is not aware of the field types and reads empty values as NaN;
    # thus, math.nan is used in the mocked dataframes to set up more realistic testing scenarios.

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
                'user_specified_system': ['TestSystem', math.nan],
                'group_id': ['test-group', math.nan],
                'linked_resource': ['//test/linked-resource-1', '//test/linked-resource-2'],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        self.assertEqual(1, len(assembled_entry_groups))

        _, groups = assembled_entry_groups[0]

        self.assertEqual(2, len(groups[0]['entries']))

    def test_read_file_missing_key_column_should_fail_for_two_or_more_records(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'group_id': ['test-group', math.nan],
                'linked_resource': ['//test/linked-resource-1', '//test/linked-resource-2'],
            })

        self.assertRaises(KeyError, custom_entries_csv_reader.CustomEntriesCSVReader.read_file,
                          'file-path')

    def test_read_file_missing_mandatory_column_should_set_nan_entry_field(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(data={
            'user_specified_system': ['TestSystem'],
            'group_id': ['test-group'],
        })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertTrue(math.isnan(entry['linked_resource']))

    def test_read_file_missing_optional_column_should_skip_entry_field(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'user_specified_system': ['TestSystem'],
                'group_id': ['test-group'],
                'linked_resource': ['//test/linked-resource'],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertFalse('description' in entry)

    def test_read_file_nan_optional_value_should_skip_entry_field(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'user_specified_system': ['TestSystem'],
                'group_id': ['test-group'],
                'linked_resource': ['//test/linked-resource'],
                'description': [math.nan],
            })

        assembled_entry_groups = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertFalse('description' in entry)

    def test_read_file_provided_optional_value_should_set_entry_field(self, mock_read_csv):
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
