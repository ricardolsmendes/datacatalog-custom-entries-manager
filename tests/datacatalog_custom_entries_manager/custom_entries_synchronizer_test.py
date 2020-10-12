import unittest
from unittest import mock

from datacatalog_custom_entries_manager import custom_entries_synchronizer

_MANAGER_PACKAGE = 'datacatalog_custom_entries_manager'


@mock.patch(f'{_MANAGER_PACKAGE}.custom_entries_csv_reader.CustomEntriesCSVReader')
class CustomEntriesSynchronizer(unittest.TestCase):
    __CONNECTORS_COMMONS_PACKAGE = 'google.datacatalog_connectors.commons'

    @mock.patch(f'{_MANAGER_PACKAGE}.datacatalog_entry_factory.DataCatalogEntryFactory')
    def setUp(self, mock_entry_factory):
        self.__synchronizer = custom_entries_synchronizer.CustomEntriesSynchronizer(
            'test-project', 'test-location')

    def test_constructor_should_set_instance_attributes(self, mock_csv_reader):
        attrs = self.__synchronizer.__dict__

        self.assertEqual('test-project', attrs['_CustomEntriesSynchronizer__project_id'])
        self.assertEqual('test-location', attrs['_CustomEntriesSynchronizer__location_id'])
        self.assertIsNotNone(attrs['_CustomEntriesSynchronizer__entry_factory'])

    @mock.patch(f'{_MANAGER_PACKAGE}.custom_entries_json_reader.CustomEntriesJSONReader')
    def test_sync_to_file_csv_file_path_should_call_csv_reader(self, mock_json_reader,
                                                               mock_csv_reader):

        mock_csv_reader.read_file.return_value = []

        self.__synchronizer.sync_to_file(csv_file_path='file-path')

        mock_csv_reader.read_file.assert_called_once()
        mock_json_reader.read_file.assert_not_called()

    @mock.patch(f'{_MANAGER_PACKAGE}.custom_entries_json_reader.CustomEntriesJSONReader')
    def test_sync_to_file_json_file_path_should_call_json_reader(self, mock_json_reader,
                                                                 mock_csv_reader):

        mock_json_reader.read_file.return_value = []

        self.__synchronizer.sync_to_file(json_file_path='file-path')

        mock_csv_reader.read_file.assert_not_called()
        mock_json_reader.read_file.assert_called_once()

    def test_sync_to_file_no_file_path_should_fail(self, mock_csv_reader):
        self.assertRaises(Exception, self.__synchronizer.sync_to_file)

    def test_sync_to_file_no_entry_group_should_do_nothing(self, mock_csv_reader):
        mock_csv_reader.read_file.return_value = [('TestSystem', [])]
        self.assertIsNotNone(self.__synchronizer.sync_to_file(csv_file_path='file-path'))

    def test_sync_to_file_no_entry_group_id_should_do_nothing(self, mock_csv_reader):
        mock_csv_reader.read_file.return_value = [('TestSystem', [{}])]
        self.assertIsNotNone(self.__synchronizer.sync_to_file(csv_file_path='file-path'))

    @mock.patch(f'{__CONNECTORS_COMMONS_PACKAGE}.cleanup.DataCatalogMetadataCleaner')
    def test_sync_to_file_no_entries_should_cleanup_catalog(self, mock_metadata_cleaner,
                                                            mock_csv_reader):

        mock_csv_reader.read_file.return_value = [('TestSystem', [{'id': 'testgroup'}])]

        self.__synchronizer.sync_to_file(csv_file_path='file-path')

        cleaner = mock_metadata_cleaner.return_value
        cleaner.delete_obsolete_metadata.assert_called_once()

    @mock.patch(f'{__CONNECTORS_COMMONS_PACKAGE}.ingest.DataCatalogMetadataIngestor')
    @mock.patch(f'{__CONNECTORS_COMMONS_PACKAGE}.cleanup.DataCatalogMetadataCleaner')
    def test_sync_to_file_with_entries_should_ingest_into_catalog(self, mock_metadata_cleaner,
                                                                  mock_metadata_ingestor,
                                                                  mock_csv_reader):

        mock_csv_reader.read_file.return_value = [('TestSystem', [{
            'id': 'testgroup',
            'entries': [{}]
        }])]

        entry_factory = self.__synchronizer.__dict__['_CustomEntriesSynchronizer__entry_factory']
        entry_factory.make_entry_from_dict.return_value = ('entry_id', {})

        self.__synchronizer.sync_to_file(csv_file_path='file-path')

        ingestor = mock_metadata_ingestor.return_value
        ingestor.ingest_metadata.assert_called_once()
