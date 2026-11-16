# %%
import logging

import requests
from tqdm.auto import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# %%
def find_surveys(token: str) -> requests.Response:
    """
    Find surveys for token

    Parameters
    ----------
    token: str, required
        A token from skyra, with scope to download one or more surveys

    Returns
    -------
    response: requests.Response
        A response object from requests module. Contains the surveys the token is scoped for.
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
) -> requests.Response:
    """
    Download specific survey by ID using token

    Parameters
    ----------
    survey_id: str, required
        The survey ID, which can be obtained from a skyra token
    filename_path: str, required
        Name and path to the survey results file you are downloading. F.ex "data/survey.csv" or "data/survey.json"
    token: str, required
        A token from skyra, with scope to download one or more surveys
    start_data: str or None, optional
        The start date to gather respones from. Use ISO 8601 with timezone F.ex 2026-01-05T00:00:00+01:00 for Oslo timezone
    end_date: str or None, optional
        The end date to gather respones from. Use ISO 8601 with timezone F.ex 2026-01-12T00:00:00+01:00 for Oslo timezone
    format: str, optional
        The file format for your download. Can be "csv" or "json". Default is "json"
    proxy: str, optional
        Allows setting a custom domain and endpoint for a proxy service if needed.

    Returns
    -------
    response: requests.Response
        A response object from requests module. Contains the survey questions and responses.
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

        logger.info("Downloaded survey %s", survey_id)

    return response
