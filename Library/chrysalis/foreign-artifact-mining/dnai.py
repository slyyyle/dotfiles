from ollama import Client

def client_connect ():
    client = Client(
    host='http://omacsndbx01.signatureperformance.com:11434')
    return client

client = client_connect()

print(client.list())

response = client.chat(model='granite3.1-dense:2b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response)
