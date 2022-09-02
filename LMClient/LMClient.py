import requests
import json
import hashlib
import base64
import time
import hmac as h

class LMClient:

    def __init__(self, account, accessId, accessKey):
        self.account = account
        self.accessId = accessId
        self.accessKey = accessKey

    def toString(self):
        """returns a string representation of the object"""
        return "account: " + self.account + " accessId: " + self.accessId

    def response(self, httpVerb, resourcePath, queryParams, data):
        """returns a response object"""
        #Construct URL 
        url = 'https://'+ self.account +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams
        #Get current time in milliseconds
        epoch =str(int(time.time() * 1000))
        #Concatenate Request details
        requestVars = httpVerb + epoch + data + resourcePath
        #Construct signature
        hmac = h.new(self.accessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
        signature = base64.b64encode(hmac.encode())
        #Construct headers
        auth = 'LMv1 ' + self.accessId + ':' + signature.decode() + ':' + epoch
        headers = {'Content-Type':'application/json','Authorization':auth}
        #Make request
        
        if httpVerb == 'GET':
            response = requests.get(url, data=data, headers=headers)
        elif httpVerb == 'POST':
            response = requests.post(url, data=data, headers=headers)
        elif httpVerb == 'PUT':
            response = requests.put(url, data=data, headers=headers)
        elif httpVerb == 'DELETE':
            response = requests.delete(url, data=data, headers=headers)
        elif httpVerb == 'PATCH':
            response = requests.patch(url, data=data, headers=headers)
        else:
            raise ValueError('Invalid HTTP verb: {}'.format(httpVerb))
        return response

    def get(self, resourcePath, queryParam=''):
        """HTTP GET
            :param resourcePath: The resource path
            :param queryParam: The optional query parameters must start with '?'
            :return: The response content
        """
        response = self.response('GET', resourcePath, queryParam, '')

        if(response.status_code != 200):
            raise ValueError('HTTP GET failed: {}'.format(response.status_code))
        else:
            entity = json.loads(response.content)['data']
            return entity

    def post(self, resourcePath, queryParams='', data=''):
        """HTTP POST
            :param resourcePath: The resource path
            :param queryParams: The optional query parameters must start with '?'
            :param data: The data to be posted
            :return: The response content
        """
        response = self.response('POST', resourcePath, queryParams, data)

        if(response.status_code != 200):
            raise ValueError('HTTP POST failed: {}'.format(response.status_code))
        else:
            entity = json.loads(response.content)['data']
            return entity

    def put(self, resourcePath, queryParams='', data=''):
        """HTTP PUT
            :param resourcePath: The resource path
            :param queryParams: The optional query parameters must start with '?'
            :param data: The data to be posted
            :return: The response content
        """
        response = self.response('PUT', resourcePath, queryParams, data)

        if(response.status_code != 200):
            raise ValueError('HTTP PUT failed: {}'.format(response.status_code))
        else:
            entity = json.loads(response.content)['data']
            return entity

    def delete(self, resourcePath, queryParams='', data=''):
        """HTTP DELETE
            :param resourcePath: The resource path
            :param queryParams: The optional query parameters must start with '?'
            :param data: The data to be posted
            :return: The response content
        """
        response = self.response('DELETE', resourcePath, queryParams, data)

        if(response.status_code != 200):
            raise ValueError('HTTP DELETE failed: {}'.format(response.status_code))
        else:
            entity = json.loads(response.content)['data']
            return entity

    def patch(self, resourcePath, queryParams='', data=''):
        """HTTP PATCH
            :param resourcePath: The resource path
            :param queryParams: The optional query parameters must start with '?'
            :param data: The data to be posted
            :return: The response content
        """
        response = self.response('PATCH', resourcePath, queryParams, data)

        if(response.status_code != 200):
            raise ValueError('HTTP PATCH failed: {}'.format(response.status_code))
        else:
            entity = json.loads(response.content)['data']
            return entity