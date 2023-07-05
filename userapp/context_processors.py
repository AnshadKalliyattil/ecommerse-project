from accounts.models import*
def checkid(request):
    if 'user_id' in request.session:
        logi = request.session.get('user_id')
        if Accounts.object.filter(username = logi):
            id = Accounts.object.get(username = logi)
        else:
            id = None
        return {
            'id' : id
        }
    else:
        return {'id':None}
