import json
import re

# Carrega o JSON original
with open(r"C:\Users\Ramon\PycharmProjects\pythonProject\ProjetoASDU\PDF_JSON\disciplinas_SIMPLES.json", encoding="utf-8") as f:
    disciplinas = json.load(f)

disciplinas_convertidas = []

for disc in disciplinas:
    dias_horas = disc["horario"].split()
    salas = disc["sala"].split()

    aulas = []
    i = 0
    while i < len(dias_horas):
        item = dias_horas[i].upper()
        if item in {"SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"}:
            dia = item
            i += 1
            blocos = []
            while i < len(dias_horas) and not re.match(r"^(SEG|TER|QUA|QUI|SEX|SAB|DOM)$", dias_horas[i].upper()):
                blocos.append(dias_horas[i].upper())
                i += 1
            aulas.append({
                "dia": dia,
                "horarios": blocos
            })
        else:
            i += 1

    # Associa as salas: se só há uma sala, usar para todas
    if len(salas) == 1:
        for aula in aulas:
            aula["sala"] = salas[0]
    else:
        for idx, aula in enumerate(aulas):
            aula["sala"] = salas[idx] if idx < len(salas) else salas[-1]

    disciplinas_convertidas.append({
        "codigo": disc["codigo"],
        "disciplina": disc["disciplina"],
        "turma": disc["turma"],
        "professor": disc["professor"],
        "aulas": aulas
    })

# Salva o novo JSON
with open("../disciplinas_FINAL.json", "w", encoding="utf-8") as f:
    json.dump(disciplinas_convertidas, f, ensure_ascii=False, indent=2)

print("✅ Arquivo disciplinas_FINAL.json gerado com sucesso.")




