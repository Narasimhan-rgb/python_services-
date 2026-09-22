import unittest
from app.services.paper_analysis import analyze_csv

HEADER='Benchmark,Mode,Score,Unit,Param: size,Param: seed,Param: distribution\n'
def run(rows): return analyze_csv((HEADER+rows).encode())

class PaperAnalysisTests(unittest.TestCase):
    def test_complete_and_mean(self):
        result=run('sort, avgt,2,ms/op,10,1,random\n'.replace(', avgt',',avgt')+'sort,avgt,4,ms/op,10,2,random\n')
        self.assertEqual(result['summary'][0]['mean'],3)
        self.assertTrue(result['observed_matrix_complete'])
        self.assertFalse(result['matches_planned_dimensions'])
    def test_missing_cells(self):
        result=run('a,avgt,1,ms/op,10,1,random\na,avgt,1,ms/op,10,2,random\nb,avgt,1,ms/op,10,1,random\n')
        self.assertEqual(result['missing_observed_matrix_rows'],1)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):run('a,avgt,1,ms/op,10,1,r\n'*2)
    def test_mixed_units_rejected(self):
        with self.assertRaises(ValueError):run('a,avgt,1,ms/op,10,1,r\nb,avgt,1,ns/op,10,1,r\n')
    def test_nonfinite_rejected(self):
        with self.assertRaises(ValueError):run('a,avgt,nan,ms/op,10,1,r\n')
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):run('')

if __name__=='__main__': unittest.main()
