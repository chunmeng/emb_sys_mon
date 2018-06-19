# emb_sys_mon
This project is created for very specific use case and not a general purpose library/application.
The main intent is monitor a target embedded system via serial command and
output the cpu and mem data for graphing.

It also contains some utils for data extraction from captured logs.

TODO List:
* Proper fw version parsing
* Auto save figure on close + periodic plot save (every 100 iterations?)
* slabinfo read and plotting
* graph configuration
* Input arg to run test or online mode
