from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta

app = FastAPI(title="SimpleTimeService")  # initialize FastAPI application


@app.get("/")
async def root(request: Request):
    forwarded_ip = request.headers.get("x-forwarded-for")  # get original client IP from proxy/LB

    if forwarded_ip:
        client_ip = forwarded_ip.split(",")[0].strip()  # take first IP (actual client)
    else:
        client_ip = request.client.host if request.client else "unknown"  # fallback to direct client IP

    
    utc_time = datetime.now(timezone.utc)# get current time in UTC

    
    ist_time = utc_time + timedelta(hours=5, minutes=30) # convert UTC to IST (UTC + 5:30)

    return JSONResponse(  # return JSON response with IST timestamp and client IP
        {
            "timestamp": ist_time.isoformat(),
            "ip": client_ip,
        }
    )
