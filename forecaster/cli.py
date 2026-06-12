"""Pipeline orchestration: ingest -> ratings -> model -> picks -> form -> publish."""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys

import pandas as pd

from forecaster import config
from forecaster.form import summarise_all
from forecaster.ingest import (
    fetch_fixtures,
    fetch_historical_results,
    write_fixtures_parquet,
)
from forecaster.model import fit_params, predict_all
from forecaster.picks import enrich_predictions
from forecaster.publish import (
    write_html_dashboard,
    write_per_fixture_json,
    write_prompt_pack,
)
from forecaster.ratings import (
    init_elo,
    update_elo_from_results,
    write_elo_parquet,
)


def _has_match_in_next_24h(fixtures: list, now: dt.datetime) -> bool:
    return any(
        now <= f.utc_kickoff <= now + dt.timedelta(days=1)
        for f in fixtures
        if f.status == "SCHEDULED"
    )


def run_pipeline(force: bool = False) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    log = logging.getLogger("forecaster")

    config.ensure_dirs()

    log.info("ingest: fixtures")
    fixtures = fetch_fixtures()
    write_fixtures_parquet(fixtures)

    now = dt.datetime.now(dt.timezone.utc)
    is_match_day = _has_match_in_next_24h(fixtures, now)
    is_scheduled_full_run = now.hour in (6, 18)
    if not (is_match_day or is_scheduled_full_run or force):
        log.info("Quiet hour and no fixture in next 24h - exiting early.")
        return

    log.info("ingest: historical")
    history = fetch_historical_results()

    log.info("ratings")
    seed = init_elo()
    finished_rows = []
    for f in fixtures:
        if f.status == "FINISHED" and f.actual_home_goals is not None:
            finished_rows.append({
                "date": pd.Timestamp(f.utc_kickoff),
                "home": f.home, "away": f.away,
                "home_goals": f.actual_home_goals,
                "away_goals": f.actual_away_goals,
                "neutral": f.venue_country not in {f.home, f.away},
            })
    finished = pd.DataFrame(finished_rows)
    if len(finished):
        seed = update_elo_from_results(seed, finished, k=30.0)
    elo = update_elo_from_results(
        seed,
        pd.concat([history, finished], ignore_index=True) if len(finished) else history,
        k=15.0,
    )
    write_elo_parquet(elo)

    log.info("model: fit")
    params = fit_params(history, elo, ref_date=pd.Timestamp(now.date()))
    log.info("fitted params: %s", params)

    log.info("model: predict")
    predictions = predict_all(fixtures, elo, params)

    log.info("picks: EV optimisation")
    predictions = enrich_predictions(predictions)

    log.info("form summary")
    rationale = summarise_all(fixtures, predictions, elo, history)

    log.info("publish")
    write_per_fixture_json(fixtures, predictions, rationale)
    write_html_dashboard(fixtures, predictions, rationale)
    write_prompt_pack(fixtures, predictions, rationale)
    log.info("done; outputs in %s", config.DOCS_DIR)


def main() -> int:
    parser = argparse.ArgumentParser(prog="forecaster")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Run the full pipeline")
    run.add_argument("--force", action="store_true",
                     help="Run even on quiet hours of a non-match day")
    args = parser.parse_args()
    if args.cmd == "run":
        run_pipeline(force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
