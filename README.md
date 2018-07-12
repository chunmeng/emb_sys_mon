# emb_sys_mon

[![Build status](https://travis-ci.com/chunmeng/emb_sys_mon.svg?master)](https://travis-ci.com/chunmeng/emb_sys_mon)

## Brief
This project is created for very specific use case and not a general purpose library/application.
The main intent is monitor a target embedded system via serial command and
output the cpu and mem data for graphing.

It also contains some utils for data extraction from captured logs.

## Additional python package
sudo apt install python3-tk -y

## python modules
Required python module listed in module_required.txt
pip install -r module_required.txt
(sudo would be needed)

## TODO List:
- Auto save figure on close + periodic plot save (every 100 iterations?)
- Rework plotting
  - need to restructure the plotting area, i.e.
  - % plot in one figure
  - kb in one axis, num of objects (kmalloc) in another
- graph configuration
- debug configuration
  - output level
- Config file as Input arg
- event marking
  - Only for post plotting? (and offline record)
  - Using a fixed file with iter no, "Description of event"
  - Is it possible to use the plot interaction to create the event log?
    - i.e. click on the point when bring up a window to enter the event and the iteraction number is taken based on the point clicked
- Additional data flexibility
  - top -m for mem use per process
  - Setting to allow different top parsing
    - top -n 2 | grep CPU
    - top -n 2 -b