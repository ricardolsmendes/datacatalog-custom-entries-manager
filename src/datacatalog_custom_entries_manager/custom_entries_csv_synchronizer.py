import logging
from typing import List

from google.cloud.datacatalog import types
from google.datacatalog_connectors.commons import cleanup, ingest, prepare

from . import data_catalog_entry_factory


class CustomEntriesCSVSynchronizer:

    def __init__(self, project_id, location_id):
        self.__project_id = project_id
        self.__location_id = location_id
        self.__data_catalog_entry_factory = data_catalog_entry_factory.DataCatalogEntryFactory(
            project_id, location_id)

    def sync_to_file(self, file_path: str) -> List[types.Entry]:
        """
        Synchronize Custom Entries to the CSV file contents.

        :param file_path: The CSV file path.
        :return: A list with the up to date Custom Entries.
        """
        logging.info('')
        logging.info('===== Synchronize Custom Entries to CSV [STARTED] ====')
