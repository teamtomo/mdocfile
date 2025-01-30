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
    return Mdoc.from_file(filename).to_dataframe()

def write(df: pd.DataFrame, filename: PathLike):
    """Write a pandas dataframe to an mdoc file. 
    Note this only works for tilt series mdoc files, not montages or frame sets.

    Parameters
    ----------
    df : pd.DataFrame
        dataframe containing info from mdoc file
    filename : PathLike
        path of file to be written
    """
    mdoc = Mdoc.from_dataframe(df)
    with open(filename, 'w') as file:
        file.write(mdoc.to_string())
