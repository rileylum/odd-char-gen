from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import Optional

from app.pdf_handler import fill_pdf_form, list_form_fields
from app.utils import generate_six_stats, random_choice, roll_dice, calculate_modifier, generate_equipment
from app.csv_handler import select_random_row, select_random_rows

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
SPELLS_PATH = Path(__file__).parent.parent / "data" / "spells.csv"
ADVENTURING_GEAR_PATH = Path(__file__).parent.parent / "data" / "adventuring_gear.csv"


@app.get("/")
def root():
    index_path = Path(__file__).parent.parent / "index.html"
    return FileResponse(index_path)


@app.get("/fields")
def get_fields():
    fields = list_form_fields(TEMPLATE_PATH)
    return {"fields": fields}


@app.post("/generate-pdf")
def generate_pdf(
    stats: Optional[dict[str, int]] = Body(None),
    character_class: Optional[str] = Body(None, alias="class")
):
    if stats:
        stat_data = {}
        for stat_name, score in stats.items():
            stat_data[stat_name] = {
                'score': score,
                'modifier': calculate_modifier(score)
            }

        stat_name_map = {
            'Strength': 'STR',
            'Dexterity': 'DEX',
            'Constitution': 'CON',
            'Intelligence': 'INT',
            'Wisdom': 'WIS',
            'Charisma': 'CHA'
        }

        stats_internal = {}
        for full_name, abbrev in stat_name_map.items():
            if full_name in stat_data:
                stats_internal[abbrev] = stat_data[full_name]
    else:
        stats_internal = generate_six_stats()

    stat_mapping = {
        'STR': 'Strength',
        'DEX': 'Dexterity',
        'CON': 'Constitution',
        'INT': 'Intelligence',
        'WIS': 'Wisdom',
        'CHA': 'Charisma'
    }

    pdf_fields = {}
    for stat_abbrev, stat_info in stats_internal.items():
        full_name = stat_mapping[stat_abbrev]
        pdf_fields[full_name] = str(stat_info['score'])
        pdf_fields[f"{full_name}Mod"] = str(stat_info['modifier'])

    if not character_class:
        character_class = random_choice(['Fighter', 'Magic User', 'Thief'])

    con_modifier = stats_internal['CON']['modifier']

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

    equipment = generate_equipment(character_class)

    gear_items = []
    if equipment['armor']:
        gear_items.append(equipment['armor'])
    gear_items.append(equipment['weapon1'])
    if equipment['weapon2']:
        gear_items.append(equipment['weapon2'])

    gear_items.extend(['3 torches', 'waterskin', 'tinderbox'])

    gold = sum(roll_dice(3, 6))
    gear_items.append(f'{gold} gp')

    wis_modifier = stats_internal['WIS']['modifier']
    num_adventuring_items = max(0, 3 + wis_modifier)
    adventuring_gear_rows = select_random_rows(ADVENTURING_GEAR_PATH, num_adventuring_items)
    adventuring_gear = [row['item'] for row in adventuring_gear_rows]

    if character_class == 'Fighter':
        adventuring_gear.append('Potion of Healing')
    elif character_class == 'Magic User':
        scroll_spell = select_random_row(SPELLS_PATH)
        adventuring_gear.append(f"Spell Scroll ({scroll_spell['spell']})")
    elif character_class == 'Thief':
        extra_gear = select_random_row(ADVENTURING_GEAR_PATH)
        adventuring_gear.append(extra_gear['item'])

    pdf_fields['Level'] = '1'
    pdf_fields['XP'] = '0'
    pdf_fields['Class'] = character_class
    pdf_fields['HD'] = str(hd)
    pdf_fields['HP'] = str(hp)
    pdf_fields['Save'] = str(save)
    pdf_fields['Notes1'] = rumour
    pdf_fields['Attack1'] = equipment['attack1']
    pdf_fields['Defend'] = equipment['defend']
    pdf_fields['Attack2'] = equipment['attack2'] if equipment['attack2'] else ''
    pdf_fields['Gear1'] = ', '.join(gear_items)
    pdf_fields['Gear2'] = ', '.join(adventuring_gear)

    if character_class == 'Thief':
        pdf_fields['Abilties1'] = 'Thief skills: 2'
        pdf_fields['Abilities2'] = ''
    elif character_class == 'Magic User':
        int_score = stats_internal['INT']['score']
        spell_rows = select_random_rows(SPELLS_PATH, int_score - 1)
        spells = [row['spell'] for row in spell_rows]
        spells.append('Read Magic')
        spells.sort()
        pdf_fields['Abilties1'] = 'Known Spells: ' + ', '.join(spells[:8])
        pdf_fields['Abilities2'] = ', '.join(spells[8:]) if len(spells) > 8 else ''
    else:
        pdf_fields['Abilties1'] = ''
        pdf_fields['Abilities2'] = ''

    pdf_output = fill_pdf_form(TEMPLATE_PATH, pdf_fields)

    return StreamingResponse(
        pdf_output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=character_sheet.pdf"
        }
    )
