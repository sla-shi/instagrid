# instagrid
Instagrid technical assessment

Install dependencies:
`pip install -r requirements.txt`

Run Chalice locally:
`chalice local`

Test POST request to lambda with a sample payload.
`curl -X POST -H "Content-Type: application/json" -d @tests/payload.json http://127.0.0.1:8000`
