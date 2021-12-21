# datacatalog-custom-entries-manager

A Python package intended to manage Google Cloud [Data Catalog custom entries][1], loading metadata
from external sources. Currently supports the CSV and JSON file formats.

It is built on top of [GoogleCloudPlatform/datacatalog-connectors][2] and, differently from the
existing connectors, allows ingesting metadata with no need to connect to other systems than Data
Catalog. Known use cases include validating Custom Entries ingestion workloads before coding their
specific features and loading metadata into development / PoC environments.

In case you need not only Entries but also Tags to validate your model/workload, consider giving
[datacatalog-custom-model-manager][3] a try.

[![license](https://img.shields.io/github/license/ricardolsmendes/datacatalog-custom-entries-manager.svg)](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/blob/master/LICENSE)
[![pypi](https://img.shields.io/pypi/v/datacatalog-custom-entries-manager.svg)](https://pypi.org/project/datacatalog-custom-entries-manager)
[![issues](https://img.shields.io/github/issues/ricardolsmendes/datacatalog-custom-entries-manager.svg)](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/issues)
[![continuous integration](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/actions/workflows/continuous-integration.yaml/badge.svg)](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/actions/workflows/continuous-integration.yaml)
[![continuous delivery](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/actions/workflows/continuous-delivery.yaml/badge.svg)](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/actions/workflows/continuous-delivery.yaml)

<!--
  DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY
  run `npx markdown-toc -i README.md`.

  Please stick to 100-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Environment setup](#1-environment-setup)
  * [1.1. Python + virtualenv](#11-python--virtualenv)
    + [1.1.1. Install Python 3.6+](#111-install-python-36)
    + [1.1.2. Create a folder](#112-create-a-folder)
    + [1.1.3. Create and activate an isolated Python environment](#113-create-and-activate-an-isolated-python-environment)
    + [1.1.4. Install the package](#114-install-the-package)
  * [1.2. Docker](#12-docker)
    + [1.2.1. Get the source code](#121-get-the-source-code)
  * [1.3. Auth credentials](#13-auth-credentials)
    + [1.3.1. Create a service account and grant it below roles](#131-create-a-service-account-and-grant-it-below-roles)
    + [1.3.2. Download a JSON key and save it as](#132-download-a-json-key-and-save-it-as)
    + [1.3.3. Set the environment variables](#133-set-the-environment-variables)
- [2. Manage Custom Entries](#2-manage-custom-entries)
  * [2.1. Synchronize](#21-synchronize)
    + [2.1.1. To a CSV file](#211-to-a-csv-file)
    + [2.1.2. To a JSON file](#212-to-a-json-file)
- [3. How to contribute](#3-how-to-contribute)
  * [3.1. Report issues](#31-report-issues)
  * [3.2. Contribute code](#32-contribute-code)

<!-- tocstop -->

---

## 1. Environment setup

### 1.1. Python + virtualenv

Using [virtualenv][4] is optional, but strongly recommended unless you use [Docker](#12-docker).

#### 1.1.1. Install Python 3.6+

#### 1.1.2. Create a folder

This is recommended so all related stuff will reside at the same place, making it easier to follow
the next instructions.

```sh
mkdir ./datacatalog-custom-entries-manager
cd ./datacatalog-custom-entries-manager
```

_All paths starting with `./` in the next steps are relative to the
`datacatalog-custom-entries-manager` folder._

#### 1.1.3. Create and activate an isolated Python environment

```sh
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

#### 1.1.4. Install the package

```sh
pip install --upgrade datacatalog-custom-entries-manager
```

### 1.2. Docker

_Docker_ may be used as an option to run `datacatalog-custom-entries-manager`. In this case,
please disregard the [above](#11-python--virtualenv) _virtualenv_ setup instructions.

#### 1.2.1. Get the source code

```sh
git clone https://github.com/ricardolsmendes/datacatalog-custom-entries-manager
cd ./datacatalog-custom-entries-manager
```

### 1.3. Auth credentials

#### 1.3.1. Create a service account and grant it below roles

- `DataCatalog entryGroup Owner`
- `DataCatalog entry Owner`
- `Data Catalog Viewer`

#### 1.3.2. Download a JSON key and save it as

- `./credentials/datacatalog-custom-entries-manager.json`

#### 1.3.3. Set the environment variables

_This step can be skipped if you're using [Docker](#12-docker)._

```sh
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/datacatalog-custom-entries-manager.json
```

## 2. Manage Custom Entries

### 2.1. Synchronize

#### 2.1.1. To a CSV file

- _SCHEMA_

The metadata schema to synchronize Custom Entries is presented below. Use as many lines as needed
to describe all Data Catalog Entries you need.

| Column                    | Description                                                                                                                                                                | Mandatory |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------: |
| **user_specified_system** | Indicates the Entry source system                                                                                                                                          |  &check;  |
| **group_id**              | Id of the Entry Group the Entry belongs to                                                                                                                                 |  &check;  |
| **linked_resource**       | The resource a metadata Entry refers to                                                                                                                                    |  &check;  |
| **display_name**          | Display information such as title and description; a short name to identify the Entry (the `entry_id` field will be generated as a normalized version of the display name) |  &check;  |
| **description**           | Can consist of several sentences that describe the Entry contents                                                                                                          |  &cross;  |
| **user_specified_type**   | A custom value indicating the Entry type                                                                                                                                   |  &check;  |
| **created_at**            | The creation time of the underlying resource, not of the Data Catalog Entry (format: YYYY-MM-DDTHH:MM:SSZ)                                                                 |  &cross;  |
| **updated_at**            | The last-modified time of the underlying resource, not of the Data Catalog Entry (format: YYYY-MM-DDTHH:MM:SSZ)                                                            |  &cross;  |

- _SAMPLE INPUT_

1. [sample-input/csv][5] for reference;
1. [Data Catalog Sample Custom Entries][6] (Google Sheets) might help to create/export a CSV file.

- _COMMANDS_

**Python + virtualenv**

```sh
datacatalog-custom-entries sync \
  --csv-file <CSV-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

**Docker**

```sh
docker build --rm --tag datacatalog-custom-entries-manager .
docker run --rm --tty \
  --volume <CREDENTIALS-FILE-DIR>:/credentials --volume <CSV-FILE-DIR>:/data \
  datacatalog-custom-entries-manager sync \
  --csv-file /data/<CSV-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

#### 2.1.2. To a JSON file

- _STRUCTURE_

The metadata structure to synchronize Custom Entries is presented below. Use as many objects as
needed to describe all Data Catalog Entries you need.

```json
{
  "userSpecifiedSystems": [
    {
      "name": "STRING",
      "entryGroups": [
        {
          "id": "STRING",
          "entries": [
            {
              "linkedResource": "STRING",
              "displayName": "STRING",
              "description": "STRING (optional)",
              "type": "STRING",
              "createdAt": "STRING (optional, format: YYYY-MM-DDTHH:MM:SSZ)",
              "updatedAt": "STRING (optional, format: YYYY-MM-DDTHH:MM:SSZ)"
            }
          ]
        }
      ]
    }
  ]
}
```

- _SAMPLE INPUT_

1. [sample-input/json][7] for reference;

- _COMMANDS_

**Python + virtualenv**

```sh
datacatalog-custom-entries sync \
  --json-file <JSON-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

**Docker**

```sh
docker build --rm --tag datacatalog-custom-entries-manager .
docker run --rm --tty \
  --volume <CREDENTIALS-FILE-DIR>:/credentials --volume <CSV-FILE-DIR>:/data \
  datacatalog-custom-entries-manager sync \
  --json-file <JSON-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

## 3. How to contribute

Please make sure to take a moment and read the [Code of
Conduct](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/blob/master/.github/CODE_OF_CONDUCT.md).

### 3.1. Report issues

Please report bugs and suggest features via the [GitHub
Issues](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/issues).

Before opening an issue, search the tracker for possible duplicates. If you find a duplicate, please
add a comment saying that you encountered the problem as well.

### 3.2. Contribute code

Please make sure to read the [Contributing
Guide](https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/blob/master/.github/CONTRIBUTING.md)
before making a pull request.

[1]: https://cloud.google.com/data-catalog/docs/how-to/custom-entries
[2]: https://github.com/GoogleCloudPlatform/datacatalog-connectors
[3]: https://github.com/ricardolsmendes/datacatalog-custom-model-manager
[4]: https://virtualenv.pypa.io/en/latest/
[5]: https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/tree/master/sample-input/csv
[6]: https://docs.google.com/spreadsheets/d/1F_6M1BA9qlcGZf_ZyC3cUAePUjMXInZWbUOSGow5Gfc
[7]: https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/tree/master/sample-input/json
