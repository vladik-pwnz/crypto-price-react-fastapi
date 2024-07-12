Backend  
python3 -m venv venv  
. venv/bin/activate или .\venv\Scripts\activate.bat  
pip install -r requirements.txt  
or
cd backend  
poetry install  
poetry shell  
uvicorn src.main:app --reload (обязательно находясь внутри папки backend)  
  
Frontend  
npm create vite@latest  
npm install  
npm install -D tailwindcss  
npm install axios  
npm run dev  
