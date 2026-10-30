# %%
import logging

import requests
from tqdm.auto import tqdm

logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# %%
def find_surveys(token: str):
    """
    Find survey for token
    """
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.get("https://api.skyra.no/beta/surveys", headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    return response


# %%
def download_survey(
    survey_id: str,
    filename_path: str,
    token: str,
    start_date: str | None = None,
    end_date: str | None = None,
    format: str = "json",
    proxy: str = "",
):
    """
    Download specific survey by ID using token
    """
    session = requests.Session()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    params = {
        "format": format,
    }
    if start_date is not None:
        params["startDate"] = start_date
    if end_date is not None:
        params["endDate"] = end_date
    try:
        response = session.get(
            f"https://api.skyra.no/beta/surveys/{survey_id}/export",
            timeout=120,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    if response.status_code == 200:
        with tqdm.wrapattr(
            open(filename_path, "wb"),
            "write",
            miniters=1,
            total=int(response.headers.get("content-length", 0)),
            desc=filename_path,
        ) as fout:
            for chunk in response.iter_content(chunk_size=8192):
                fout.write(chunk)

        logging.info("Downloaded survey %s", survey_id)

    return response
