import fitz  # PyMuPDF
import json
import re
from collections import defaultdict

# Caminho para o seu PDF
pdf_path = r"C:\Users\Ramon\Documents\01_Ramon\04_FaculdadeDeEng.Elétrica\04_Periodo\ProjetoDeAmbienteComputacional\projetoASDU\salas\06-DESC-2025-1.pdf"

# Lista que armazenará as linhas do PDF
linhas_extraidas = []

# Abre o PDF
with fitz.open(pdf_path) as doc:
    for page in doc:
        texto = page.get_text("text")  # Mantém a ordem visual
        linhas = texto.split('\n')     # Divide por linha visual
        linhas_extraidas.extend(linhas)


# Suponha que esta seja sua lista já extraída com PyMuPDF:
linhas = linhas_extraidas  # Substitua com a sua lista real

# Limpa espaços e remove vazios
linhas = [l.strip() for l in linhas if l.strip()]

disciplinas = []
i = 0

while i < len(linhas):
    linha = linhas[i]

    # Detecta novo código
    if re.match(r"^\d{5}$", linha):
        codigo = linha
        i += 1
        disciplina = linhas[i]
        i += 1
        turma = linhas[i] if linhas[i].isdigit() else "1"
        i += 1
        professor = linhas[i]
        i += 1

        horario_dict = defaultdict(list)
        salas = []

        while i < len(linhas):
            atual = linhas[i]

            if re.match(r"^\d{5}$", atual):  # nova disciplina
                break

            # Horário
            if re.match(r"^(SEG|TER|QUA|QUI|SEX|SAB|DOM)", atual.upper()):
                partes = atual.replace(",", "").split()
                dia = partes[0].lower()
                tempos = [t.lower() for t in partes[1:]]
                horario_dict[dia].extend(tempos)
                i += 1
                continue

            # Sala
            if re.match(r"^\d{4}-[A-Z]", atual):
                salas.append(atual)
                i += 1
                continue

            # Caso inesperado
            i += 1

        # Organiza os horários agrupando por dia
        horario_final = []
        for dia, tempos in horario_dict.items():
            tempos_unicos = sorted(set(tempos), key=lambda t: (t[0], int(t[1:])))
            horario_final.append(f"{dia} {' '.join(tempos_unicos)}")

        disciplinas.append({
            "codigo": codigo,
            "disciplina": disciplina,
            "turma": turma,
            "professor": professor,
            "horario": " ".join(horario_final),
            "sala": " ".join(salas)
        })

    else:
        i += 1

# Salva como JSON
with open("disciplinas_SIMPLES.json", "w", encoding="utf-8") as f:
    json.dump(disciplinas, f, ensure_ascii=False, indent=2)

print("✅ Arquivo disciplinas_SIMPLES.json gerado com sucesso!")
