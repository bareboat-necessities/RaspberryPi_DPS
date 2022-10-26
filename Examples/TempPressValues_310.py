import DPS

from time import sleep


dps310 = DPS.DPS()

# P_b = static pressure (pressure at sea level) [Pa]
# T_b = standard temperature (temperature at sea level) [K]
# L_b = standard temperature lapse rate [K/m] = -0.0065 [K/m]
# h   = height about sea level [m]
# h_b = height at the bottom of atmospheric layer [m]
# R   = universal gas constant = 8.31432 [N*m/(mol*K)]
# g_0 = gravitational acceleration constant = 9.80665 (m/s2)
# M   = molar mass of Earth’s air = 0.0289644 [kg/mol]
#
# h = h_b + ( (T_b/L_b) * (power(P/P_b, -R*L_b/(g_0*M)) - 1) )
#
# F = -R*L_b/(g_0*M)
#
# delta_h = (T_b/L_b) (power(P1/P_b, F) - power(P2/P_b, F))

L_b = -0.0065
R = 8.31432
g_0 = 9.80665
M = 0.0289644
F = -R*L_b/(g_0*M)


def delta_h(T_b: float, L_b: float, P_b: float, P1: float, P2: float):
    return (T_b/L_b) * (pow(P1/P_b, F) - pow(P2/P_b, F))


try:

        while True:

            scaled_p = dps310.calcScaledPressure()

            scaled_t = dps310.calcScaledTemperature()

            p = dps310.calcCompPressure(scaled_p, scaled_t)

            t = dps310.calcCompTemperature(scaled_t)

            print(f'{p:8.1f} Pa {t:4.1f} C')

            sleep(0.1)

except KeyboardInterrupt:

        pass
