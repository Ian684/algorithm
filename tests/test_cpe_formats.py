import unittest
from cpe_solutions import uva10003,uva10069,uva10304,uva10032,uva10271,uva10285,uva10261

class CPEFormats(unittest.TestCase):
    def test_official_samples(self):
        self.assertEqual(uva10003.solve('100\n3\n25 50 75\n10\n4\n4 5 7 8\n0\n'),'The minimum cutting is 200.\nThe minimum cutting is 22.')
        self.assertEqual(uva10069.solve('2\nbabgbag\nbag\nrabbbit\nrabbit\n'),'5\n3')
        self.assertEqual(uva10304.solve('1 5\n3 10 10 10\n3 5 10 20\n'),'0\n20\n20')
        self.assertEqual(uva10032.solve('1\n\n3\n100\n90\n200\n'),'190 200')
        lengths='1 8 10 16 19 22 27 33 36 40 47 52 56 61 63 71 72 75 81 81 84 88 96 98 103 110 113 118 124 128 129 134 134 139 148 157 157 160 162 164'
        self.assertEqual(uva10271.solve('1\n1 40\n'+lengths+'\n'),'23')
        text='2\nFeldberg 10 5\n56 14 51 58 88\n26 94 24 39 41\n24 16 8 51 51\n76 72 77 43 10\n38 50 59 84 81\n5 23 37 71 77\n96 10 93 53 82\n94 15 96 69 9\n74 0 62 38 96\n37 54 55 82 38\nSpiral 5 5\n1 2 3 4 5\n16 17 18 19 6\n15 24 25 20 7\n14 23 22 21 8\n13 12 11 10 9\n'
        self.assertEqual(uva10285.solve(text),'Feldberg: 7\nSpiral: 25')

    def test_ferry_custom_and_case_separator(self):
        output=uva10261.solve('2\n\n2\n100\n100\n100\n0\n\n1\n200\n0\n')
        first,second=output.split('\n\n')
        rows=first.splitlines();self.assertEqual(rows[0],'3')
        self.assertEqual(len(rows[1:]),3)
        self.assertTrue(all(side in ('port','starboard') for side in rows[1:]))
        self.assertEqual(second,'0')

if __name__=='__main__':unittest.main()
