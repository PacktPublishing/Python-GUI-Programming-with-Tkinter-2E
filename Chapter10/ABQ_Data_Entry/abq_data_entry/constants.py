"""Global constants and classes needed by other modules in ABQ Data Entry"""
from enum import Enum, auto

class FieldTypes(Enum):
  string = auto()
  string_list = auto()
  short_string_list = auto()
  iso_date_string = auto()
  long_string = auto()
  decimal = auto()
  integer = auto()
  boolean = auto()
