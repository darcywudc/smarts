import numpy as np

class BoltPhysics:
    MATERIALS = {
        "Steel 8.8": {"E": 210000, "Yield": 640, "Tensile": 800, "Poisson": 0.3, "Color": "#C0C0C0"},
        "Steel 10.9": {"E": 210000, "Yield": 940, "Tensile": 1040, "Poisson": 0.3, "Color": "#505050"},
        "Stainless Steel 316": {"E": 193000, "Yield": 205, "Tensile": 515, "Poisson": 0.28, "Color": "#E0E0E0"},
        "Titanium Gr5": {"E": 113800, "Yield": 880, "Tensile": 950, "Poisson": 0.34, "Color": "#8a9597"},
        "Aluminum 6061-T6": {"E": 68900, "Yield": 276, "Tensile": 310, "Poisson": 0.33, "Color": "#dcdcdc"}
    }

    @staticmethod
    def calculate_stress(diameter, force):
        """
        Calculate nominal tensile stress.
        Force in Newtons, Diameter in mm.
        Result in MPa.
        """
        area = np.pi * (diameter / 2) ** 2
        if area == 0: return 0
        return force / area

    @staticmethod
    def calculate_deformation(length, stress, E):
        """
        Calculate axial deformation (Delta L).
        Length in mm, Stress in MPa, E in MPa.
        Result in mm.
        """
        if E == 0: return 0
        strain = stress / E
        return strain * length

    @staticmethod
    def simulate_stress_distribution(length, shank_len, nominal_stress):
        """
        Simulate a finite element stress distribution profile along the bolt axis.
        Returns arrays for positions (y) and stress values.
        """
        # Discretize the bolt into segments
        num_segments = 100
        y_positions = np.linspace(-length, 0, num_segments)
        stress_profile = []

        # Thread start (transition from shank to thread) is a stress concentration point
        thread_start = -shank_len

        for y in y_positions:
            if y > thread_start + 1:
                # Shank area: Nominal stress
                s = nominal_stress
            elif y > thread_start - 2:
                # Concentration zone
                # Stress Concentration Factor (Kt) approx 2.5 for threads
                factor = 2.5 * np.exp(-0.5 * ((y - thread_start)**2)) + 1.0
                s = nominal_stress * factor
            else:
                # Deep threads: Load dissipates
                dist = abs(y - thread_start)
                s = nominal_stress * (1.2 / (1 + 0.1 * dist))

            # Add some randomness/noise
            s += np.random.normal(0, nominal_stress * 0.02)
            stress_profile.append(s)

        return y_positions, np.array(stress_profile)
