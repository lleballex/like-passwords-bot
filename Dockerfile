FROM python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir src/db
CMD python src/bot.py migrate && python src/bot.py
