# Pixel Forge Backend

FastAPI backend for Pixel Forge.

It supports two independent 3D paths:

1. **Pixel Forge local engine** — deterministic JPG/PNG/WebP → relief/lithophane → STL/GLB.
2. **AI 3D mode** — image analysis with OpenAI or Gemini → public reference images through Cloudinary → three.ws image-to-3D → textured GLB.

The local engine does not require an AI API key.

## Architecture

```text
Frontend
   |
   +--> /api/v1/analysis/image
   |       +--> OpenAI vision (preferred when configured)
   |       +--> Gemini fallback
   |       +--> local prompt fallback
   |
   +--> /api/v1/convert/local
   |       +--> grayscale / smoothing
   |       +--> physical height map
   |       +--> closed mesh
   |       +--> STL / GLB
   |
   +--> /api/v1/ai3d/generate
           +--> vision prompt builder
           +--> Cloudinary public image URLs
           +--> three.ws reconstruction
           +--> /api/v1/jobs/{id}
```

## Run locally

Use Python 3.11+.

```bash
cd backend
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## Environment variables

The backend works with no external AI keys for relief/lithophane conversion.

For AI features configure any of:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.6-luna

GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash-lite

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Cloudinary is required for the current three.ws route because the reconstruction provider consumes public image URLs.

Never commit a populated `.env` file.

## Endpoints

### Health

```http
GET /health
GET /providers
```

### Analyze an image

```http
POST /api/v1/analysis/image
```

Multipart fields:

- `file`
- `provider`: `auto | openai | gemini | local`
- `description`: optional user guidance

Example:

```bash
curl -X POST http://localhost:8000/api/v1/analysis/image \
  -F "file=@shoe.jpg" \
  -F "provider=auto" \
  -F "description=running shoe"
```

### Local image → STL/GLB

```http
POST /api/v1/convert/local
```

Useful fields:

- `mode=relief|lithophane`
- `output_format=stl|glb`
- `width_mm=100`
- `depth_mm=8`
- `base_thickness_mm=1.5`
- `max_thickness_mm=4`
- `resolution=128`
- `smoothing=15`
- `invert=false`

Example:

```bash
curl -X POST http://localhost:8000/api/v1/convert/local \
  -F "file=@logo.png" \
  -F "mode=relief" \
  -F "output_format=stl" \
  -F "width_mm=100" \
  -F "depth_mm=8" \
  -F "resolution=128"
```

The response includes a URL under `/files/...`.

### Full AI image → 3D

```http
POST /api/v1/ai3d/generate
```

Upload 1–6 views.

```bash
curl -X POST http://localhost:8000/api/v1/ai3d/generate \
  -F "files=@front.jpg" \
  -F "files=@side.jpg" \
  -F "vision_provider=auto" \
  -F "description=preserve the exact shoe proportions" \
  -F "tier=draft"
```

The response returns a Pixel Forge job ID. Poll:

```http
GET /api/v1/jobs/{job_id}
```

When complete, the response contains `glb_url` and `viewer_url`.

## Vision behavior

When `vision_provider=auto`:

1. OpenAI is attempted if `OPENAI_API_KEY` exists.
2. Gemini is used if OpenAI is unavailable/fails and Gemini is configured.
3. A deterministic local prompt builder is used if neither provider is configured.

The OpenAI implementation uses image input plus Pydantic-backed Structured Outputs so the downstream 3D provider receives predictable geometry-oriented fields instead of loose prose.

## Local conversion limitations

The local engine creates **2.5D** geometry. It is appropriate for:

- lithophanes
- embossed/engraved images
- logos
- reliefs
- height-map-like objects

It does not infer the unseen back side of a photographed real object. Use AI 3D mode for that.

## Tests

From `backend/`:

```bash
pytest -q
```

## Render

Create a Python Web Service with:

**Root directory**

```text
backend
```

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set:

```env
PUBLIC_BASE_URL=https://YOUR-BACKEND.onrender.com
CORS_ORIGINS=https://forge-pixel-forge.onrender.com
```

Then add API keys as Render environment variables rather than putting them in GitHub.

## Production notes

The current job store is deliberately in-memory for hackathon speed. For production, replace it with Redis or Postgres. Generated local files are also stored on the service filesystem; use object storage for durable production downloads.
