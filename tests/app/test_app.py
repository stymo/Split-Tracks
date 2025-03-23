import unittest
import os
from datetime import datetime

from tests.config.definitions import ROOT_DIR
from app.app import App
from sdk.moveapps_io import MoveAppsIo
import pandas as pd
import movingpandas as mpd


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['APP_ARTIFACTS_DIR'] = os.path.join(ROOT_DIR, 'tests/resources/output')
        self.sut = App(moveapps_io=MoveAppsIo())

    def test_app_runs(self):
        # prepare
        data: mpd.TrajectoryCollection = pd.read_pickle(os.path.join(ROOT_DIR, 'tests/resources/app/input4_LatLon.pickle'))
        config: dict = {
            "gap-interval": "hours",
            "gap-amount": 24,
        }

        # execute
        self.sut.execute(data=data, config=config)

    def test_app_config(self):
        # prepare
        config = {
            "gap-interval": "hours",
            "gap-amount": 24,
        }

        # execute
        actual = config

        # verify
        self.assertEqual("hours", actual["gap-interval"])
        self.assertEqual(24, actual["gap-amount"])

    def test_year_present(self):
        # prepare input data
        df = pd.DataFrame([
            {'timestamp_utc': "2001-06-11 09:00:00", 'coords_x': 1, 'coords_y': 5, 'track_id': 'ID_1'},
            {'timestamp_utc': "2001-06-12 09:00:00", 'coords_x': 2, 'coords_y': 4, 'track_id': 'ID_1'},
            {'timestamp_utc': "2001-06-13 09:00:00", 'coords_x': 3, 'coords_y': 3, 'track_id': 'ID_1'},
            {'timestamp_utc': "2001-06-15 09:00:00", 'coords_x': 4, 'coords_y': 2, 'track_id': 'ID_1'},
            {'timestamp_utc': "2001-06-16 09:00:00", 'coords_x': 5, 'coords_y': 1, 'track_id': 'ID_1'},
        ])
        input = mpd.TrajectoryCollection(
            df,
            traj_id_col='track_id',
            t='timestamp_utc',
            crs='epsg:4326',
            x='coords_x', y='coords_y'
        )

        # prepare configuration
        config = {
            "gap-interval": "hours",
            "gap-amount": 24,
        }

        # execute
        actual = self.sut.execute(data=input, config=config)

        self.assertEqual(len(actual.trajectories), 2)
        self.assertEqual(actual.trajectories[0].get_start_time(), datetime(2001,6,11,9))
        self.assertEqual(actual.trajectories[0].get_end_time(), datetime(2001,6,13,9))
        self.assertEqual(actual.trajectories[1].get_start_time(), datetime(2001,6,15,9))
        self.assertEqual(actual.trajectories[1].get_end_time(), datetime(2001,6,16,9))
