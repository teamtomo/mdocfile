from os import PathLike

import pandas as pd

from .data_models import Mdoc


def read(filename: PathLike) -> pd.DataFrame:
    """Read an mdoc file as a pandas dataframe.

    Parameters
    ----------
    filename : PathLike
        SerialEM mdoc file to read

    Returns
    -------
    df : pd.DataFrame
        dataframe containing info from mdoc file
    """
    return Mdoc.from_file(filename).as_dataframe()
