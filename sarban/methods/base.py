import requests, json

import sarban
from sarban import errors

class Base:

    def request(
        self: "sarban.SARBAN",
        path: str,
        method: str,
        headers: dict,
        data: dict = None

    ) -> requests.Response:
        """Request to the Marzban.

        Parameters:
            path (``str``):
                The request path, you can see all of them in your API documention of MArzban
                
            method (``str``):
                The request method
                
            data (``dict``, optional):
                The request parameters, None is set for default but it's necessary for some POST methods
            
            headers (``dict``):
                The request headers

        Returns:
            `~requests.Response`: On success, the response is returned.
        """
        


        url = f"{self.full_address}/api/{path}"

        if method == "GET":
            response = requests.get(url, headers=headers, data=json.dumps(data), verify=self.https)
        elif method == "POST":
            if "admin/token" in path:
                response = requests.post(url, headers=headers, data=data, verify=self.https)
            else:
                response = requests.post(url, headers=headers, data=json.dumps(data), verify=self.https)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=json.dumps(data), verify=self.https)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, verify=self.https)



        return response

    def verify_response(
        self: "sarban.SARBAN",
        response: requests.Response
    ) -> requests.Response:
        if response.status_code != 404 and response.headers.get('Content-Type').startswith('application/json'):
            return response.json()
        
        raise errors.NotFound()