from detoxify import Detoxify

DETOXIFY_MODEL = Detoxify('original')

def analyze(text):
  return DETOXIFY_MODEL.predict(text)
