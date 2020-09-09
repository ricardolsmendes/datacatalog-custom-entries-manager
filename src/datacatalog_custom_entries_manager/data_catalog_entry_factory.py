from datetime import datetime
from google.cloud.datacatalog import types

from google.cloud import datacatalog
from google.datacatalog_connectors.commons import prepare


class DataCatalogEntryFactory(prepare.BaseEntryFactory):
    __DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

    def __init__(self, project_id, location_id):
        self.__project_id = project_id
        self.__location_id = location_id

    def make_entry_from_dict(self, group_id, data, user_specified_system):
        entry = types.Entry()

        generated_id = self.__format_id(data.get('displayName'))
        entry.name = datacatalog.DataCatalogClient.entry_path(
            self.__project_id, self.__location_id, group_id, generated_id)

        entry.linked_resource = data.get('linkedResource')
        entry.display_name = self._format_display_name(data.get('displayName'))
        entry.description = data.get('description', '')

        entry.user_specified_type = data.get('userSpecifiedType')
        entry.user_specified_system = user_specified_system

        entry.source_system_timestamps.create_time.seconds = \
            self.__convert_datetime_str_to_seconds(data.get('createdAt'))
        entry.source_system_timestamps.update_time.seconds = \
            self.__convert_datetime_str_to_seconds(data.get('updatedAt'))

        return generated_id, entry

    @classmethod
    def __format_id(cls, unformatted_id):
        lower_case_id = unformatted_id.lower()
        return cls._format_id(lower_case_id)

    @classmethod
    def __convert_datetime_str_to_seconds(cls, datetime_string):
        datetime_object = datetime.strptime(datetime_string, cls.__DATETIME_FORMAT)
        return int(datetime_object.timestamp())
