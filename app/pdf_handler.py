from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter


def get_form_fields(pdf_path: str | Path) -> dict:
    reader = PdfReader(pdf_path)
    fields = {}
    if reader.get_fields():
        for field_name, field_data in reader.get_fields().items():
            fields[field_name] = field_data.get('/V', '')
    return fields


def fill_pdf_form(template_path: str | Path, field_values: dict[str, str]) -> BytesIO:
    reader = PdfReader(template_path)
    writer = PdfWriter()

    writer.append(reader)

    writer.update_page_form_field_values(
        writer.pages[0],
        field_values
    )

    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output


def list_form_fields(pdf_path: str | Path) -> list[str]:
    reader = PdfReader(pdf_path)
    if reader.get_fields():
        return list(reader.get_fields().keys())
    return []
