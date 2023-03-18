from django.shortcuts import render
from datetime import date
from .models import Identifikation, ACLTyp, IDLog
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
        # is this slug ok length?
        if len(slug) != 50:
            raise Http404("No such ID found (len)")
        if request.user.is_authenticated and request.user.has_perm('ids.add_identifikation'):
            return render(request, 'id_create.html', {'slug': slug, 'acltypes': ACLTyp.objects.all()})
        raise Http404("No such ID found (no admin, no such slug)")

    if id.active == False or id.user == None:
        if request.user.is_authenticated and request.user.has_perm('ids.add_identifikation'):
            return render(request, 'id_activate.html', {'id': id, 'acltypes': ACLTyp.objects.all()})
        raise Http404("No such ID found (no admin, empty user)")
    else:
        # store searching in session
        if 'acl_search' in request.GET:
            request.session['acl_search'] = request.GET['acl_search']

        # get currently valid ACLs
        valid_acls = id.acl_set.filter(beginn__lte=date.today(), ende__gte=date.today())

        highest_plus = 0
        acl_dict = {}
        for acl in valid_acls:
            if acl.plus > highest_plus:
                highest_plus = acl.plus
            for acltyp in acl.type.all():
                acl_dict[acltyp.name] = {
                    'plus': acl.plus,
                    'acl': acl
                }
        
        # set AAA with highest plus
        if id.aaa:
            acl_dict['AAA'] = { 'plus': highest_plus, 'acl': None }

        # do we have an acl we are looking for?
        acl_search = False
        acl_search_plus = 0
        acl_ok = False
        matched_acl = None
        if 'acl_search' in request.session and request.session['acl_search'] != '':
            acl_search = True
            # we have one to search, look for it
            if request.session['acl_search'] in acl_dict:
                acl_ok = True
                acl_search_plus = acl_dict[request.session['acl_search']]['plus']
                matched_acl = acl_dict[request.session['acl_search']]['acl']
            elif 'AAA' in acl_dict:
                acl_ok = True
                acl_search_plus = acl_dict['AAA']['plus']

        # LOG Scan
        if acl_search and acl_ok:
            acltyp = ACLTyp.objects.get(name=request.session['acl_search'])
            IDLog.objects.create(identifikation=id, matched_type=acltyp, matched_acl=matched_acl, match_success=True)
        elif acl_search:
            try:
                acltyp = ACLTyp.objects.get(name=request.session['acl_search'])
                IDLog.objects.create(identifikation=id, matched_type=acltyp, match_success=False)
            except ObjectDoesNotExist:
                IDLog.objects.create(identifikation=id, match_success=False)
        else:
            IDLog.objects.create(identifikation=id)

        return render(request, 'id.html', {'id': id, 'acls': acl_dict, 'acl_search': acl_search, 'acl_ok': acl_ok, 'acltypes': ACLTyp.objects.all(), 'acl_search_plus': acl_search_plus})

