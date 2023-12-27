from django.shortcuts import redirect


def auth_middleware(get_response):
 def middleware(request):
  print("middleware")
  returnUrl=request.META['PATH_INFO']
  print(returnUrl)
  print(request.session.get('customer_id'))
  if not request.session.get('customer_id'):
   return redirect(f'login?return_url={returnUrl}')
  response=get_response(request)
  return response
 return middleware