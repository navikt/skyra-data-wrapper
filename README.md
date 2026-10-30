# skyra data wrapper

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

This is a wrapper for Skyra APIs. You can use it to download survey responses and metadata for each survey. Built with requests and tqdm.

Install with

```bash
pip install skyra-data-wrapper
```

or 

```bash
uv add skyra-data-wrapper
```

## Supported APIs

- [Skyra Data Wrapper](#skyra-data-wrapper)
  - [Supported APIs](#supported-apis)
    - [Find surveys](#find-surveys)
    - [Download survey](#download-survey)

Note most of these APIs are still in beta and might change in the future.

### Find surveys

You can list all surveys available by your skyra token

```python
import src.skyra_data_wrapper.skyra_api as skyra

surveys = skyra.find_surveys(token=token)
```

<details>
<summary>Expandable example data</summary>

```json
{'data': {'items': [{'id': 'fafaa700-ade8-4ffb-9106-9f1ad293dd85',
    'name': 'Example',
    'slug': 'example'}],
  'pagination': {'limit': 2, 'nextCursor': None, 'hasMore': False},
  'organisation_id': 'fafaa700-ade8-4ffb-9106-9f1ad293dd85'}}
```

</details>

### Download survey

You can download a survey as json or csv.

For the csv format

```python
data = skyra.download_survey(
    survey_id=survey_ids[0],
    filename_path="data/test_survey.csv",
    token=token,
    format="csv",
)
```

For the json format

```python
data = skyra.download_survey(
    survey_id=survey_ids[0],
    filename_path="data/test_survey.json",
    token=token,
    format="json"
)
```

Downloading responses for a date range

```python
start = datetime(2026, 1, 5, 00, 00, tzinfo=zoneinfo.ZoneInfo("Europe/Oslo"))
end = datetime(2026, 1, 12, 00, 00, tzinfo=zoneinfo.ZoneInfo("Europe/Oslo"))

data = skyra.download_survey(
    survey_id=survey_ids[0],
    filename_path="data/test_survey_range.csv",
    token=token,
    format="csv",
    start_date=start.isoformat(),  # 2026-01-05T00:00:00+01:00 # 8601 with timezone oslo
    end_date=end.isoformat(),  # 2026-01-12T00:00:00+01:00
)
```


See more examples in [examples.py](/examples.py)