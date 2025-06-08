import os


MLMODEL_URI = os.getenv("MLMODEL_URI")
MLMODELS_DIR = os.getenv("MLMODELS_DIR")

assert MLMODEL_URI, "MLMODEL_URI is not set"
assert MLMODELS_DIR, "MLMODELS_DIR is not set"
