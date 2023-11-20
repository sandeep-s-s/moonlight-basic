from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import AppForm
from django.http import JsonResponse
import requests
import json
import base64 


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def index_action(request):
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            v = form.data
            #https://stackoverflow.com/questions/39565023/django-querydict-only-returns-the-last-value-of-a-list
            url = form.cleaned_data['url']
            method = form.cleaned_data['method']
            param_key_list = form.data.getlist('param_key')
            param_value_list = form.data.getlist('param_value')
            header_key_list = form.data.getlist('header_key')
            header_value_list = form.data.getlist('header_value')
            request_body = form.data['request_body']
            auth_type = form.data['auth_type']
            json_object = ''
            if request_body:
                json_object = json.loads(request_body)
            payload = dict(zip(param_key_list,param_value_list))
            headers_payload = dict(zip(header_key_list,header_value_list))
            if auth_type == 'basicAuth':
                basic_username = form.data['basic_username']
                basic_password = form.data['basic_password']
                basic_auth_byte_array = basic_username+":"+basic_password
                basic_auth_string = base64.b64encode(basic_auth_byte_array.encode()).decode("utf-8")
                headers_payload.update({ 'Authorization': 'Basic '+basic_auth_string })
            if auth_type == 'bearerToken':
                bearer_token = form.data['bearer_token']
                headers_payload.update({ 'Authorization': 'Bearer '+bearer_token })
            print(headers_payload)
            print(f"Url: {url}, Method: {method}, Param keys: {param_key_list}, param values: {param_value_list},Headers {headers_payload}")
            try:
                print(method)
                response = ''
                if method == 'GET':
                # Make the GET request
                    response = requests.get(url,params=payload,headers=headers_payload)
                if method == 'POST':
                    headers_payload.update({'accept': 'application/json','Content-Type': 'application/json'})
                    response = requests.request("POST", url, headers=headers_payload, data=json_object,params=payload)
                    print(response)
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse the response content as needed
                    api_data = response.json()
                    response_header = dict(response.headers)
                    print(response.headers)

                    # Process the data or return it as a JSON response
                    return JsonResponse({'status': 'success', 'data': api_data,'headers':response_header})
                else:
                    # Handle the case where the API request was not successful
                    return JsonResponse({'status': 'error', 'message': f"API request failed with status code {response.status_code}"})
            except Exception as e:
                print(e)
                # Handle any exceptions that may occur during the request
                return JsonResponse({'status': 'error', 'message': f"An error occurred: {str(e)}"})
            # You can also save the data to the database here if needed
            # MyModel.objects.create(name=name, email=email)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = AppForm()

    return render(request, 'my_template.html', {'form': form})