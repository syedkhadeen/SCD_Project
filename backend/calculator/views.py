from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def calculate_load(request):
    try:
        # Get the list of appliances from the request data
        appliances = request.data.get('appliances', [])
        
        # Calculate total load
        total_load = sum(int(appliance['watts']) * int(appliance['quantity']) for appliance in appliances)

        # Return the total load as a JSON response
        return Response({'totalLoad': total_load}, status=status.HTTP_200_OK)
    except Exception as e:
        # Return an error message as a JSON response
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
