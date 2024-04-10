FROM python:3.11.6

SHELL [ "/bin/bash", "-c" ]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -rms /bin/bash mainus && chmod 777 /opt /run

WORKDIR /backend
COPY --chown=mainus:mainus . .

RUN pip install -r requirements.txt

CMD sleep 5 && python manage.py migrate \
    && python manage.py setup_superuser \
    && python manage.py fill_database \
    && python manage.py collectstatic --no-input \
    && gunicorn -b 0.0.0.0:8000 -w 8 --threads 3 --timeout 30 backend.wsgi:application
