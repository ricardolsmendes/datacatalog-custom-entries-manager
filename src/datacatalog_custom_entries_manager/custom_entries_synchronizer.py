import logging
from typing import Callable, Dict, List, Tuple

from google.cloud.datacatalog import types
from google.datacatalog_connectors.commons import cleanup, ingest, prepare

from . import custom_entries_csv_reader, custom_entries_json_reader, datacatalog_entry_factory


class CustomEntriesSynchronizer:

    def __init__(self, project_id, location_id):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__entry_factory = datacatalog_entry_factory.DataCatalogEntryFactory(
            project_id, location_id)

    def sync_to_file(self,
                     csv_file_path: str = None,
                     json_file_path: str = None) -> List[types.Entry]:
        """
        Synchronize Custom Entries to the provided file contents.

        :param
            csv_file_path: Path of a CSV file with metadata for the Custom Entries.
            json_file_path: Path of a JSON file with metadata for the Custom Entries.
        :return: A list with the up to date Custom Entries.
        """
        file_path = csv_file_path if csv_file_path else json_file_path if json_file_path else None

        logging.info('')
        logging.info('==== Synchronize Custom Entries to file [STARTED] =====')

        read_file: Callable[[str], List[Tuple[str, List[Dict[str, object]]]]] = \
            custom_entries_csv_reader.CustomEntriesCSVReader.read_file if csv_file_path \
            else custom_entries_json_reader.CustomEntriesJSONReader.read_file if json_file_path \
            else Exception('Either a CSV or a JSON file must be provided.')

        assembled_entry_groups = read_file(file_path)

        logging.info('')
        logging.info('>> Synchronizing file :: Data Catalog metadata...')

        entries = []
        for system_name, entry_groups in assembled_entry_groups:
            entries.extend([
                self.__synchronize_entry_group(entry_group, system_name)
                for entry_group in entry_groups
            ])

        logging.info('')
        logging.info('==== Synchronize Custom Entries to file [FINISHED] ====')

        return entries

    def __synchronize_entry_group(self, entry_group: Dict[str, object], system_name: str) \
            -> List[types.Entry]:

        group_id = entry_group.get('id')
        if not group_id:
            return []

        logging.info('')
        logging.info('Processing Entry Group: %s...', group_id)

        # Prepare: convert raw metadata into Data Catalog entries.
        logging.info('')
        logging.info('Converting raw metadata into Data Catalog entries...')

        entries = entry_group.get('entries')
        assembled_entries = self.__make_assembled_entries(group_id, entries) if entries else []
        logging.info('==== DONE ====')

        # Data Catalog cleanup: delete obsolete data.
        logging.info('')
        logging.info('Deleting obsolete metadata from Data Catalog...')

        cleaner = \
            cleanup.DataCatalogMetadataCleaner(self.__project_id, self.__location_id, group_id)
        cleaner.delete_obsolete_metadata(assembled_entries, f'system={system_name}')
        logging.info('==== DONE ====')

        logging.info('')
        if not assembled_entries:
            logging.info('No metadata to ingest...')
            return []

        # Ingest metadata into Data Catalog.
        logging.info('Ingesting metadata into Data Catalog...')

        ingestor = \
            ingest.DataCatalogMetadataIngestor(self.__project_id, self.__location_id, group_id)
        ingestor.ingest_metadata(assembled_entries)
        logging.info('==== DONE ====')

        return [assembled_entry.entry for assembled_entry in assembled_entries]

    def __make_assembled_entries(self, group_id, data):
        return [self.__make_assembled_entry(group_id, entry) for entry in data]

    def __make_assembled_entry(self, group_id, data):
        entry_id, entry = self.__entry_factory.make_entry_from_dict(group_id, data)
        return prepare.AssembledEntryData(entry_id, entry)
