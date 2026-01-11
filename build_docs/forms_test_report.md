# Forms Test Report

## Overview
Automated tests were executed after installing project dependencies to validate the sponsor application, food vendor application, and liability application flows. The tests confirmed that submissions redirect on success and that records are persisted in the database.

## Environment
- Python 3.11
- Dependencies installed via `pip install -r requirements.txt`

## Test Coverage
- Sponsor application: required fields, support selection, logo upload, and database persistence.
- Food vendor application: required fields, vehicle details, payment selection, menu minimums, uploads, and database persistence.
- Liability application: required signature/name fields and database persistence.

## Commands Run
- `pip install -r requirements.txt`
- `pytest`

## Results
- All automated tests passed (20 total).
