python -m venv venv

venv\Scripts\activate
venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

---

### migrate command

aerich migrate
aerich upgrade
