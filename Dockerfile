### STAGE 1: Build ###

FROM python:3.7-alpine as build

# Install and compile dependencies
RUN apk add --no-cache gcc make libressl-dev musl-dev libffi-dev

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

### STAGE 2: Production Environment ###

FROM python:3.7-alpine

# Install and compile dependencies
RUN apk add --no-cache libressl-dev

# Copy python libs
COPY --from=build /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/

WORKDIR /usr/src/app

COPY . .

ENTRYPOINT [ "python", "./app.py" ]