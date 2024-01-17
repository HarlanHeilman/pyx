import json
from datetime import datetime
from pathlib import Path
from random import choices

import art
import typer
from astropy.io import fits
from pandas import DataFrame
from rich import print
from typing_extensions import Annotated

app = typer.Typer(rich_markup_mode="markdown", pretty_exceptions_enable=True)

db_json = __file__.replace("liquid.py", r"db\db.json")
db = Path(json.load(open(db_json))["path"])


def get_from_list() -> str:  # type: ignore
    beamtimes = [x.name for x in db.iterdir() if x.is_dir()][::-1]
    for i, beamtime in enumerate(beamtimes):
        print(f"[{i}] {beamtime}")
        if i > 0 and i % 10 == 0:
            choice = typer.prompt(
                "Enter the beamtime you wish to select (or leave blank to see more)",
                default="",
            )
            if choice == "":
                continue
            elif isinstance(choice, int) and choice < len(beamtimes[0:i]):
                return beamtimes[int(choice)]
            else:
                return choices(beamtimes)[0]


@app.command()
def report(
    beamtime: Annotated[
        str,
        typer.Option(
            "--beamtime",
            "-bt",
            help="Beamtime to select",
            show_default=True,
            rich_help_panel="Beamtime Settings",
        ),
    ] = datetime.now().strftime("%b%y"),
    day: Annotated[
        str,
        typer.Option(
            "--day",
            "-d",
            help="Day of beamtime",
            show_default=True,
            rich_help_panel="Beamtime Settings",
        ),
    ] = "all",
):
    """
    :calendar: **Report** - Shows a report on the selected beamtime. If the beamtime is left empty, it will default to the current beamtime.

    ---

    Each beamtime has a folder associated to it, with data collected for liquid experiments stoed within that folder.

    In general, the data is stored under the following structure

    * Beamtime -> Liquid -> Day Month -> CCD -> Data
    """

    if beamtime == "?":
        beamtime = get_from_list()

    liquid_data = db / beamtime / "Liquid"


if __name__ == "__main__":
    app()
