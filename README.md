# emb_sys_mon
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
- slabinfo plotting
  - need to restructure the plotting area, i.e.
  - % plot in one figure
  - kb in one axis, num of objects (kmalloc) in another
- graph configuration
- debug configuration
  - logging console output to file (important for event tracing)
  - output level
- Config file as Input arg
