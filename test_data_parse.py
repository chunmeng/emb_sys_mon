import unittest

from data_reader import DataReader

class TestDataParser(unittest.TestCase):
    def test_parse_meminfo(self):
        test_str = ("MemTotal:         210768 kB\n"
            "MemFree:          101408 kB\n"
            "MemAvailable:     128648 kB\n"
            "Buffers:              44 kB\n"
            "Cached:            31620 kB\n"
            "SwapCached:            0 kB\n"
            "Active:            56368 kB\n"
            "Inactive:          22592 kB\n"
            "Active(anon):      47524 kB\n"
            "Inactive(anon):      128 kB\n"
            "Active(file):       8844 kB\n"
            "Inactive(file):    22464 kB\n"
            "Unevictable:          64 kB\n"
            "Mlocked:              64 kB\n"
            "SwapTotal:             0 kB\n"
            "SwapFree:              0 kB\n"
            "Dirty:                 0 kB\n"
            "Writeback:             0 kB\n"
            "AnonPages:         47364 kB\n"
            "Mapped:            16608 kB\n"
            "Shmem:               356 kB\n"
            "Slab:              16144 kB\n"
            "SReclaimable:       2352 kB\n"
            "SUnreclaim:        13792 kB\n"
            "KernelStack:         704 kB\n"
            "PageTables:          932 kB\n"
            "NFS_Unstable:          0 kB\n"
            "Bounce:                0 kB\n"
            "WritebackTmp:          0 kB\n"
            "CommitLimit:      105384 kB\n"
            "Committed_AS:     129700 kB\n"
            "VmallocTotal:    1843200 kB\n"
            "VmallocUsed:      145072 kB\n"
            "VmallocChunk:    1405392 kB\n")

        dut = DataReader(None)
        exist,val = dut.parse_meminfo(test_str, tag='MemAvailable')
        self.assertEqual(exist, True)
        self.assertEqual(val, 128648)

        exist,val = dut.parse_meminfo(test_str, tag='will_not_found')
        self.assertEqual(exist, False)
        self.assertEqual(val, 0)

    def test_parse_slabinfo(self):
        test_str = ("Name                   Objects Objsize    Space Slabs/Part/Cpu  O/S O %Fr %Ef Flg\n"
            "kmalloc-1024               288    1024   294.9K          9/0/9   16 2   0 100 *\n"
            "kmalloc-128               2822     128   372.7K       64/11/27   32 0  12  96 *\n"
            "kmalloc-192               2163     192   425.9K        82/0/22   21 0   0  97 *\n"
            "kmalloc-2048              2241    2048     4.7M       138/45/7   16 3  31  96 *\n"
            "kmalloc-256               4921     256     1.3M       313/67/5   16 0  21  96 *\n"
            "kmalloc-4096               584    4096     2.3M         70/0/3    8 3   0 100 *\n"
            "kmalloc-512               2674     512     1.3M        163/6/7   16 1   3  98 *\n"
            "kmalloc-64               12904      64   843.7K      174/23/32   64 0  11  97 *\n"
            "kmalloc-8192                32    8192   262.1K          3/0/5    4 3   0 100 \n")

        dut = DataReader(None)
        exist,val = dut.parse_slabinfo(test_str, tag='kmalloc-1024')
        self.assertEqual(exist, True)
        self.assertEqual(val, 288)

        exist,val = dut.parse_slabinfo(test_str, tag='kmalloc-64')
        self.assertEqual(exist, True)
        self.assertEqual(val, 12904)

        exist,val = dut.parse_slabinfo(test_str, tag='will_not_found')
        self.assertEqual(exist, False)
        self.assertEqual(val, 0)

if __name__ == '__main__':
    unittest.main()