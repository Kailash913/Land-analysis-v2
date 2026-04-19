"""
Admin Router — authentication and data management.
"""
import os
import csv
import io
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import bcrypt
from jose import jwt, JWTError
from database.models import AdminUser, LandRateDataset

router = APIRouter()
security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "lres-super-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))


class LoginRequest(BaseModel):
    username: str
    password: str


def _create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRY),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def _verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")


@router.post("/login")
async def admin_login(req: LoginRequest):
    """Admin authentication — returns JWT token."""
    user = await AdminUser.find_one(AdminUser.username == req.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(req.password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = _create_token(req.username)
    return {"token": token, "username": req.username, "expires_in": JWT_EXPIRY * 60}


@router.post("/upload-data")
async def upload_dataset(
    file: UploadFile = File(...),
    username: str = Depends(_verify_token),
):
    """
    Upload a CSV file containing land rate data.
    Expected columns: state, district, base_rate_per_acre, year, source
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    inserted = 0
    errors = []

    for i, row in enumerate(reader, start=2):
        try:
            record = LandRateDataset(
                state=row.get("state", "").strip(),
                district=row.get("district", "").strip(),
                base_rate_per_acre=float(row.get("base_rate_per_acre", 0)),
                year=int(row.get("year", 2024)),
                source=row.get("source", file.filename),
            )
            await record.insert()
            inserted += 1
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    return {
        "message": f"Uploaded {inserted} records from {file.filename}",
        "inserted": inserted,
        "errors": errors[:10],  # Show first 10 errors
        "uploaded_by": username,
    }


@router.get("/datasets")
async def list_datasets(username: str = Depends(_verify_token)):
    """List all uploaded dataset records."""
    records = await LandRateDataset.find_all().sort("-created_at").limit(100).to_list()
    return [
        {
            "id": str(r.id),
            "state": r.state,
            "district": r.district,
            "base_rate_per_acre": r.base_rate_per_acre,
            "year": r.year,
            "source": r.source,
        }
        for r in records
    ]
