"""Exercise a running local demo API without printing passwords or tokens."""
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1]/'.env',override=False)
base=os.environ.get('SMOKE_API_BASE','http://127.0.0.1:8000/api/')
password=os.environ.get('DEMO_PASSWORD')
if not password:
    raise SystemExit('Set DEMO_PASSWORD; run seed_demo before smoke checks.')
token=''
def call(path: str, data=None) -> dict:
    body=json.dumps(data).encode() if data is not None else None
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Token '+token
    with urlopen(Request(base+path,data=body,headers=headers),timeout=15) as response:
        return json.load(response)['data']
token=call('auth/login',{'mobile':'9000000000','password':password})['token']
assert call('farmers/me')['profile']['district']=='Lucknow'
assert len(call('farms'))>=1
answer=call('advisory/ask',{'question':'गेहूँ के पीले पत्ते में दवा कितनी दूँ?'})
assert answer['expert_required'] and answer['confidence']=='low'
assert call('feedback',{'message_id':answer['message_id'],'helpful':True})['saved']
assert len(call('weather')['forecast'])==5
prices=call('market-prices')
assert prices['is_sample'] and prices['live_status']=='Current market price data is unavailable.'
print('Smoke passed: auth, own profile/farms, cautious advice, feedback, weather, labeled sample prices.')
