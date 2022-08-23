FROM python:3.9

RUN pip install django

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY requirements.txt ./ 

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

ENTRYPOINT [ "bash", "-l", "/user/src/app/api_entrypoint.sh" ]

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "review_king.wsgi:application"]