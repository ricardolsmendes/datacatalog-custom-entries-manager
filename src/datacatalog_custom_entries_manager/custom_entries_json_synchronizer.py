import json
import logging

from google.datacatalog_connectors.commons import cleanup, ingest, prepare

from . import data_catalog_entry_factory


class CustomEntriesJSONSynchronizer:

    def __init__(self, project_id, location_id):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__data_catalog_entry_factory = data_catalog_entry_factory.DataCatalogEntryFactory(
            project_id, location_id)

    def sync_to_file(self, file_path):
        """
        Synchronize Custom Entries to a JSON file contents.

        :param file_path: The JSON file path.
        :return: A list with the up to date Custom Entries.
        """
        logging.info('')
        logging.info('===== Synchronize Custom Entries to JSON [STARTED] ====')

        logging.info('')
        logging.info('>> Reading the JSON file: %s...', file_path)

        with open(file_path) as json_file:
            data = json.load(json_file)

        logging.info('')
        logging.info('>> Synchronizing JSON :: Data Catalog metadata...')

        custom_entries = self.__synchronize_entry_groups(data)

        logging.info('')
        logging.info('==== Synchronize Custom Entries to JSON [FINISHED] ====')

        return custom_entries

    def __synchronize_entry_groups(self, data):
        entry_groups = data.get('entryGroups')
        user_specified_system = data.get('userSpecifiedSystem')
        return [
            self.__synchronize_entry_group(entry_group, user_specified_system)
            for entry_group in entry_groups
        ]

    def __synchronize_entry_group(self, data, user_specified_system):
        group_id = data.get('id')
        entries = data.get('entries')

        logging.info('')
        logging.info('Processing Entry Group: %s...', group_id)

        # Prepare: convert raw metadata into Data Catalog entries.
        logging.info('')
        logging.info('Converting raw metadata into Data Catalog entries...')

        assembled_entries = self.__make_assembled_entries(group_id, entries, user_specified_system)
        logging.info('==== DONE ====')

        # Data Catalog cleanup: delete obsolete data.
        logging.info('')
        logging.info('Deleting obsolete metadata from Data Catalog...')

        cleaner = cleanup.DataCatalogMetadataCleaner(
            self.__project_id, self.__location_id, group_id)
        cleaner.delete_obsolete_metadata(assembled_entries, f'system={user_specified_system}')
        logging.info('==== DONE ====')

        # Ingest metadata into Data Catalog.
        logging.info('')
        logging.info('Ingesting metadata into Data Catalog...')

        ingestor = ingest.DataCatalogMetadataIngestor(
            self.__project_id, self.__location_id, group_id)
        ingestor.ingest_metadata(assembled_entries)
        logging.info('==== DONE ====')

        return [assembled_entry.entry for assembled_entry in assembled_entries]

    def __make_assembled_entries(self, group_id, data, user_specified_system):
        return [
            self.__make_assembled_entry(group_id, entry, user_specified_system)
            for entry in data
        ]

    def __make_assembled_entry(self, group_id, data, user_specified_system):
        entry_id, entry = self.__data_catalog_entry_factory.make_entry_from_dict(
            group_id, data, user_specified_system)

        return prepare.AssembledEntryData(entry_id, entry)
