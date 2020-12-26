import unittest
from unittest import mock

import datacatalog_custom_entries_manager
from datacatalog_custom_entries_manager import custom_entries_manager_cli


class CustomEntriesManagerCLITest(unittest.TestCase):
    __CLI_MODULE = 'datacatalog_custom_entries_manager.custom_entries_manager_cli'
    __CLI_CLASS = f'{__CLI_MODULE}.CustomEntriesManagerCLI'

    @mock.patch(f'{__CLI_CLASS}._parse_args')
    def test_run_should_parse_args(self, mock_parse_args):
        custom_entries_manager_cli.CustomEntriesManagerCLI.run([])
        mock_parse_args.assert_called_once()

    @mock.patch(f'{__CLI_CLASS}._CustomEntriesManagerCLI__synchronize_custom_entries')
    @mock.patch(f'{__CLI_CLASS}._parse_args')
    def test_run_sync_should_call_synchronize_custom_entries(self, mock_parse_args,
                                                             mock_synchronize_custom_entries):

        mock_parse_args.return_value.func = mock_synchronize_custom_entries
        custom_entries_manager_cli.CustomEntriesManagerCLI.run([])
        mock_synchronize_custom_entries.assert_called_once_with(mock_parse_args.return_value)

    def test_parse_args_no_subcommand_should_raise_system_exit(self):
        self.assertRaises(SystemExit,
                          custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args,
                          ['--csv-file', 'test.csv'])

    def test_parse_args_invalid_subcommand_should_raise_system_exit(self):
        self.assertRaises(SystemExit,
                          custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args,
                          ['create'])

    def test_parse_args_sync_missing_mandatory_args_should_raise_system_exit(self):
        self.assertRaises(SystemExit,
                          custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args, ['sync'])

    def test_parse_args_sync_should_parse_mandatory_args(self):
        args = custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args(
            ['sync', '--project-id', 'test-project', '--location-id', 'test-location'])
        self.assertEqual('test-project', args.project_id)
        self.assertEqual('test-location', args.location_id)

    def test_parse_args_sync_should_parse_optional_args_csv(self):
        args = custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args([
            'sync', '--csv-file', 'test.csv', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])
        self.assertEqual('test.csv', args.csv_file)

    def test_parse_args_sync_should_parse_optional_args_json(self):
        args = custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args([
            'sync', '--json-file', 'test.json', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])
        self.assertEqual('test.json', args.json_file)

    @mock.patch(f'{__CLI_CLASS}._CustomEntriesManagerCLI__synchronize_custom_entries')
    def test_parse_args_sync_should_set_default_function(self, mock_synchronize_custom_entries):
        args = custom_entries_manager_cli.CustomEntriesManagerCLI._parse_args(
            ['sync', '--project-id', 'test-project', '--location-id', 'test-location'])
        self.assertEqual(mock_synchronize_custom_entries, args.func)

    @mock.patch(f'{__CLI_MODULE}.custom_entries_synchronizer.CustomEntriesSynchronizer')
    def test_sync_should_sync_to_csv_file(self, mock_custom_entries_synchronizer):
        custom_entries_manager_cli.CustomEntriesManagerCLI.run([
            'sync', '--csv-file', 'test.csv', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])
        mock_custom_entries_synchronizer.assert_called_with('test-project', 'test-location')
        mock_custom_entries_synchronizer.return_value.sync_to_file.assert_called_with(
            csv_file_path='test.csv', json_file_path=None)

    @mock.patch(f'{__CLI_MODULE}.custom_entries_synchronizer.CustomEntriesSynchronizer')
    def test_sync_should_sync_to_json_file(self, mock_custom_entries_synchronizer):
        custom_entries_manager_cli.CustomEntriesManagerCLI.run([
            'sync', '--json-file', 'test.json', '--project-id', 'test-project', '--location-id',
            'test-location'
        ])
        mock_custom_entries_synchronizer.assert_called_with('test-project', 'test-location')
        mock_custom_entries_synchronizer.return_value.sync_to_file.assert_called_with(
            csv_file_path=None, json_file_path='test.json')

    @mock.patch(f'{__CLI_CLASS}.run')
    def test_main_should_call_cli_run(self, mock_run):
        datacatalog_custom_entries_manager.main()
        mock_run.assert_called_once()
