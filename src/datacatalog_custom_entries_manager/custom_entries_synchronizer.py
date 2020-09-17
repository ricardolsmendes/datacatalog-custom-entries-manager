from typing import Callable, List

from google.cloud.datacatalog import types

from . import custom_entries_csv_synchronizer, custom_entries_json_synchronizer


class CustomEntriesSynchronizer:

    def __init__(self, project_id, location_id):
        self.__csv_synchronizer: Callable[[str], List[types.Entry]] = \
            custom_entries_csv_synchronizer.CustomEntriesCSVSynchronizer(
                project_id, location_id).sync_to_file
        self.__json_synchronizer: Callable[[str], List[types.Entry]] = \
            custom_entries_json_synchronizer.CustomEntriesJSONSynchronizer(
                project_id, location_id).sync_to_file

    def sync_to_file(self, csv_file_path: str, json_file_path: str) -> List[types.Entry]:
        """
        Synchronize Custom Entries to the provided file contents.

        :param
            csv_file_path: Path of a CSV file with metadata for the Custom Entries.
            json_file_path: Path of a JSON file with metadata for the Custom Entries.
        :return: A list with the up to date Custom Entries.
        """
        file_path = csv_file_path if csv_file_path else json_file_path if json_file_path else None

        if not file_path:
            raise Exception('Either a CSV or a JSON file must be provided.')

        synchronizer = self.__csv_synchronizer if csv_file_path else self.__json_synchronizer

        return synchronizer(file_path)
