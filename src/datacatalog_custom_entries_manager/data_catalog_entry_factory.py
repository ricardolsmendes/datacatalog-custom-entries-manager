from datetime import datetime
from typing import Dict, Tuple

from google.cloud import datacatalog
from google.cloud.datacatalog import types
from google.datacatalog_connectors.commons import prepare


class DataCatalogEntryFactory(prepare.BaseEntryFactory):
    __DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, project_id, location_id):
        self.__project_id = project_id
        self.__location_id = location_id

    def make_entry_from_dict(self, group_id: str, data: Dict[str, str]) -> Tuple[str, types.Entry]:
        entry = types.Entry()

        generated_id = self.__format_id(data.get('display_name'))
        entry.name = datacatalog.DataCatalogClient.entry_path(self.__project_id,
                                                              self.__location_id, group_id,
                                                              generated_id)

        entry.linked_resource = data.get('linked_resource')
        entry.display_name = self._format_display_name(data.get('display_name'))

        description = data.get('description')
        if description:
            entry.description = description

        entry.user_specified_type = data.get('user_specified_type')
        entry.user_specified_system = data.get('user_specified_system')

        created_at = data.get('created_at')
        if created_at:
            entry.source_system_timestamps.create_time.seconds = \
                self.__convert_datetime_str_to_seconds(created_at)
        updated_at = data.get('updated_at')
        if updated_at:
            entry.source_system_timestamps.update_time.seconds = \
                self.__convert_datetime_str_to_seconds(updated_at)

        return generated_id, entry

    @classmethod
    def __format_id(cls, not_formatted_id):
        lower_case_id = not_formatted_id.lower()
        return cls._format_id(lower_case_id)

    @classmethod
    def __convert_datetime_str_to_seconds(cls, datetime_string):
        datetime_object = datetime.strptime(datetime_string, cls.__DATETIME_FORMAT)
        return int(datetime_object.timestamp())
