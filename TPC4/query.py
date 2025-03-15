import requests

def query_graphdb(endpoint_url, sparql_query):
	headers = { 'Accept': 'application/json' }
	
	try:
		response = requests.get(endpoint_url, headers=headers, params={'query': sparql_query})
		response.raise_for_status()
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
		return None
	except requests.exceptions.ConnectionError as conn_err:
		print(f"Connection error occurred: {conn_err}")
		return None
	except requests.exceptions.Timeout as timeout_err:
		print(f"Timeout error occurred: {timeout_err}")
		return None
	except requests.exceptions.RequestException as req_err:
		print(f"An error occurred: {req_err}")
		return None

	try:
		return response.json()
	except ValueError as json_err:
		print(f"JSON decode error: {json_err}")
		return None