from datetime import timedelta

from sdk.moveapps_spec import hook_impl
from sdk.moveapps_io import MoveAppsIo
from movingpandas import TrajectoryCollection, ObservationGapSplitter
import logging
import matplotlib.pyplot as plt

# showcase for importing functions from another .py file (in this case from "./app/getGeoDataFrame.py")
from app.getGeoDataFrame import get_GDF


class App(object):

    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:

        logging.info(f'Welcome to the {config}')

        gap_params = {config['gap-interval']: config['gap-amount']}
        result = ObservationGapSplitter(data).split(gap=timedelta(**gap_params))

        # return the resulting data for next Apps in the Workflow
        return result
