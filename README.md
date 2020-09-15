# ALS Data Engineering

[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Instructions

This requires python > 3.7, ideally use a virtual environment but it's not strictly required:
1. `virtualenv -p /Users/YOURUSER/.pyenv/versions/3.7.0/bin/python3.7 .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements/prod.txt`
4. `PYTHONPATH=lib python3 bin/run_tasks.py`

## Dataset

A gzipped copy of the original input files (as of 2020-09-14) is available under the repo under [static/input](.static/input)

### Constituent Information

Columns:

- birth_dt
- change_password_next_login
- cons_id
- consent_type_id
- create_app
- create_dt
- create_user
- employer
- firstname
- gender
- income
- is_banned
- is_validated
- lastname
- middlename
- modified_app
- modified_dt
- modified_user
- note
- occupation
- password
- prefix
- salutation
- source
- status
- subsource
- suffix
- title
- userid

### Constituent Email Addresses

Columns:

- canonical_local_part
- cons_email_id
- cons_email_type_id
- cons_id
- create_app
- create_dt
- create_user
- domain
- double_validation
- email
- is_primary
- modified_app
- modified_dt
- modified_user
- note
- status

Notes:
Boolean columns (including `is_primary`) in all of these datasets are 1/0 numeric values. 1 means True, 0 means False.

### Constituent Subscription Status

Columns:

- cons_email_chapter_subscription_id
- cons_email_id
- chapter_id
- isunsub
- unsub_dt
- modified_dt

Notes:
 - We only care about subscription statuses where `chapter_id` is 1.
 - If an email is not present in this table, it is assumed to still be subscribed where `chapter_id` is 1.

## Tasks

### Task 1

Produce a "people" file with the following schema. Save it as a CSV with a header line to the working directory:

Column | Type | Description
-- | -- | --
email | string | Primary email address
code | string | Source code
is_unsub | boolean | Is the primary email address unsubscribed?
created_dt | datetime | Person creation datetime
updated_dt | datetime | Person updated datetime

### Task 2

Use the output of Task 1 to produce an "acquisition_facts" file with the following schema that aggregates stats about when people in the dataset were acquired. Save it to the working directory:

Column | Type | Description
-- | -- | --
acquisition_date | date | Calendar date of acquisition
acquisitions | int | Number of constituents acquired on acquisition_date
