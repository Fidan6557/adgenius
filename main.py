import asyncio
import logging
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import AsyncOpenAI, OpenAIError
from pydantic import BaseModel, ConfigDict, Field

from prompts import (
    facebook_prompt,
    instagram_prompt,
    tiktok_prompt,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "templates" / "index.html"
MODEL = "gpt-4o"

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ad-generator")

app = FastAPI(
    title="AdGenius API",
    description="Generate platform-specific ad copy with OpenAI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class GenerateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    business_name: str = Field(min_length=1, max_length=120)
    product: str = Field(min_length=1, max_length=500)
    language: Literal["az", "en"] = "az"


class GenerateResponse(BaseModel):
    instagram: str
    facebook: str
    tiktok: str


def get_openai_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY is not configured.")
        raise HTTPException(
            status_code=500,
            detail="The AI service is not configured. Please contact the administrator.",
        )
    return AsyncOpenAI(api_key=api_key, timeout=45.0, max_retries=2)


async def generate_ad(
    client: AsyncOpenAI,
    system_prompt: str,
    user_prompt: str,
) -> str:
    completion = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
    )

    content = completion.choices[0].message.content
    if not content or not content.strip():
        raise RuntimeError("OpenAI returned an empty response.")
    return content.strip()


@app.get("/", response_class=FileResponse, include_in_schema=False)
async def serve_index() -> FileResponse:
    return FileResponse(INDEX_FILE)


@app.get("/health", include_in_schema=False)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_ads(payload: GenerateRequest) -> GenerateResponse:
    client = get_openai_client()

    instagram_system, instagram_user = instagram_prompt(
        payload.business_name, payload.product, payload.language
    )
    facebook_system, facebook_user = facebook_prompt(
        payload.business_name, payload.product, payload.language
    )
    tiktok_system, tiktok_user = tiktok_prompt(
        payload.business_name, payload.product, payload.language
    )

    try:
        instagram, facebook, tiktok = await asyncio.gather(
            generate_ad(client, instagram_system, instagram_user),
            generate_ad(client, facebook_system, facebook_user),
            generate_ad(client, tiktok_system, tiktok_user),
        )
    except (OpenAIError, RuntimeError) as exc:
        logger.exception("Ad generation failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="We couldn't generate your ads right now. Please try again shortly.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error during ad generation: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating your ads.",
        ) from exc
    finally:
        await client.close()

    return GenerateResponse(
        instagram=instagram,
        facebook=facebook,
        tiktok=tiktok,
    )
