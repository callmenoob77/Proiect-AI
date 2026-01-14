# SmarTest AI

Aplicație web pentru generarea și evaluarea automată a întrebărilor din domeniul Inteligenței Artificiale. Sistemul suportă multiple tipuri de întrebări (strategie, CSP, Minimax, Nash Equilibrium) și oferă evaluare inteligentă a răspunsurilor folosind procesare de limbaj natural.

---

## Cuprins

1. [Cerințe de Sistem](#cerințe-de-sistem)
2. [Instalare](#instalare)
3. [Configurare Baza de Date](#configurare-baza-de-date)
4. [Rulare](#rulare)
5. [Ghid de Utilizare](#ghid-de-utilizare)
6. [Structura Proiectului](#structura-proiectului)
7. [Funcționalități](#funcționalități)
8. [Tehnologii Utilizate](#tehnologii-utilizate)

---

## Cerințe de Sistem

### Software necesar

- Python 3.10 sau superior
- Node.js 18.x sau superior
- PostgreSQL 14 sau superior
- pip (package manager Python)
- npm (package manager Node.js)

### Sistem de operare

Aplicația a fost testată pe:
- Ubuntu 22.04 LTS (WSL2)
- Windows 11

---

## Instalare

### 1. Clonare repository

```bash
git clone https://github.com/callmenoob77/Proiect-AI.git
cd Proiect-AI
```

### 2. Backend (Python/FastAPI)

```bash
# Crearea mediului virtual
python -m venv venv

# Activare mediu virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Instalare dependențe
pip install -r requirements.txt
```

Dependențele principale instalate:
- `fastapi` - Framework web asincron
- `uvicorn` - Server ASGI
- `sqlalchemy` - ORM pentru baza de date
- `sentence-transformers` - Model NLP pentru evaluare semantică

### 3. Frontend (React)

```bash
cd frontend
npm install
cd ..
```

---

## Configurare Baza de Date

### 1. Creare bază de date PostgreSQL

```sql
CREATE DATABASE smartest_ai;
```

### 2. Configurare conexiune

Editați fișierul `app/database.py` și actualizați URL-ul de conexiune conform setărilor locale:

```python
DATABASE_URL = "postgresql://postgres:parola_ta@localhost/Proiect-AI"
```

Formatul: `postgresql://utilizator:parola@host/nume_baza_de_date`

### 3. Adăugare tipuri de întrebări în baza de date

Executați următoarele comenzi în PostgreSQL (pgAdmin sau psql):

```sql
-- Tipuri de probleme de bază
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'N_QUEENS';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'HANOI';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'GRAPH_COLORING';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'KNIGHT_TOUR';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'BACKTRACKING_ASSIGNMENT';

-- Tipuri adăugate ulterior
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'RIVER_CROSSING';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'WATER_JUG';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'SLIDING_PUZZLE';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'X_O';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'CSP_PROBLEM';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'A_STAR_DESCRIPTION';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'MINIMAX_TREE';
ALTER TYPE question_type ADD VALUE IF NOT EXISTS 'GAME_MATRIX';
```

### 4. Conexiune la baza de date hostată (Neon)

Dacă folosiți o bază de date PostgreSQL hostată în cloud (Neon), urmați acești pași pentru configurarea conexiunii în pgAdmin:

**Pasul 1: Obțineți datele de conectare**

Veți primi un URL de conectare (connection string) de forma:
```
postgresql://neondb_owner:PAROLA_SECRETA@ep-purple-scene-xxxx.aws.neon.tech/neondb
```

**Pasul 2: Adăugați un server nou în pgAdmin**

1. Deschideți pgAdmin
2. Click-dreapta pe "Servers" în meniul din stânga
3. Selectați "Create" -> "Server..."

**Pasul 3: Completați detaliile conexiunii**

Tab-ul **General**:
- Name: `Proiect-AI Neon` (sau alt nume descriptiv)

Tab-ul **Connection**:

| Câmp | Valoare (din URL) |
|------|-------------------|
| Host name/address | Partea după `@` și înainte de `/` (ex: `ep-purple-scene-xxxx.aws.neon.tech`) |
| Port | `5432` |
| Maintenance database | Partea după ultimul `/` (ex: `neondb`) |
| Username | Partea dintre `//` și `:` (ex: `neondb_owner`) |
| Password | Parola din URL (`PAROLA_SECRETA`) |

**Pasul 4: Configurați SSL (OBLIGATORIU)**

1. Mergeți la tab-ul **Parameters**
2. Găsiți rândul "SSL mode"
3. Schimbați valoarea în **Require**

**Pasul 5: Salvați și conectați-vă**

Apăsați "Save". Serverul va apărea în lista din stânga. Pentru a vedea tabelele, navigați la:
`Databases -> neondb -> Schemas -> public -> Tables`

**Configurare în aplicație**

În fișierul `app/database.py`, actualizați URL-ul:
```python
DATABASE_URL = "postgresql://neondb_owner:PAROLA_SECRETA@ep-purple-scene-xxxx.aws.neon.tech/neondb?sslmode=require"
```

---

## Rulare

Aplicația necesită două terminale separate.

### Terminal 1 - Backend

```bash
cd Proiect-AI
source venv/bin/activate  # sau .\venv\Scripts\activate pe Windows
uvicorn app.main:app --reload
```

Backend-ul va porni pe `http://localhost:8000`

### Terminal 2 - Frontend

```bash
cd Proiect-AI/frontend
npm start
```

Frontend-ul va porni pe `http://localhost:3000`

### Verificare funcționare

Accesați în browser:
- Frontend: http://localhost:3000

---

## Ghid de Utilizare

După accesarea aplicației în browser, utilizatorul este întâmpinat cu pagina principală.

### Pagina Principală

Pe pagina principală există două moduri de generare a întrebărilor:

**1. Întrebare generată** (selectat implicit)
- Sistemul generează automat o întrebare aleatorie din capitolele disponibile
- Utilizatorul poate filtra după capitol și dificultate

**2. Întrebare pe pattern**
- Utilizatorul specifică manual parametrii întrebării
- Util pentru exersarea unui anumit tip de problemă

### Selectoare disponibile

| Element | Descriere |
|---------|----------|
| Alege capitolul | Filtrare după: Toate capitolele, Strategii algoritmice, Algoritmi de căutare și CSP, Teoria Jocurilor |
| Dificultate | Ușor (instanțe mici), Mediu (standard), Greu (complex) |
| Răspuns Multiplu | Întrebare cu 4 variante de răspuns |
| Răspuns Text | Întrebare cu răspuns liber evaluat prin NLP |
| Creează Test | Generează un set de mai multe întrebări |

### Flux de lucru pentru întrebări individuale

1. Selectați capitolul dorit (opțional)
2. Selectați dificultatea
3. Alegeți tipul de răspuns (Multiplu sau Text)
4. Apăsați butonul **Generează întrebare**
5. Citiți enunțul și vizualizările asociate (arbori, matrici)
6. Selectați răspunsul sau scrieți în câmpul text
7. Apăsați **Verifică răspunsul**
8. Consultați feedback-ul și soluția de referință
9. Apăsați unul din butoanele de generare pentru o nouă întrebare

### Flux de lucru pentru Mod Test

1. Selectați **Creează Test** de pe pagina principală
2. Alegeți numărul de întrebări (1-20)
3. Selectați modul: **Practice** (fără limită de timp) sau **Examen** (2 minute/întrebare)
4. Apăsați **Începe Testul**
5. Navigați între întrebări folosind butoanele Anterior/Următoarea sau indicatorii numerotați
6. La final, apăsați **Finalizează Testul**
7. Consultați rezultatele detaliate pentru fiecare întrebare

### Întrebări pe Pattern

Pentru modul **Întrebare pe pattern**, selectați tipul și completați câmpurile:

| Tip Pattern | Câmpuri necesare |
|-------------|------------------|
| Teorie | Nume strategie (ex: A* Search) |
| Strategie | Nume problemă, Instanță |
| CSP | Variază în funcție de subtip (FC, MRV, AC3) |
| Minimax | Fără câmpuri - generare automată |
| Nash | Fără câmpuri - generare automată |

---

## Structura Proiectului

```
Proiect-AI/
├── app/                          # Backend FastAPI
│   ├── core/                     # Logica de bază
│   │   ├── generator.py          # Generator întrebări principale
│   │   ├── evaluator.py          # Evaluator răspunsuri (NLP)
│   │   ├── csp_generator.py      # Generator CSP
│   │   ├── minimax_generator.py  # Generator Minimax
│   │   ├── minimax_solver.py     # Solver Alpha-Beta
│   │   ├── nash_generator.py     # Generator Nash Equilibrium
│   │   └── csp_solver.py         # Solver CSP
│   ├── models/                   # Modele SQLAlchemy
│   ├── routers/                  # API endpoints
│   ├── schemas/                  # Scheme Pydantic
│   ├── database.py               # Configurare DB
│   └── main.py                   # Entry point aplicație
├── frontend/                     # Frontend React
│   ├── src/
│   │   ├── components/
│   │   │   ├── TreeVisualizer.js       # Vizualizare arbori Minimax
│   │   │   ├── GameMatrixVisualizer.js # Vizualizare matrice Nash
│   │   │   └── TestMode.jsx            # Componenta mod test
│   │   └── App.js                # Componenta principală
│   └── package.json
├── requirements.txt              # Dependențe Python
└── README.md                     # Acest fișier
```

---

## Funcționalități

### Tipuri de Întrebări

| Tip | Descriere | Mod răspuns |
|-----|-----------|-------------|
| Strategii Algoritmice | N-Queens, Turnurile Hanoi, Graph Coloring | Multiple choice / Text |
| CSP | Forward Checking, MRV, Arc Consistency | Multiple choice / Text |
| Minimax | Arbori de joc cu Alpha-Beta Pruning | Multiple choice / Text |
| Nash Equilibrium | Jocuri în formă normală | Multiple choice / Text |

### Moduri de Utilizare

1. **Întrebare Generată** - Sistem generează aleatoriu o întrebare
2. **Întrebare pe Pattern** - Utilizatorul specifică parametrii (problemă, instanță)
3. **Mod Test** - Set de întrebări cu scor final

### Evaluare Răspunsuri

Sistemul folosește o abordare hibridă pentru evaluarea răspunsurilor text:
- 60% - Similaritate semantică (Sentence Transformers)
- 40% - Potrivire cuvinte cheie

Model NLP utilizat: `paraphrase-multilingual-MiniLM-L12-v2` (suport limba română)

---

## Tehnologii Utilizate

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Sentence Transformers (NLP)

### Frontend
- React 18
- Tailwind CSS
- Lucide React (iconuri)

---

## Autori

Proiect realizat pentru cursul de Inteligență Artificială.

---

## Notă

La prima rulare, modelul Sentence Transformers va fi descărcat automat (aproximativ 400MB). Aceasta poate dura câteva minute în funcție de viteza conexiunii la internet.
