from fastapi import FastAPI, HTTPException, status

from src.redis_client import redis_client
from src.schemas import PhoneAddressResponse, PhoneAddressCreate, PhoneAddressUpdate

app = FastAPI(title="Phone-Address Service", version="1.0")


@app.get("/address/{phone}", response_model=PhoneAddressResponse)
async def get_address(phone: str):
    address = await redis_client.get(phone)

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found")

    return PhoneAddressResponse(phone=phone, address=address)


@app.post("/address", response_model=PhoneAddressResponse, status_code=status.HTTP_201_CREATED)
async def create_phone_address(data: PhoneAddressCreate):
    exists = await redis_client.exists(data.phone)

    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone already exists")

    await redis_client.set(data.phone, data.address)
    return {"phone": data.phone, "address": data.address}


@app.put("/address/{phone}", response_model=PhoneAddressResponse)
async def update_phone_address(phone: str, data: PhoneAddressUpdate):
    exists = await redis_client.exists(phone)

    if not exists:
        raise HTTPException(status_code=404, detail="Phone not found")

    await redis_client.set(phone, data.address)
    return {"phone": phone, "address": data.address}


@app.delete("/address/{phone}", status_code=204)
async def delete_phone_address(phone: str):
    deleted = await redis_client.delete(phone)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Phone not found")

    return
