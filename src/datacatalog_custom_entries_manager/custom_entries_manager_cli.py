import argparse
import logging
import sys

from . import custom_entries_synchronizer


class CustomEntriesManagerCLI:

    @classmethod
    def run(cls, argv):
        cls.__setup_logging()

        args = cls._parse_args(argv)
        args.func(args)

    @classmethod
    def __setup_logging(cls):
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def _parse_args(cls, argv):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        subparsers = parser.add_subparsers()

        sync_entries_parser = subparsers.add_parser('sync', help='Synchronize Custom Entries')
        sync_entries_parser.add_argument('--csv-file',
                                         help='CSV file with metadata for the Custom Entries')
        sync_entries_parser.add_argument('--json-file',
                                         help='JSON file with metadata for the Custom Entries')
        sync_entries_parser.add_argument('--project-id',
                                         help='Google Cloud Project ID',
                                         required=True)
        sync_entries_parser.add_argument('--location-id',
                                         help='Google Cloud Location ID',
                                         required=True)
        sync_entries_parser.set_defaults(func=cls.__synchronize_custom_entries)

        return parser.parse_args(argv)

    @classmethod
    def __synchronize_custom_entries(cls, args):
        custom_entries_synchronizer.CustomEntriesSynchronizer(args.project_id, args.location_id)\
            .sync_to_file(csv_file_path=args.csv_file, json_file_path=args.json_file)


def main():
    argv = sys.argv
    CustomEntriesManagerCLI.run(argv[1:] if len(argv) > 0 else argv)
