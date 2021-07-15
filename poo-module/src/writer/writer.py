from genericpath import exists
import os
import json
from typing import Union


class DataTypeNotSupported(Exception):
    pass


class DataWriter:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, "a+") as f:
            f.write(row + "\n")

    def write(self, data: Union[list, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data))
        elif isinstance(data, list):
            for n in data:
                self.write(n)
        else:
            raise DataTypeNotSupported(f"Type of data {type(data)} not supported")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        return True


if __name__ == "__main__":
    with DataWriter("this.json") as dw:
        dw.write({"a": "b"})
