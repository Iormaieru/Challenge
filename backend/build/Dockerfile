FROM python:3.10

ENV PYTHONUNBUFFERED=1

ENV C_FORCE_ROOT=1

WORKDIR /backend

RUN apt-get update && apt-get install -y \
	gcc \
	musl-dev \
	python3-dev \
	libc-dev \
	libpq-dev \
	libffi-dev \
	libssl-dev \
	libjpeg-dev \
	zlib1g-dev \
	default-libmysqlclient-dev \
	poppler-utils

COPY . /backend/

RUN chmod -R +x /backend/build/cmd/*.sh

RUN /backend/build/cmd/dependencies.sh

ENTRYPOINT [ "sh", "/backend/build/cmd/run_backend.sh" ]