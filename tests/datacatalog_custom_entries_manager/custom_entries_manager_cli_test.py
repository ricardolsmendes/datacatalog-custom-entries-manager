import unittest
from unittest import mock

import datacatalog_custom_entries_manager
from datacatalog_custom_entries_manager import custom_entries_manager_cli


class CustomEntriesManagerCLITest(unittest.TestCase):

    def test_parse_args_invalid_subcommand_should_raise_system_exit(self):
        self.assertRaises(SystemExit,
                          custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args,
                          ['create'])

    def test_parse_args_sync_entries_missing_mandatory_args_should_raise_system_exit(self):
        self.assertRaises(SystemExit,
                          custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args, ['sync'])

    def test_parse_args_sync_entries_should_parse_mandatory_args_csv(self):
        args = custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args([
            'sync', '--csv-file', 'test.csv', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])
        self.assertEqual('test.csv', args.csv_file)
        self.assertEqual('test-project', args.project_id)
        self.assertEqual('test-location', args.location_id)

    def test_parse_args_sync_entries_should_parse_mandatory_args_json(self):
        args = custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args([
            'sync', '--json-file', 'test.json', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])
        self.assertEqual('test.json', args.json_file)
        self.assertEqual('test-project', args.project_id)
        self.assertEqual('test-location', args.location_id)

    def test_run_no_args_should_raise_attribute_error(self):
        self.assertRaises(AttributeError, custom_entries_manager_cli.CustomEntriesManagerCLI.run,
                          None)

    @mock.patch('datacatalog_custom_entries_manager.custom_entries_manager_cli.'
                'custom_entries_synchronizer.CustomEntriesSynchronizer')
    def test_run_sync_entries_should_call_processor_sync_to_file_csv(
            self, mock_custom_entries_synchronizer):

        custom_entries_manager_cli.CustomEntriesManagerCLI.run([
            'sync', '--csv-file', 'test.csv', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])

        custom_entries_synchronizer = mock_custom_entries_synchronizer.return_value
        custom_entries_synchronizer.sync_to_file.assert_called_once()
        custom_entries_synchronizer.sync_to_file.assert_called_with(csv_file_path='test.csv',
                                                                    json_file_path=None)

    @mock.patch('datacatalog_custom_entries_manager.custom_entries_manager_cli.'
                'custom_entries_synchronizer.CustomEntriesSynchronizer')
    def test_run_sync_entries_should_call_processor_sync_to_file_json(
            self, mock_custom_entries_synchronizer):

        custom_entries_manager_cli.CustomEntriesManagerCLI.run([
            'sync', '--json-file', 'test.json', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])

        custom_entries_synchronizer = mock_custom_entries_synchronizer.return_value
        custom_entries_synchronizer.sync_to_file.assert_called_once()
        custom_entries_synchronizer.sync_to_file.assert_called_with(csv_file_path=None,
                                                                    json_file_path='test.json')

    @mock.patch(
        'datacatalog_custom_entries_manager.custom_entries_manager_cli.CustomEntriesManagerCLI')
    def test_main_should_call_cli_run(self, mock_cli):
        datacatalog_custom_entries_manager.main()
        mock_cli.run.assert_called_once()
