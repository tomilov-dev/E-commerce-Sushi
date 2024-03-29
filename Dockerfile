FROM python:3.11.6

SHELL [ "/bin/bash", "-c" ]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev libpq-dev \ 
    libmariadb-dev libmariadb-dev-compat gettext cron openssh-client locales neovim

RUN useradd -rms /bin/bash mainus && chmod 777 /opt /run

WORKDIR /mainus

RUN mkdir /mainus/static && mkdir /mainus/media && chown -R mainus:mainus /mainus && chmod 755 /mainus

COPY --chown=mainus:mainus . .

RUN pip install -r requirements.txt

USER mainus

CMD ["gunicorn", "-b", "0.0.0.0:8001", "backend.backend:application"]
