from django.shortcuts import redirect
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from requests_oauthlib import OAuth2Session
from MyGitHubProject.defines import SESSION_VALIDATED, GITHUB_APP_USERNAME, GITHUB_APP_PASSWORD, \
    SESSION_APP_GITHUB_OAUTH_TOKEN, GITHUB_OAUTH_LOGIN_AUTH, GITHUB_OAUTH_LOGIN_TOKEN, GITHUB_APP_SCOPE, \
    GITHUB_ORG_REPO_NAME_WASF, GITHUB_ORG_REPO_NAME_SFT
from django.core.urlresolvers import reverse


def index(request):
    try:
        error = request.session[SESSION_VALIDATED]
    except:
        error = None
    request.session[SESSION_VALIDATED] = None
    t = loader.get_template('index.html')
    c = Context({ 'error': error,
    })
    return HttpResponse(t.render(c))


def credentials_validate(request):
    authorization_url = None
    state = None

    github = OAuth2Session(GITHUB_APP_USERNAME, scope=GITHUB_APP_SCOPE)

    authorization_url, state = github.authorization_url(GITHUB_OAUTH_LOGIN_AUTH)

    if state and authorization_url:
        request.session[SESSION_APP_GITHUB_OAUTH_TOKEN] = state
        return redirect(authorization_url)
    else:
        request.session[SESSION_VALIDATED] = "Incorrect GitHub OAuth Application ID or State"
        return HttpResponseRedirect(reverse('index_page'))


def auth(request):
    token = None
    try:
        code = request.GET['code']
    except:
        code = None
    try:
        state = request.session[SESSION_APP_GITHUB_OAUTH_TOKEN]
    except:
        state = None

    github = OAuth2Session(GITHUB_APP_USERNAME, state=state)
    token = github.fetch_token(GITHUB_OAUTH_LOGIN_TOKEN, client_secret=GITHUB_APP_PASSWORD,
                code=code)

    if token:
        request.session[SESSION_VALIDATED] = "Validated"
        request.session[SESSION_APP_GITHUB_OAUTH_TOKEN] = token
        return HttpResponseRedirect(reverse('dashboard_page'))
    else:
        request.session[SESSION_VALIDATED] = "Incorrect GitHub OAuth Application Code"
        return HttpResponseRedirect(reverse('index_page'))


def exit(request):
    request.session[SESSION_VALIDATED] = None
    return HttpResponseRedirect(reverse('index_page'))


def mydashboard(request):
    try:
        if not request.session[SESSION_VALIDATED] == "Validated":
            return HttpResponseRedirect(reverse('index_page'))
    except:
        return HttpResponseRedirect(reverse('index_page'))

    t = loader.get_template('mydashboard.html')
    c = Context({'GITHUB_ORG_REPO_NAME_WASF':GITHUB_ORG_REPO_NAME_WASF,
                 'GITHUB_ORG_REPO_NAME_SFT':GITHUB_ORG_REPO_NAME_SFT,
    })
    return HttpResponse(t.render(c))


