from pyemotiv import Epoc

epoc = Epoc()
while True:
    # get only the most recent values for the gyro sensors and the latest time
    # stamp
    g_y, g_x, t= epoc.get_next(single=['ED_GYROY','ED_GYROX','ED_TIMESTAMP'])
    print g_y, g_x, t