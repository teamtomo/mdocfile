from os import PathLike

import pandas as pd

from .mdoc import Mdoc
from .utils import camel_to_snake as _camel_to_snake


def read(filename: PathLike, camel_to_snake: bool = True) -> pd.DataFrame:
    """Read an mdoc file as a pandas dataframe.

    Parameters
    ----------
    filename : PathLike
        SerialEM mdoc file to read
    camel_to_snake : bool
        flag to convert headings from SerialEM 'CamelCase' to 'snake_case'
    Returns
    -------
    df : pd.DataFrame
        dataframe containing info from mdoc file
    """
    mdoc = Mdoc.from_file(filename)
    global_data = mdoc.global_data.dict()
    section_data = {
        k: [section.dict()[k] for section in mdoc.section_data]
        for k
        in mdoc.section_data[0].dict().keys()
    }
    df = pd.DataFrame(data=section_data)

    # add duplicate copies of global data and mdoc file titles to each row of
    # the dataframe - wide format data is easier to analyse
    for k, v in global_data.items():
        df[k] = [v] * len(df)
    df['titles'] = [mdoc.titles] * len(df)
    df = df.dropna(axis='columns', how='all')

    if camel_to_snake is True:
        df.columns = [_camel_to_snake(h) for h in df.columns]
    return df
