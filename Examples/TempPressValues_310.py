import DPS, sys

from time import sleep

dps310 = DPS.DPS()

# P_b = static pressure (pressure at sea level) [Pa]
# T_b = standard temperature (temperature at sea level) [K]
# L_b = standard temperature lapse rate [K/m] = -0.0065 [K/m]
# h   = height about sea level [m]
# h_b = height at the bottom of atmospheric layer [m]
# R   = universal gas constant = 8.3144598 [N*m/(mol*K)]
# g_0 = gravitational acceleration constant = 9.80665 (m/s2)
# M   = molar mass of Earth’s air = 0.0289644 [kg/mol]
#
# h = h_b + ( (T_b/L_b) * (power(P/P_b, -R*L_b/(g_0*M)) - 1) )
#
# F = -R*L_b/(g_0*M)
#
# delta_h = (T_b/L_b) (power(P1/P_b, F) - power(P2/P_b, F))

L_b = -0.0065
R = 8.3144598
g_0 = 9.80665
M = 0.0289644
K0 = 273.15
h_bias = 0.08
F = - (R * L_b) / (g_0 * M)

t0 = 0.1    # interval for sampling (sec)
t1 = 40.0   # interval for measuring wave height (sec)
count = round(t1 / t0)


def delta_h(T_b: float, L_b: float, P_b: float, P1: float, P2: float):
    return (T_b / L_b) * (pow(P1 / P_b, F) - pow(P2 / P_b, F))


try:

    idx = 0
    maxP = 0.0
    minP = sys.float_info.max
    maxT = 0.0
    minT = sys.float_info.max

    while True:

        scaled_p = dps310.calcScaledPressure()
        scaled_t = dps310.calcScaledTemperature()
        p = dps310.calcCompPressure(scaled_p, scaled_t)
        t = dps310.calcCompTemperature(scaled_t)

        print(f'{p:8.1f} Pa {t:4.1f} C')

        sleep(t0)

        if t > maxT: maxT = t
        if t < minT: minT = t
        if p > maxP: maxP = p
        if p < minP: minP = p

        idx += 1

        if idx >= count:
            T_b = K0 + ((maxT + minT) / 2)
            P_b = (maxP + minP) / 2
            d_h = delta_h(T_b, L_b, P_b, minP, maxP)
            if d_h > h_bias: d_h -= h_bias
            idx = 0
            maxP = 0.0
            minP = sys.float_info.max
            maxT = 0.0
            minT = sys.float_info.max
            h_d_ft = d_h * 3.28084
            print(f'Sea: {P_b:8.1f} Pa {T_b:4.1f} K')
            print(f'Wave height: {h_d_ft:4.2f} ft')

except KeyboardInterrupt:

    pass
