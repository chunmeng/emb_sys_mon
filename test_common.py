import unittest

from common import parse_version
from common import parse_top

class TestCommon(unittest.TestCase):

    def test_parse_version(self):
        self.assertEqual(parse_version(""), '') # empty
        self.assertEqual(parse_version("ver 1.01.1.1"), '1.01.1.1')
        self.assertEqual(parse_version("version=0.1.1.0-build5"), '0.1.1.0-build5')
        self.assertEqual(parse_version("version=7.1.1.0test111"), '7.1.1.0test111')
        self.assertEqual(parse_version("[[[version 1.3.3-rc1\n\n\n"), '1.3.3-rc1')
        self.assertEqual(parse_version("[[[version 1.3.3-rc1_1.0.1+ Something else\n\n\n"), '1.3.3-rc1_1.0.1+') # Special case
        self.assertEqual(parse_version("This is awesome version string 1.3.3-rc1_1.0-1_xx?x* \f\fr"), '1.3.3-rc1_1.0-1_xx?x*') # Special case
        self.assertEqual(parse_version("[[[Some garbage4.1.3.3-rc1_debug_this_and_that Something else\n\n\n"), '4.1.3.3-rc1_debug_this_and_that')

    def test_parse_top_bad(self):
        test_contents = [ '',
                      'Where are my cpu line\nI can\'t see a thing.\n', # No target string
                      'Are you nuts?\nCPU: Here is your data\n',
                      'CPU: % idle % sirq\n',
                      'CPU: nic % idle irq % sirq\n']
        for content in test_contents:
            v,_,_ = parse_top(content)
            self.assertFalse(v)

    def test_parse_top_grep(self):
        test_content = '''
top -n 2 | grep CPU
CPU:  0.0% usr  3.5% sys  0.0% nic 89.2% idle  0.0% io  0.0% irq  7.1% sirq
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
12670 12646 root     S     2340  1.1   1  3.5 grep CPU
CPU:  0.0% usr  1.3% sys  0.0% nic 95.7% idle  0.0% io  0.0% irq  2.8% sirq
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND'''

        v,i,s = parse_top(test_content)
        self.assertTrue(v)
        self.assertEqual(i, 95.7)
        self.assertEqual(s, 2.8)

    def test_parse_top_grep_timeout(self):
        # Timeout case - take the 1st line available
        test_content = '''
top -n 2 | grep CPU
CPU:  8.3% usr 25.0% sys  0.0% nic 62.5% idle  0.0% io  0.0% irq  4.1% sirq
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND'''

        v,i,s = parse_top(test_content)
        self.assertTrue(v)
        self.assertEqual(i, 62.5)
        self.assertEqual(s, 4.1)

    def test_parse_top_batch(self):
        test_content = '''
top -n 2 -b
Mem: 125224K used, 85544K free, 532K shrd, 48K buff, 33088K cached
CPU:  0.0% usr  0.0% sys  0.0% nic  100% idle  0.0% io  0.0% irq  0.0% sirq
Load average: 0.37 0.41 0.47 2/88 12921
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
12921 12646 root     R     2336  1.1   0  0.0 top -n 2 -b
  905   767 root     S <   3284  1.5   0  0.0 /sbin/ulogd
12646 12640 root     S     2748  1.3   0  0.0 -sh
 1805   767 root     S     2348  1.1   1  0.0 /bin/sh -i
  776    97 root     S <   1928  0.9   0  0.0 /sbin/udevd --daemon
    3     2 root     SW       0  0.0   0  0.0 [ksoftirqd/0]
    9     2 root     SW       0  0.0   1  0.0 [ksoftirqd/1]
   42     2 root     SW       0  0.0   1  0.0 [scsi_eh_0]
   52     2 root     SW       0  0.0   1  0.0 [kworker/u:2]
12719     2 root     SW       0  0.0   1  0.0 [flush-ubifs_0_3]
Mem: 125268K used, 85500K free, 532K shrd, 48K buff, 33088K cached
CPU:  0.0% usr  0.5% sys  0.0% nic 95.1% idle  0.0% io  0.0% irq  4.1% sirq
Load average: 0.34 0.41 0.47 3/88 12925
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
    3     2 root     SW       0  0.0   0  0.1 [ksoftirqd/0]
12921 12646 root     R     2748  1.3   0  0.1 top -n 2 -b
 1802   767 root     S     2348  1.1   1  0.1 /bin/sh -i
  905   767 root     S <   3284  1.5   0  0.0 /sbin/ulogd
  130    97 root     S <   1928  0.9   0  0.0 /sbin/udevd --daemon
  776    97 root     S <   1928  0.9   0  0.0 /sbin/udevd --daemon
    9     2 root     SW       0  0.0   1  0.0 [ksoftirqd/1]
   53     2 root     SW       0  0.0   1  0.0 [kworker/1:2]
   10     2 root     SW<      0  0.0   1  0.0 [cpuset]
   11     2 root     SW<      0  0.0   1  0.0 [khelper]
   12     2 root     SW       0  0.0   1  0.0 [kdevtmpfs]
12719     2 root     SW       0  0.0   1  0.0 [flush-ubifs_0_3]'''

        v,i,s = parse_top(test_content)
        self.assertTrue(v)
        self.assertEqual(i,95.1)
        self.assertEqual(s, 4.1)

if __name__ == '__main__':
    unittest.main()