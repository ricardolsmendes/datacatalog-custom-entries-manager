import io
import unittest
from unittest import mock

from datacatalog_custom_entries_manager import custom_entries_json_reader


@mock.patch('datacatalog_custom_entries_manager.custom_entries_json_reader.open',
            new_callable=mock.mock_open())
class CustomEntriesJSONReaderTest(unittest.TestCase):

    def test_read_file_multiple_user_specified_systems_should_succeed(self, mock_open):
        mock_open.return_value = io.StringIO('''
            {
              \"userSpecifiedSystems\": [{
                \"name\": \"TestSystem1\",
                \"entryGroups\": [{
                  \"id\": \"testgroup1\",
                  \"entries\": [{
                    \"linkedResource\": \"//test/linked-resource-1\",
                    \"displayName\": \"Display name 1\",
                    \"type\": \"test_type\"
                  }]
                }]
              }, {
                \"name\": \"TestSystem2\",
                \"entryGroups\": [{
                  \"id\": \"testgroup2\",
                  \"entries\": [{
                    \"linkedResource\": \"//test/linked-resource-2\",
                    \"displayName\": \"Display name 2\",
                    \"type\": \"test_type\"
                  }]
                }]
              }]
            }
            ''')

        assembled_entry_groups = \
            custom_entries_json_reader.CustomEntriesJSONReader.read_file('file-path')

        self.assertEqual(2, len(assembled_entry_groups))

        _, groups_system_1 = assembled_entry_groups[0]
        _, groups_system_2 = assembled_entry_groups[1]

        group_1 = groups_system_1[0]
        group_2 = groups_system_2[0]

        self.assertEqual('testgroup1', group_1['id'])
        self.assertEqual('testgroup2', group_2['id'])

        entry_1 = group_1['entries'][0]
        entry_2 = group_2['entries'][0]

        self.assertEqual('TestSystem1', entry_1['user_specified_system'])
        self.assertEqual('TestSystem2', entry_2['user_specified_system'])

    def test_read_file_missing_key_field_should_fail(self, mock_open):
        mock_open.return_value = io.StringIO('{ \"specifiedSystems\": [] }')

        self.assertRaises(KeyError, custom_entries_json_reader.CustomEntriesJSONReader.read_file,
                          'file-path')

    def test_read_file_missing_optional_field_should_skip_entry_field(self, mock_open):
        mock_open.return_value = io.StringIO('''
            {
              \"userSpecifiedSystems\": [{
                \"name\": \"TestSystem\",
                \"entryGroups\": [{
                  \"id\": \"testgroup\",
                  \"entries\": [{
                    \"linkedResource\": \"//test/linked-resource\",
                    \"displayName\": \"Display name\",
                    \"type\": \"test_type\"
                  }]
                }]
              }]
            }
            ''')

        assembled_entry_groups = \
            custom_entries_json_reader.CustomEntriesJSONReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertFalse('description' in entry)

    def test_read_file_provided_optional_field_should_set_entry_field(self, mock_open):
        mock_open.return_value = io.StringIO('''
            {
              \"userSpecifiedSystems\": [{
                \"name\": \"TestSystem\",
                \"entryGroups\": [{
                  \"id\": \"testgroup\",
                  \"entries\": [{
                    \"linkedResource\": \"//test/linked-resource\",
                    \"displayName\": \"Display name\",
                    \"description\": \"Test description\",
                    \"type\": \"test_type\"
                  }]
                }]
              }]
            }
            ''')

        assembled_entry_groups = \
            custom_entries_json_reader.CustomEntriesJSONReader.read_file('file-path')

        _, groups = assembled_entry_groups[0]
        entry = groups[0]['entries'][0]

        self.assertEqual('Test description', entry['description'])
