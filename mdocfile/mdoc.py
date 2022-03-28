from typing import List

from pydantic import BaseModel
from .global_data import MdocGlobalData
from .section_data import MdocSectionData
from .utils import find_z_value_entries, find_title_entries


class Mdoc(BaseModel):
    titles: List[str]
    global_data: MdocGlobalData
    section_data: List[MdocSectionData]

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as file:
            lines = [line.strip() for line in file.readlines()]
        split_idxs = find_z_value_entries(lines)
        split_idxs.append(len(lines))

        header_lines = lines[0:split_idxs[0]]
        title_idxs = find_title_entries(header_lines)

        titles = [header_lines[idx] for idx in title_idxs]
        global_data = MdocGlobalData.from_lines(header_lines)
        section_data = [
            MdocSectionData.from_lines(lines[start_idx:end_idx])
            for start_idx, end_idx
            in zip(split_idxs, split_idxs[1:])
            ]
        return cls(titles=titles, global_data=global_data, section_data=section_data)

    def to_string(self):
        """
        Generate the string representation of the Mdoc data
        """
        return '\n\n'.join([
            self.global_data.to_string(),
            '\n\n'.join(self.titles),
            '\n\n'.join(section.to_string() for section in self.section_data),
        ])
