import json
class MyEncoder(json.JSONEncoder):
  def default(self, obj):
    return json.JSONEncoder.default(self, obj)