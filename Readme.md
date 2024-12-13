### Step how to run this project

python -m venv .venv

.venv\Scripts\activate <<<----- for windows 
.venv/bin/activate <<<----- for Linux/Macos

pip install -r requirements.txt

uvicorn main:app --reload

---

### migrate command

hapus folder migrations (jangan lupa server harus jalan)

aerich init-db
aerich migrate
aerich upgrade
