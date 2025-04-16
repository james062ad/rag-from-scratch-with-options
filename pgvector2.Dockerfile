# Stage 1: Build pgvector
FROM postgres:15-alpine AS builder

RUN apk add --no-cache \
  build-base \
  git \
  postgresql-dev \
  clang \
  llvm-dev

WORKDIR /build

RUN git clone --branch v0.5.0 https://github.com/pgvector/pgvector.git \
  && cd pgvector \
  && make \
  && make install

# Stage 2: Final image with extension installed
FROM postgres:15-alpine

COPY --from=builder /usr/local/lib/postgresql/ /usr/local/lib/postgresql/
COPY --from=builder /usr/local/share/postgresql/ /usr/local/share/postgresql/

# Optional: Set default user/password/db
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydb
