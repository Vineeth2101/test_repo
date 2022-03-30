
#THIS IS PRICE API
def coupon_details(request):
    retailer = request.GET.get("retailer", '')
    merchant = request.GET.get("merchant", '')
    pdp = request.GET.get("pdp", '')
    source = request.GET.get("source", '').strip().lower()
    if not retailer and merchant:
        retailer = merchant
    if not retailer:
        return JsonResponse({'error': "Retailer missing"}, status=400)
    cache_key_prefix = 'offers_details_{}'.format(retailer.lower())
    print('cache_key_prefix', cache_key_prefix)
    print('request.build_absolute_uri()', request.build_absolute_uri())
    cache_key = generate_cache_key_for_url(url=request.build_absolute_uri(), key_prefix=cache_key_prefix)
    if cache_key in cache:
        print("CACHED COUPONS DETAILS", cache_key_prefix)
        # Yeah we have cached data
        data = cache.get(cache_key)
        return JsonResponse(data)
    result = get_coupons(retailer, pdp, source)
    cache.set(cache_key, result, cache_max_age)
    return JsonResponse(result)
