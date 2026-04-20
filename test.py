import urllib.request
import json
req = urllib.request.Request(
    'http://127.0.0.1:8000/analyze',
    data=json.dumps({'species': 'Allosaurus', 'growth_pct': 75, 'is_prime': False}).encode(),
    headers={'Content-Type': 'application/json'}
)
res = json.loads(urllib.request.urlopen(req).read().decode())
print(res['matchups'][0])