import os


class Config(object):
    SECRET_KEY = "pedaling"

    DEBUG = True

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "app/uploads")
    FUELSTAT_ROOT = os.path.join(PROJECT_ROOT, "../")