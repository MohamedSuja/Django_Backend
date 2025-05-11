from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from ..serializers import SearchPropertyRequestSerializer
from ..service import SearchPropertyService


@require_http_methods(["GET"])
def SearchProperty(request):

    serializer = SearchPropertyRequestSerializer(data=request.GET)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    params = serializer.validated_data
    listings = SearchPropertyService.get_listings(params)

    if not listings:
        return JsonResponse({"message": "No listings found"}, status=404)

    return JsonResponse({"listings": listings}, status=200)

