import act
import xarray as xr
import numpy as np
from datetime import datetime


def test_dates_between():
    start_date = '20190101'
    end_date = '20190110'

    date_list = act.utils.dates_between(start_date, end_date)
    answer = [datetime(2019, 1, 1),
              datetime(2019, 1, 2),
              datetime(2019, 1, 3),
              datetime(2019, 1, 4),
              datetime(2019, 1, 5),
              datetime(2019, 1, 6),
              datetime(2019, 1, 7),
              datetime(2019, 1, 8),
              datetime(2019, 1, 9),
              datetime(2019, 1, 10)]
    assert date_list == answer


def test_add_in_nan():
    # Make a 1D array with a 4 day gap in the data
    time_list = [np.datetime64(datetime(2019, 1, 1, 1, 0)),
                 np.datetime64(datetime(2019, 1, 1, 1, 1)),
                 np.datetime64(datetime(2019, 1, 1, 1, 2)),
                 np.datetime64(datetime(2019, 1, 1, 1, 8)),
                 np.datetime64(datetime(2019, 1, 1, 1, 9))]
    data = np.linspace(0., 8., 5)

    time_list = xr.DataArray(time_list)
    data = xr.DataArray(data)
    time_filled, data_filled = act.utils.add_in_nan(
        time_list, data)

    assert(data_filled.data[8] == 6.)

    time_answer = [np.datetime64(datetime(2019, 1, 1, 1, 0)),
                   np.datetime64(datetime(2019, 1, 1, 1, 1)),
                   np.datetime64(datetime(2019, 1, 1, 1, 2)),
                   np.datetime64(datetime(2019, 1, 1, 1, 3)),
                   np.datetime64(datetime(2019, 1, 1, 1, 4)),
                   np.datetime64(datetime(2019, 1, 1, 1, 5)),
                   np.datetime64(datetime(2019, 1, 1, 1, 6)),
                   np.datetime64(datetime(2019, 1, 1, 1, 7)),
                   np.datetime64(datetime(2019, 1, 1, 1, 8)),
                   np.datetime64(datetime(2019, 1, 1, 1, 9))]

    assert(time_filled[8].values == time_answer[8])
    assert(time_filled[5].values == time_answer[5])


def test_accum_precip():
    obj = act.io.armfiles.read_netcdf(
        act.tests.sample_files.EXAMPLE_MET_WILDCARD)

    obj = act.utils.data_utils.accumulate_precip(obj, 'tbrg_precip_total')

    dmax = round(np.nanmax(obj['tbrg_precip_total_accumulated']))

    assert dmax == 13.0


def test_calc_cog_sog():
    obj = act.io.armfiles.read_netcdf(
        act.tests.sample_files.EXAMPLE_NAV)

    obj = act.utils.ship_utils.calc_cog_sog(obj)

    cog = obj['course_over_ground'].values
    sog = obj['speed_over_ground'].values

    np.testing.assert_almost_equal(cog[10], 170.987, decimal=3)
    np.testing.assert_almost_equal(sog[15], 0.448, decimal=3)


def test_destination_azimuth_distance():
    lat = 37.1509
    lon = -98.362
    lat2, lon2 = act.utils.geo_utils.destination_azimuth_distance(lat, lon, 180., 100)

    np.testing.assert_almost_equal(lat2, 37.150, decimal=3)
    np.testing.assert_almost_equal(lon2, -98.361, decimal=3)
