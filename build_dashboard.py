"""Generate an offline dashboard from the original Excel database (read only)."""
from pathlib import Path
import base64
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
import openpyxl

ROOT = Path(__file__).resolve().parent

def extract(path):
    book = openpyxl.load_workbook(path, data_only=True)
    records, incomplete = [], []
    clean = lambda v: re.sub(r'\s+', ' ', str(v)).strip() if v is not None else ''
    for sheet in book:
        section, current = '', None
        for rownum, values in enumerate(sheet.values, 1):
            row = list(values) + [None] * 8
            a, name = clean(row[0]), clean(row[1])
            if 'perkara' in name.lower():
                current = None
                continue
            if a and not name and not a.isdigit():
                section, current = a, None
                continue
            if a.isdigit() and not name:
                incomplete.append({'sheet': sheet.title, 'row': rownum, 'section': section})
                current = None
                continue
            if name:
                status = clean(row[6])
                lower = status.lower()
                condition = ('Rosak' if 'rosak' in lower else 'Penyelenggaraan' if 'penyelenggaraan' in lower or 'selenggara' in lower else 'Baik' if 'baik' in lower else 'Tidak dinyatakan')
                usage = 'Tidak digunakan' if 'tidak digunakan' in lower else 'Digunakan / diduduki' if 'digunakan' in lower or 'diduduki' in lower else 'Tidak dinyatakan'
                current = dict(id=f'{sheet.title}:{rownum}', name=name, category=sheet.title, section=section, location=clean(row[2]), civil=clean(row[3]), admin=clean(row[4]), gps=clean(row[5]).split('http')[0].strip(), status=status, condition=condition, usage=usage, row=rownum, maps=[], photos=[], warnings=[])
                records.append(current)
            if current:
                urls = re.findall(r'https?://[^\s,<>]+', ' '.join(clean(v) for v in row))
                for url in urls:
                    key = 'photos' if 'drive.google.com/' in url else 'maps' if 'maps' in url else None
                    if key and url not in current[key]: current[key].append(url)
    groups = defaultdict(list)
    for item in records:
        if item['gps']: groups[item['gps']].append(item)
    for group in groups.values():
        if len({r['location'].casefold() for r in group}) > 1:
            for item in group: item['warnings'].append('Koordinat sama digunakan pada lokasi berlainan. Sahkan kedudukan sebelum lawatan.')
    return records, incomplete

def main():
    records, incomplete = extract(ROOT / 'data.xlsx')
    payload = dict(records=records, incomplete=incomplete, modified=datetime.fromtimestamp((ROOT/'data.xlsx').stat().st_mtime, timezone(timedelta(hours=8))).strftime('%d/%m/%Y %H:%M'), logo='data:image/jpeg;base64,' + base64.b64encode((ROOT/'logo.jpg').read_bytes()).decode())
    html = (ROOT/'dashboard_template.html').read_text(encoding='utf-8').replace('__PAYLOAD__', json.dumps(payload, ensure_ascii=True).replace('</', '<\\/'))
    (ROOT/'Dashboard_Bangunan.html').write_text(html, encoding='utf-8')
    print(json.dumps({'assets': len(records), 'conditions': dict(Counter(r['condition'] for r in records)), 'incomplete':len(incomplete)}, ensure_ascii=True))

if __name__ == '__main__': main()
