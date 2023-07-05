# Writing mdoc files

This page will explain how to write valid SerialEM mdoc files in Python 
using *mdocfile*.

## The problem with dataframes

*mdocfile* returns a single pandas dataframe when reading files. This tabular representation 
is convenient for data exploration and analysis. Some global data is replicated across 
all sections to enable returning this simple dataframe but this makes the dataframe a bad 
model for the contents of a file.

## Introduction to data models

The contents of a file are represented as a small set of 
[pydantic models](https://docs.pydantic.dev/latest/) internally. 
These are simple classes containing data that provide guarantees about the types of those 
data based on type hints.

- [Mdoc](https://github.com/teamtomo/mdocfile/blob/a7015de82fb511f4a76be6326b2b15c0ab27245c/mdocfile/data_models.py#L161-L164) - the whole file
- [MdocGlobalData](https://github.com/teamtomo/mdocfile/blob/a7015de82fb511f4a76be6326b2b15c0ab27245c/mdocfile/data_models.py#L8-L19) - global data applying to all sections
- [MdocSectionData](https://github.com/teamtomo/mdocfile/blob/a7015de82fb511f4a76be6326b2b15c0ab27245c/mdocfile/data_models.py#L55-L108) - data pertaining to each section

These models can be explicitly constructed and used to write an mdoc file.

## Writing an mdoc file

In this section, we will write a simple mdoc file with data for two sections.

The attribute names for each model reflect those found in the 
[SerialEM documentation](https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm).
The expected types can be seen by inspecting the model definitions in 
[data_models.py](https://github.com/teamtomo/mdocfile/blob/main/mdocfile/data_models.py).

```python
from pathlib import Path
from mdocfile.data_models import Mdoc, MdocGlobalData, MdocSectionData

# construct global data model
global_data = MdocGlobalData(
    DataMode=1,
    ImageSize=(3838, 3710),
    PixelSpacing=1.35,
    Voltage=300
)

# construct section data models
first_section = MdocSectionData(
    ZValue=0,
    TiltAngle=0,
    StagePosition=(0.25, -0.25),
    PriorRecordDose=0,
    ExposureDose=0.3,
    SubFramePath=Path('/images/first_image.tif'),
    DateTime='05-Nov-15  15:21:38',
    NumSubFrames=8,
)

second_section = MdocSectionData(
    ZValue=1,
    TiltAngle=3,
    StagePosition=(0.25, -0.25),
    PriorRecordDose=0.3,
    ExposureDose=0.3,
    SubFramePath=Path('/images/second_image.tif'),
    DateTime='05-Nov-15  15:22:38',
    NumSubFrames=8,
)

# construct mdoc model
mdoc = Mdoc(
    titles=[
        '[T = SerialEM: Digitized on EMBL Krios                       30-Nov-15  15:14:20    ]',
        '[T =     Tilt axis angle = 85.3, binning = 4  spot = 8  camera = 2]'
    ],
    global_data=global_data,
    section_data=[first_section, second_section]
)

# write out the file
with open('my_new_mdoc.mdoc', mode='w+') as file:
    file.write(mdoc.to_string())
```

The code above produces the following file:

```text
DataMode = 1
ImageSize = 3838 3710
PixelSpacing = 1.35
Voltage = 300.0

[T = SerialEM: Digitized on EMBL Krios                       30-Nov-15  15:14:20    ]

[T =     Tilt axis angle = 85.3, binning = 4  spot = 8  camera = 2]

[ZValue = 0]
TiltAngle = 0.0
StagePosition = 0.25 -0.25
ExposureDose = 0.3
PriorRecordDose = 0.0
SubFramePath = /images/first_image.tif
NumSubFrames = 8
DateTime = 05-Nov-15  15:21:38

[ZValue = 1]
TiltAngle = 3.0
StagePosition = 0.25 -0.25
ExposureDose = 0.3
PriorRecordDose = 0.3
SubFramePath = /images/second_image.tif
NumSubFrames = 8
DateTime = 05-Nov-15  15:22:38
```