from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.pdf_handler import fill_pdf_form, list_form_fields
from app.utils import generate_six_stats, random_choice, roll_dice
from app.csv_handler import select_random_row

app = FastAPI(title="ODD Character Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "charactersheet_fillable.pdf"
RUMOURS_PATH = Path(__file__).parent.parent / "data" / "rumours.csv"


@app.get("/")
def root():
    index_path = Path(__file__).parent.parent / "index.html"
    return FileResponse(index_path)


@app.get("/fields")
def get_fields():
    fields = list_form_fields(TEMPLATE_PATH)
    return {"fields": fields}


@app.post("/generate-pdf")
def generate_pdf(field_values: dict[str, str] = {}):
    stats = generate_six_stats()

    stat_mapping = {
        'STR': 'Strength',
        'DEX': 'Dexterity',
        'CON': 'Constitution',
        'INT': 'Intelligence',
        'WIS': 'Wisdom',
        'CHA': 'Charisma'
    }

    pdf_fields = {}
    for stat_abbrev, stat_data in stats.items():
        full_name = stat_mapping[stat_abbrev]
        pdf_fields[full_name] = str(stat_data['score'])
        pdf_fields[f"{full_name}Mod"] = str(stat_data['modifier'])

    character_class = random_choice(['Fighter', 'Magic User', 'Thief'])

    con_modifier = stats['CON']['modifier']

    if character_class == 'Fighter':
        hd = 2
        save = 14
        first_roll = max(4, sum(roll_dice(1, 6))) + con_modifier
        second_roll = sum(roll_dice(2, 6)) + (con_modifier * 2)
        if second_roll > first_roll:
            hp = second_roll
        else:
            hp = first_roll + 1
    elif character_class == 'Magic User':
        hd = 1
        save = 15
        hp = max(4, sum(roll_dice(1, 6))) + con_modifier
    else:
        hd = 1
        save = 13
        hp = max(4, sum(roll_dice(1, 6))) + con_modifier

    rumour_row = select_random_row(RUMOURS_PATH)
    rumour = rumour_row.get('rumour', '')

    pdf_fields['Level'] = '1'
    pdf_fields['XP'] = '0'
    pdf_fields['Class'] = character_class
    pdf_fields['HD'] = str(hd)
    pdf_fields['HP'] = str(hp)
    pdf_fields['Save'] = str(save)
    pdf_fields['Notes1'] = rumour
    pdf_fields['Attack1'] = ''
    pdf_fields['Defend'] = ''
    pdf_fields['Attack2'] = ''

    pdf_fields.update(field_values)

    pdf_output = fill_pdf_form(TEMPLATE_PATH, pdf_fields)

    return StreamingResponse(
        pdf_output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=character_sheet.pdf"
        }
    )
