FROM python:3.8

# 讓 print 的東西不會被緩衝，能即時顯示在終端
ENV PYTHONUNBUFFERED=1  

WORKDIR /workplace
COPY ./backend /workplace

RUN pip install -r requirements.txt
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]