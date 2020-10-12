# datacatalog-custom-entries-manager

Python package to manage Google Cloud [Data Catalog custom entries][1], loading metadata from
external sources. Currently supports the CSV and JSON file formats.

![Continuous Integration][2]

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
  * [2.1. Synchronize Data Catalog](#21-synchronize-data-catalog)
    + [2.1.1. To a CSV file](#211-to-a-csv-file)
    + [2.1.2. To a JSON file](#212-to-a-json-file)

<!-- tocstop -->

## 1. Environment setup

### 1.1. Python + virtualenv

Using [virtualenv][3] is optional, but strongly recommended unless you use [Docker](#12-docker).

#### 1.1.1. Install Python 3.6+

#### 1.1.2. Create a folder

This is recommended so all related stuff will reside at the same place, making it easier to follow
below instructions.

````bash
mkdir ./datacatalog-custom-entries-manager
cd ./datacatalog-custom-entries-manager
````

_All paths starting with `./` in the next steps are relative to the
`datacatalog-custom-entries-manager` folder._

#### 1.1.3. Create and activate an isolated Python environment

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

#### 1.1.4. Install the package

```bash
pip install --upgrade datacatalog-custom-entries-manager
```

### 1.2. Docker

Docker may be used as an alternative to run `datacatalog-custom-entries-manager`. In this case,
please disregard the [above](#11-python--virtualenv) _virtualenv_ setup instructions.

#### 1.2.1. Get the source code

```bash
git clone https://github.com/ricardolsmendes/datacatalog-custom-entries-manager
cd ./datacatalog-custom-entries-manager
```

### 1.3. Auth credentials

#### 1.3.1. Create a service account and grant it below roles

- DataCatalog entryGroup Owner
- DataCatalog entry Owner
- Data Catalog Viewer 

#### 1.3.2. Download a JSON key and save it as
- `./credentials/datacatalog-custom-entries-manager.json`

#### 1.3.3. Set the environment variables

_This step can be skipped if you're using [Docker](#12-docker)._

```bash
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/datacatalog-custom-entries-manager.json
```

## 2. Manage Custom Entries

### 2.1. Synchronize Data Catalog

#### 2.1.1. To a CSV file

- *SAMPLE INPUT* 

1. [sample-input/csv][4] for reference;
1. [Data Catalog Sample Custom Entries][5] (Google Sheets) might help to create/export a CSV file.

- *COMMANDS*

**Python + virtualenv**

```bash
datacatalog-custom-entries sync \
  --csv-file <CSV-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

**Docker**

```bash
docker build --rm --tag datacatalog-custom-entries-manager .
docker run --rm --tty \
  --volume <CREDENTIALS-FILE-FOLDER>:/credentials --volume <CSV-FILE-FOLDER>:/data \
  datacatalog-custom-entries-manager sync \
  --csv-file /data/<CSV-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

#### 2.1.2. To a JSON file

- *SAMPLE INPUT* 

1. [sample-input/json][6] for reference;

- *COMMANDS*

**Python + virtualenv**

```bash
datacatalog-custom-entries sync \
  --json-file <JSON-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

**Docker**

```bash
docker build --rm --tag datacatalog-custom-entries-manager .
docker run --rm --tty \
  --volume <CREDENTIALS-FILE-FOLDER>:/credentials --volume <CSV-FILE-FOLDER>:/data \
  datacatalog-custom-entries-manager sync \
  --json-file <JSON-FILE-PATH> \
  --project-id <YOUR-PROJECT-ID> --location-id <YOUR-LOCATION-ID>
```

[1]: https://cloud.google.com/data-catalog/docs/how-to/custom-entries
[2]: https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/workflows/Continuous%20Integration/badge.svg
[3]: https://virtualenv.pypa.io/en/latest/
[4]: https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/tree/master/sample-input/csv
[5]: https://docs.google.com/spreadsheets/d/1F_6M1BA9qlcGZf_ZyC3cUAePUjMXInZWbUOSGow5Gfc
[6]: https://github.com/ricardolsmendes/datacatalog-custom-entries-manager/tree/master/sample-input/json
