from django.shortcuts import render
from datetime import date
from .models import Identifikation
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, Http404

# this view simply loads an ID Card's data
# If the card is not in use, and someone is logged in that has permission to add one, this option is offered
# otherwise a 404 error is displayed
# If the card is found it is displayed
# This displaying system allows marking a certain ACL field to look for!

def id(request, slug):
    try:
        id = Identifikation.objects.get(slug=slug)
    except Identifikation.DoesNotExist:
        raise Http404("No such ID found")

    if (id.user == None):
        if request.user.is_authenticated and request.user.has_perm('ids.add_identifikation'):
            return render(request, 'id_activate.html', {'id': id})
        raise Http404("No such ID found")
    else:
        # store searching in session
        if 'acl_search' in request.GET:
            request.session['acl_search'] = request.GET['acl_search']

        # get currently valid ACLs
        valid_acls = id.acl_set.filter(beginn__lte=date.today(), ende__gte=date.today())

        acl_dict = []
        for acls in valid_acls:
            for acl in acls.type.all():
                acl_dict += [acl.name]

        # do we have an acl we are looking for?
        acl_search = False
        acl_ok = False
        if 'acl_search' in request.session:
            acl_search = True
            # we have one to search, look for it
            acl_ok = True if request.session['acl_search'] in acl_dict or 'AAA' in acl_dict else False

        return render(request, 'id.html', {'id': id, 'acls': acl_dict, 'acl_search': acl_search, 'acl_ok': acl_ok})

