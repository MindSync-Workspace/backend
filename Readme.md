python -m venv venv

venv\Scripts\activate
venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

---

### migrate command

// kalo update constraint harus hapus manual dbnya

hapus folder migrations (jangan lupa server harus jalan)

aerich init-db
aerich migrate
aerich upgrade
