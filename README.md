# Email senting service

## Run locally (without container)

```
cp .env.example .env # Read/edit

cd src/web

. venv/bin/activate
flask run
```

## Podman setup

```
. venv/bin/activate
pip install https://github.com/containers/podman-compose/archive/devel.tar.gz
```

## Docs
Full api docs:
```
http://127.0.0.1:5000/docs#/
```


# Send an email API example

```
#!/bin/bash
curl --request POST \
  --url http://127.0.0.1:5000/send-email \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{
  "BCC": [
    "user@example.com"
  ],
  "BODY": "string",
  "CC": [
    "user@example.com"
  ],
  "FROM": "user@example.com",
  "SUBJECT": "string",
  "TO": [
    "user@example.com"
  ]
}'

```
