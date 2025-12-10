
from pydantic import BaseModel, Field


class PhoneAddressBase(BaseModel):
    phone: str = Field(..., min_length=3, max_length=15)
    address: str


class PhoneAddressResponse(PhoneAddressBase):
    pass


class PhoneAddressCreate(PhoneAddressBase):
    pass


class PhoneAddressUpdate(BaseModel):
    address: str