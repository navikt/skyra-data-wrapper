# %%
import os
import json
from datetime import datetime
import zoneinfo

from dotenv import load_dotenv

import src.skyra_data_wrapper.skyra_api as skyra

# %%
load_dotenv()

token = os.getenv("api_key")
# %%
surveys = skyra.find_surveys(token=token)
# %%
surveys.json()
# %%
survey_names = []
survey_ids = []
survey_slugs = []
for i in surveys.json()["data"]["items"]:
    survey_names.append(i["name"])
    survey_ids.append(i["id"])
    survey_slugs.append(i["slug"])
# %%
with open("data/surveys.json", "w") as f:
    json.dump(surveys.json(), f, ensure_ascii=False)
# %%
# Download survey as json
data = skyra.download_survey(
    survey_id=survey_ids[0],
    filename_path="data/test_survey.json",
    token=token,
    format="json",
)
# %%
# Download survey as csv
data = skyra.download_survey(
    survey_id=survey_ids[0],
    filename_path="data/test_survey.csv",
    token=token,
    format="csv",
)

# %%
# Download survey responses for date range
# Set date, time and timezone for Oslo
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
# %%
data.status_code
# %%
