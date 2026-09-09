import json, math, pathlib, time, urllib.request

def validate(data, now):
    stamp=data.get('generatedAt')
    if data.get('schema')!=1 or isinstance(stamp,bool) or not isinstance(stamp,(int,float)) or not math.isfinite(stamp):
        raise ValueError('Invalid schedule schema or timestamp')
    if not -300 <= now-stamp <= 900:
        raise ValueError('Upstream schedule is stale or from the future')
    events=data.get('events')
    if not isinstance(events,list) or len(events)>1000:
        raise ValueError('Invalid events')
    for e in events:
        if not isinstance(e,dict):raise ValueError('Invalid event')
        start,end=e.get('start'),e.get('end')
        if any(isinstance(n,bool) or not isinstance(n,(int,float)) or not math.isfinite(n) for n in (start,end)) or end<=start:
            raise ValueError('Invalid interval')
        if type(e.get('artistIndex')) is not int or not 0<=e['artistIndex']<=6:
            raise ValueError('Unmapped artist')
        if not all(isinstance(e.get(k),str) for k in ('id','title','artist','artistId')):
            raise ValueError('Missing event identity')
    return data

def main():
    now=time.time()
    url='https://entertune.net/assets/data/show-schedule.json?v='+str(int(now))
    req=urllib.request.Request(url,headers={'User-Agent':'Entertune-Public-Schedule-Mirror','Cache-Control':'no-cache'})
    with urllib.request.urlopen(req,timeout=30) as r:
        raw=r.read(1048577)
    if len(raw)>1048576:raise ValueError('Oversized feed')
    data=validate(json.loads(raw),now)
    out=pathlib.Path('public');out.mkdir(exist_ok=True)
    (out/'show-schedule.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (out/'.nojekyll').touch()
    (out/'index.html').write_text('<!doctype html><title>Entertune Park Schedule</title><a href="show-schedule.json">Public show schedule</a><p>Source: entertune.net</p>',encoding='utf-8')
    print('Validated public schedule:',len(data['events']),'events; original timestamp preserved')
if __name__=='__main__':main()
