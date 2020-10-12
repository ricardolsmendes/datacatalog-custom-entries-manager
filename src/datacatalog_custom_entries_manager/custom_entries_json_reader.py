import json
import logging
from typing import Dict, List, Tuple

from . import constant


class CustomEntriesJSONReader:

    @classmethod
    def read_file(cls, file_path: str) -> List[Tuple[str, List[Dict[str, object]]]]:
        """
        Read Custom Entries from a JSON file.

        :param file_path: The JSON file path.
        :return: A list with Entry Group ``dicts`` assembled
            by their parent User Specified Systems.
        """
        logging.info('')
        logging.info('>> Reading the JSON file: %s...', file_path)

        with open(file_path) as json_file:
            json_data = json.load(json_file)

        return cls.__assemble_entry_groups_from_system_indexed_data(json_data)

    @classmethod
    def __assemble_entry_groups_from_system_indexed_data(cls, json_object: Dict[str, object]) \
            -> List[Tuple[str, List[Dict[str, object]]]]:

        systems_json = json_object[constant.ENTRIES_JSON_USER_SPECIFIED_SYSTEMS_FIELD_NAME]
        return [cls.__assemble_entry_groups_by_system(system_json) for system_json in systems_json]

    @classmethod
    def __assemble_entry_groups_by_system(cls, json_object: Dict[str, object]) \
            -> Tuple[str, List[Dict[str, object]]]:

        system_name = json_object[constant.ENTRIES_JSON_USER_SPECIFIED_SYSTEM_FIELD_NAME]
        groups_json = json_object[constant.ENTRIES_JSON_ENTRY_GROUPS_FIELD_NAME]
        return \
            system_name, \
            [cls.__make_entry_group(group_json, system_name) for group_json in groups_json]

    @classmethod
    def __make_entry_group(cls, json_object: Dict[str, object], system_name: str) \
            -> Dict[str, object]:

        entries_json = json_object[constant.ENTRIES_JSON_ENTRIES_FIELD_NAME]
        return {
            'id': json_object.get(constant.ENTRIES_JSON_ENTRY_GROUP_ID_FIELD_NAME),
            'entries': [cls.__make_entry(entry_json, system_name) for entry_json in entries_json]
        }

    @classmethod
    def __make_entry(cls, json_object: Dict[str, object], system_name: str) -> Dict[str, object]:
        # Mandatory fields
        entry = {
            'linked_resource': json_object[constant.ENTRIES_JSON_LINKED_RESOURCE_FIELD_NAME],
            'display_name': json_object[constant.ENTRIES_JSON_DISPLAY_NAME_FIELD_NAME],
            'user_specified_type':
            json_object[constant.ENTRIES_JSON_USER_SPECIFIED_TYPE_FIELD_NAME],
            'user_specified_system': system_name,
        }

        # Optional fields
        cls.__set_optional_string_field(
            entry, 'description', json_object.get(constant.ENTRIES_JSON_DESCRIPTION_FIELD_NAME))

        cls.__set_optional_string_field(
            entry, 'created_at', json_object.get(constant.ENTRIES_JSON_CREATED_AT_FIELD_NAME))

        cls.__set_optional_string_field(
            entry, 'updated_at', json_object.get(constant.ENTRIES_JSON_UPDATED_AT_FIELD_NAME))

        return entry

    @classmethod
    def __set_optional_string_field(cls, entry: Dict[str, object], field_id: str, value: object):
        if value and isinstance(value, str):
            entry[field_id] = value
