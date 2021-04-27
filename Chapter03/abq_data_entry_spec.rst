======================================
 ABQ Data Entry Program specification
======================================

Description
-----------
This program facilitates entry of laboratory observations
into a CSV file.

Functionality Required
----------------------

The program must:

  * allow all relevant, valid data to be entered,
    as per the data dictionary
  * append entered data to a CSV file:
    - The CSV file must have a filename of
    abq_data_record_CURRENTDATE.csv, where CURRENTDATE is the date
    of the laboratory observations in ISO format (Year-month-day)
    - The CSV file must include all fields
    listed in the data dictionary
    - The CSV headers will avoid cryptic abbreviations
  * enforce correct datatypes per field

The program should try, whenever possible, to:

  * enforce reasonable limits on data entered, per the data dict
  * Auto-fill data to save time
  * Suggest likely correct values
  * Provide a smooth and efficient workflow
  * Store data in a format easily understandable by Python

Functionality Not Required
--------------------------

The program does not need to:

  * Allow editing of data.
  * Allow deletion of data.

Users can perform both actions in LibreOffice if needed.


Limitations
-----------

The program must:

  * Be efficiently operable by keyboard-only users.
  * Be accessible to color blind users.
  * Run on Debian GNU/Linux.
  * Run acceptably on a low-end PC.

Data Dictionary
---------------
+------------+--------+----+---------------+--------------------+
|Field       | Type   |Unit| Valid Values  |Description         |
+============+========+====+===============+====================+
|Date        |Date    |    |               |Date of record      |
+------------+--------+----+---------------+--------------------+
|Time        |Time    |    |8:00, 12:00,   |Time period         |
|            |        |    |16:00, or 20:00|                    |
+------------+--------+----+---------------+--------------------+
|Lab         |String  |    | A - C         |Lab ID              |
+------------+--------+----+---------------+--------------------+
|Technician  |String  |    |               |Technician name     |
+------------+--------+----+---------------+--------------------+
|Plot        |Int     |    | 1 - 20        |Plot ID             |
+------------+--------+----+---------------+--------------------+
|Seed        |String  |    | 6-character   |Seed sample ID      |
|sample      |        |    | string        |                    |
+------------+--------+----+---------------+--------------------+
|Fault       |Bool    |    | True, False   |Environmental       |
|            |        |    |               |Sensor Fault        |
+------------+--------+----+---------------+--------------------+
|Light       |Decimal |klx | 0 - 100       |Light at plot.      |
|            |        |    |               |blank on fault.     |
+------------+--------+----+---------------+--------------------+
|Humidity    |Decimal |g/m³| 0.5 - 52.0    |Abs humidity at plot|
|            |        |    |               |blank on fault.     |
+------------+--------+----+---------------+--------------------+
|Temperature |Decimal |°C  | 4 - 40        |Temperature at plot |
|            |        |    |               |blank on fault.     |
+------------+--------+----+---------------+--------------------+
|Blossoms    |Int     |    | 0 - 1000      |No. blossoms in plot|
+------------+--------+----+---------------+--------------------+
|Fruit       |Int     |    | 0 - 1000      |No. fruits in plot  |
+------------+--------+----+---------------+--------------------+
|Plants      |Int     |    | 0 - 20        |No. plants in plot  |
+------------+--------+----+---------------+--------------------+
|Max height  |Decimal |cm  | 0 - 1000      |Height of tallest   |
|            |        |    |               |plant in plot       |
+------------+--------+----+---------------+--------------------+
|Min height  |Decimal |cm  | 0 - 1000      |Height of shortest  |
|            |        |    |               |plant in plot       |
+------------+--------+----+---------------+--------------------+
|Median      |Decimal |cm  | 0 - 1000      |Median height of    |
|height      |        |    |               |plants in plot      |
+------------+--------+----+---------------+--------------------+
|Notes       |String  |    |               |Miscellaneous notes |
+------------+--------+----+---------------+--------------------+
