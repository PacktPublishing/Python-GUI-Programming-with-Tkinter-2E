============================
 ABQ Data Entry Application
============================

Description
===========

This program provides entry, retrieval, and reporting on ABQ Agrilabs laboratory data.

Features
--------

* Enter data through validated form
* View historical data
* SQL Database storage
* Generate charts and plots
* Upload CSV extracts to corporate servers

Authors
=======

Alan D Moore, 2021

Requirements
============

One of the following operating systems:

* **Microsoft Windows**: 64-bit Windows 10 or higher
* **Apple macOS**: 64-bit High Sierra or higher
* **Linux**: x86_64 with kernel 4.4.0 or higher.  *Debian 10 or Ubuntu 20.04 (or newer) recommended.*

Installation
============

Windows
-------

Double-click the ``ABQ_Data_Entry-1.0-win64.msi`` file to launch the installation wizard.
Shortcuts will appear on your desktop and in the menu after the wizard completes.

macOS
-----

Double-click the ``ABQ_Data_Enter-1.0.dmg`` file to open it,
then drag the ``ABQ-Data-Entry`` application to your desktop or Applications folder.


Linux
-----
Extract ``abq_data_entry_1.0.tar.gz`` into a directory on your system.
``/opt/abq`` is recommended.  You can then execute the ``abq`` file from that directory.

You may wish to create a script in the ``/usr/local/bin/`` folder, like so::

  #!/bin/sh
  # /usr/local/bin/abq

  cd /opt/abq
  ./abq $@

This way you can launch abq from anywhere on the system by typing ``abq``.

Configuration
=============

Configuration for the application is stored in the ``abq_settings.json`` file
in a directory appropriate to your OS.  Refer to this table:

========== ==============================================
System     Directory
========== ==============================================
Linux, BSD ``$XDG_HOME/`` if defined, else ``~/.config/``
macOS      ``~/Library/Application Support/``
Windows    ``%HOME%\AppData\Local``
========== ==============================================

The configuration file should be used to set the host and port of the database server,
the connection properties for corporate REST and SFTP servers, and the call-sign for the
weather station nearest the facility.  Other configuration options can be configured
from within the application.

General Notes
=============

Please report all bugs to the data analysis department at the Bloomington, IN facility.
