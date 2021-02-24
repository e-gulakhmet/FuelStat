import os


class Config(object):
    SECRET_KEY = "pedaling"

    DEBUG = True

    PROJECT_FOLDER = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(PROJECT_FOLDER, "app/uploads/")
    FUELSTAT_FOLDER = os.path.join(PROJECT_FOLDER, "../")
    DATA_FOLDER = os.path.join(FUELSTAT_FOLDER, "data/")