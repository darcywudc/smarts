import unittest
from physics import BoltPhysics

class TestPhysics(unittest.TestCase):
    def test_stress_calculation(self):
        # 1000N on 20mm diameter
        # Area = pi * 10^2 = 314.159
        # Stress = 1000 / 314.159 = 3.18 MPa
        stress = BoltPhysics.calculate_stress(20, 1000)
        self.assertAlmostEqual(stress, 3.183, places=2)

    def test_deformation(self):
        # Length 100mm, Stress 210 MPa, E 210000 MPa
        # Strain = 0.001
        # Deformation = 0.1 mm
        defm = BoltPhysics.calculate_deformation(100, 210, 210000)
        self.assertAlmostEqual(defm, 0.1, places=2)

if __name__ == '__main__':
    unittest.main()
