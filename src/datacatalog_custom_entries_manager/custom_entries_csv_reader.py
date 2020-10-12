import logging
from typing import Dict, List, Tuple

import pandas as pd

from . import constant


class CustomEntriesCSVReader:

    @classmethod
    def read_file(cls, file_path: str) -> List[Tuple[str, List[Dict[str, object]]]]:
        """
        Read Custom Entries from a JSON file.

        :param file_path: The JSON file path.
        :return: A list with Entry Group ``dicts`` assembled
            by their parent User Specified Systems.
        """
        logging.info('')
        logging.info('>> Reading the CSV file: %s...', file_path)

        dataframe = pd.read_csv(file_path)

        return cls.__assemble_entry_groups_from_system_indexable_dataframe(dataframe)

    @classmethod
    def __assemble_entry_groups_from_system_indexable_dataframe(cls, dataframe) \
            -> List[Tuple[str, List[Dict[str, object]]]]:

        normalized_df = cls.__normalize_dataframe(dataframe)
        normalized_df.set_index(constant.ENTRIES_DS_USER_SPECIFIED_SYSTEM_COLUMN_LABEL,
                                inplace=True)

        assembled_entry_groups = []
        for system in normalized_df.index.unique().tolist():
            entry_groups_subset = \
                normalized_df.loc[[system], constant.ENTRIES_DS_GROUP_ID_COLUMN_LABEL:]

            # Save memory by deleting data already copied to a subset.
            normalized_df.drop(system, inplace=True)

            assembled_entry_groups.append(
                (system, cls.__make_entry_groups(entry_groups_subset, system)))

        return assembled_entry_groups

    @classmethod
    def __normalize_dataframe(cls, dataframe):
        # Reorder dataframe columns.
        ordered_df = dataframe.reindex(columns=constant.ENTRIES_DS_COLUMNS_ORDER, copy=False)

        # Fill NA/NaN values by propagating the last valid observation forward to next valid.
        filled_subset = ordered_df[constant.ENTRIES_DS_FILLABLE_COLUMNS].fillna(method='pad')

        # Rebuild the dataframe by concatenating the fillable and non-fillable columns.
        rebuilt_df = pd.concat(
            [filled_subset, ordered_df[constant.ENTRIES_DS_NON_FILLABLE_COLUMNS]], axis=1)

        return rebuilt_df

    @classmethod
    def __make_entry_groups(cls, dataframe, system_name: str) -> List[Dict[str, object]]:
        dataframe.set_index(constant.ENTRIES_DS_GROUP_ID_COLUMN_LABEL, inplace=True)

        entry_groups = []
        for group_id in dataframe.index.unique().tolist():
            entries_subset = \
                dataframe.loc[[group_id], constant.ENTRIES_DS_DISPLAY_NAME_COLUMN_LABEL:]

            # Save memory by deleting data already copied to a subset.
            dataframe.drop(group_id, inplace=True)

            entry_groups.append({
                'id': group_id,
                'entries': cls.__make_entries(entries_subset, system_name)
            })

        return entry_groups

    @classmethod
    def __make_entries(cls, dataframe, system_name: str) -> List[Dict[str, object]]:
        records = dataframe.to_dict(orient='records')
        return [cls.__make_entry(record, system_name) for record in records]

    @classmethod
    def __make_entry(cls, record: Dict[str, object], system_name: str) -> Dict[str, object]:
        # Mandatory fields
        entry = {
            'linked_resource': record[constant.ENTRIES_DS_LINKED_RESOURCE_COLUMN_LABEL],
            'display_name': record[constant.ENTRIES_DS_DISPLAY_NAME_COLUMN_LABEL],
            'user_specified_type': record[constant.ENTRIES_DS_USER_SPECIFIED_TYPE_COLUMN_LABEL],
            'user_specified_system': system_name,
        }

        # Optional fields
        cls.__set_optional_string_field(entry, 'description',
                                        record[constant.ENTRIES_DS_DESCRIPTION_COLUMN_LABEL])
        cls.__set_optional_string_field(entry, 'created_at',
                                        record[constant.ENTRIES_DS_CREATED_AT_COLUMN_LABEL])
        cls.__set_optional_string_field(entry, 'updated_at',
                                        record[constant.ENTRIES_DS_UPDATED_AT_COLUMN_LABEL])

        return entry

    @classmethod
    def __set_optional_string_field(cls, entry: Dict[str, object], field_id: str, value: object):
        # Pandas is not aware of the field types and reads empty values as NaN (float),
        # hence the type check.
        if value and isinstance(value, str):
            entry[field_id] = value
