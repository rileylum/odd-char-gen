from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.pdf_handler import fill_pdf_form, list_form_fields

app = FastAPI(title="ODD Character Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "charactersheet_fillable.pdf"


@app.get("/")
def root():
    index_path = Path(__file__).parent.parent / "index.html"
    return FileResponse(index_path)


@app.get("/fields")
def get_fields():
    fields = list_form_fields(TEMPLATE_PATH)
    return {"fields": fields}


@app.post("/generate-pdf")
def generate_pdf(field_values: dict[str, str]):
    pdf_output = fill_pdf_form(TEMPLATE_PATH, field_values)

    return StreamingResponse(
        pdf_output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=character_sheet.pdf"
        }
    )
