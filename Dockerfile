# Usa un'immagine base di Python
FROM surnet/alpine-python-wkhtmltopdf:3.9.9-0.12.6-small

# Imposta l'ambiente di lavoro come /app
WORKDIR /app

# Copia il file requirements.txt nella directory /app
COPY requirements.txt .

# Installa le dipendenze
RUN pip install -r requirements.txt

# Copia il codice della tua applicazione Django nella directory /app
COPY . .

# Porta 8000 del container a 8000 del host
EXPOSE 8000

# Comando per eseguire il server Django quando il container viene avviato
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
