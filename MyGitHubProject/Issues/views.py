from celery.utils import jsonify
from django.core.urlresolvers import reverse
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
import requests
import json
import operator
from requests_oauthlib import OAuth2Session
from MyGitHubProject.Issues.forms import AddIssueForm
from MyGitHubProject.defines import GITHUB_ORG_REPO_NAME_WASF, GITHUB_ORG_API_REPO_ISSUES_WASF, GITHUB_USERNAME, \
    GITHUB_PASSWORD, SESSION_VALIDATED, GITHUB_APP_USERNAME, SESSION_APP_GITHUB_OAUTH_TOKEN, GITHUB_ORG_REPO_NAME_SFT, \
    GITHUB_ORG_API_REPO_ISSUES_SFT, GITHUB_ORG_API_REPO_LABELS_WASF, GITHUB_ORG_API_REPO_LABELS_SFT


# This View is Display the list of Issues (All the processing happen in the view)
def view_issues_1(request, repo):
    # Security check if you have valid Token
    try:
        if not request.session[SESSION_VALIDATED] == "Validated":
            return HttpResponseRedirect(reverse('index_page'))
    except:
        return HttpResponseRedirect(reverse('index_page'))

    api_repo_issues = None
    api_repo_name = ""
    # Get selected Repo
    if repo == GITHUB_ORG_REPO_NAME_WASF:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_WASF
        api_repo_name = GITHUB_ORG_REPO_NAME_WASF
    elif repo == GITHUB_ORG_REPO_NAME_SFT:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_SFT
        api_repo_name = GITHUB_ORG_REPO_NAME_SFT
    else:
        return HttpResponseRedirect(reverse('index_page'))

    error = None
    issue_items = None
    issue_list = []

    # Set Auth
    github = OAuth2Session(GITHUB_APP_USERNAME, token=request.session[SESSION_APP_GITHUB_OAUTH_TOKEN])
    # Get data
    issue_items = jsonify(github.get(api_repo_issues).json())

    #Check if Request got no error
    if issue_items:
        ln = lambda x: operator.getitem(x, 'number')
        issue_items = sorted(issue_items, key=ln)

        #Get data from issue_items
        for item in issue_items:
            my_dic = {}
            my_dic['action'] = item['title']
            my_dic['description'] = item['body']
            my_dic['number'] = item['number']
            my_dic['status'] = item['state']

            # See if Assigned
            if item['assignee']:
                my_dic['assigned_to'] = item['assignee']['login']
            else:
                my_dic['assigned_to'] = ""
            my_dic['name'] = ""
            my_dic['priority'] = ""
            my_dic['category'] = ""

            #See if any Labels
            if item['labels']:
                for label in item['labels']:

                    #Check for ":"
                    if label['name'][1:2] == ":":
                        if label['name'][0:1] == "C":
                            my_dic['name'] = label['name'][3:]
                        if label['name'][0:1] == "P":
                            my_dic['priority'] = label['name'][3:]
                    else:
                        my_dic['category'] = label['name']
            my_dic['comments'] = ""

            #Check if comments
            if item['comments']:

                # Get Comments
                get_comments = requests.get(item['comments_url'])
                if (get_comments.ok):
                    comments_items = json.loads(get_comments.text or get_comments.content)
                    if comments_items:
                        all_comments = ""
                        for comment in comments_items:
                            all_comments += comment['body']
                        my_dic['comments'] = all_comments
            issue_list.append(my_dic)
    else:
        error = "Request error for {0}".format(api_repo_issues)
    t = loader.get_template('Issues/view_issues_1.html')
    c = Context({'error': error,
                 'issue_list': issue_list,
                 'GITHUB_ORG_REPO_NAME': api_repo_name,
    })
    return HttpResponse(t.render(c))


# This View is used to add a new Issue and use the GitHub Oauth function (Right Method)
def add_issue_2(request, repo):
    # Security check if you have valid Token
    try:
        if not request.session[SESSION_VALIDATED] == "Validated":
            return HttpResponseRedirect(reverse('index_page'))
    except:
        return HttpResponseRedirect(reverse('index_page'))

    api_repo_issues = None
    api_repo_name = ""
    # Get selected Repo
    if repo == GITHUB_ORG_REPO_NAME_WASF:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_WASF
        api_repo_labels = GITHUB_ORG_API_REPO_LABELS_WASF
        api_repo_name = GITHUB_ORG_REPO_NAME_WASF
    elif repo == GITHUB_ORG_REPO_NAME_SFT:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_SFT
        api_repo_labels = GITHUB_ORG_API_REPO_LABELS_SFT
        api_repo_name = GITHUB_ORG_REPO_NAME_SFT
    else:
        return HttpResponseRedirect(reverse('index_page'))

    # Set Auth
    github = OAuth2Session(GITHUB_APP_USERNAME, token=request.session[SESSION_APP_GITHUB_OAUTH_TOKEN])
    # Get data from GitHub
    label_items = jsonify(github.get(api_repo_labels).json())

    #Create list for dropdown
    list_names = []
    list_priority = []
    list_category = []

    if label_items:
        #Get data from issue_items
        for item in label_items:
            #Check for ":"
            if item['name'][1:2] == ":":
                if item['name'][0:1] == "C":
                    client_name = item['name'][3:]
                    var_list = (item['name'], client_name)
                    list_names.append(var_list)
                if item['name'][0:1] == "P":
                    priority_name = item['name'][3:]
                    var_list = (item['name'], priority_name)
                    list_priority.append(var_list)
            else:
                category_name = item['name']
                var_list = (item['name'], category_name)
                list_category.append(var_list)

    error = None
    send_status = None
    form_name = "add_issue_2"
    if request.method == 'POST':
        form = AddIssueForm(request.POST, list_names=list_names, list_priority=list_priority, list_category=list_category)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            action = form.cleaned_data.get('action')
            description = form.cleaned_data.get('description')
            priority = form.cleaned_data.get('priority')
            category = form.cleaned_data.get('category')

            # Build List for Labels
            my_list = [category, name, priority]

            # Build Dic to send
            issue_dic = {}
            issue_dic['title'] = action
            issue_dic['body'] = description
            issue_dic['labels'] = my_list

            body = json.dumps(issue_dic)
            #body = issue_dic

            # Set send data to GitHub
            post_request = github.post(url=api_repo_issues, data=body)

            # Check Send Status
            if post_request.status_code == 201:
                send_status = "Successfully created Issue {0}".format(action)
            elif post_request.status_code == 404:
                error = "Don have access to Write to Repo: {0}".format(api_repo_name)
            else:
                error = "Could not create Issue {0}: {1}".format(action, post_request.content)

            return render_to_response('Issues/add_issue.html',
                                      {'form': form,
                                       'error': error,
                                       'send_status':send_status,
                                       'form_name': form_name,
                                       'GITHUB_ORG_REPO_NAME':api_repo_name },
                                      context_instance=RequestContext(request))
        else:
            error = "You didn't fill in all the required Field 'Action'"
    else:
        form = AddIssueForm(list_names=list_names, list_priority=list_priority, list_category=list_category)
    return render_to_response('Issues/add_issue.html',
                              {'form': form,
                               'error': error,
                               'send_status':send_status,
                               'form_name': form_name,
                               'GITHUB_ORG_REPO_NAME':api_repo_name },
                              context_instance=RequestContext(request))






# Not used views:
# This View is Display the list of Issues (All the processing happen in the Template - Not used)
def view_issues_2(request, repo):
    # Security check if you have valid Token
    try:
        if not request.session[SESSION_VALIDATED] == "Validated":
            return HttpResponseRedirect(reverse('index_page'))
    except:
        return HttpResponseRedirect(reverse('index_page'))

    api_repo_issues = None
    api_repo_name = ""
    # Get selected Repo
    if repo == GITHUB_ORG_REPO_NAME_WASF:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_WASF
        api_repo_name = GITHUB_ORG_REPO_NAME_WASF
    elif repo == GITHUB_ORG_REPO_NAME_SFT:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_SFT
        api_repo_name = GITHUB_ORG_REPO_NAME_SFT
    else:
        return HttpResponseRedirect(reverse('index_page'))

    error = None
    issue_items = None

    # Set Auth
    github = OAuth2Session(GITHUB_APP_USERNAME, token=request.session[SESSION_APP_GITHUB_OAUTH_TOKEN])
    # Get data
    issue_items = jsonify(github.get(api_repo_issues).json())

    # Check if Request got no error
    # Sort by Number
    if issue_items:
        ln = lambda x: operator.getitem(x, 'number')
        issue_items = sorted(issue_items, key=ln)
    else:
        error = "Request error for {0}".format(api_repo_issues)
    t = loader.get_template('Issues/view_issues_2.html')
    c = Context({'error': error,
                 'issue_items': issue_items,
                 'GITHUB_ORG_REPO_NAME': api_repo_name,
    })
    return HttpResponse(t.render(c))


# This View is used to add a new Issue and use the GitHub User and Password, but will not use it (Wrong Method - Not used)
def add_issue_1(request, repo):
    # Security check if you have valid Token
    try:
        if not request.session[SESSION_VALIDATED] == "Validated":
            return HttpResponseRedirect(reverse('index_page'))
    except:
        return HttpResponseRedirect(reverse('index_page'))

    api_repo_issues = None
    api_repo_name = ""
    # Get selected Repo
    if repo == GITHUB_ORG_REPO_NAME_WASF:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_WASF
        api_repo_name = GITHUB_ORG_REPO_NAME_WASF
    elif repo == GITHUB_ORG_REPO_NAME_SFT:
        api_repo_issues = GITHUB_ORG_API_REPO_ISSUES_SFT
        api_repo_name = GITHUB_ORG_REPO_NAME_SFT
    else:
        return HttpResponseRedirect(reverse('index_page'))

    error = None
    send_status = None
    form_name = "add_issue_1"
    if request.method == 'POST':
        form = AddIssueForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            action = form.cleaned_data.get('action')
            description = form.cleaned_data.get('description')
            priority = form.cleaned_data.get('priority')
            category = form.cleaned_data.get('category')

            # Build List for Labels
            my_list = [category, name, priority]

            # Build Dic to send
            issue_dic = {}
            issue_dic['title'] = action
            issue_dic['body'] = description
            issue_dic['labels'] = my_list

            # Set Auth
            auth = HTTPBasicAuth(GITHUB_USERNAME, GITHUB_PASSWORD)
            body = json.dumps(issue_dic)

            # POST data to Repo
            post_request = requests.post(url=api_repo_issues, auth=auth, data=body)

            # Check Send Status
            if post_request.status_code == 201:
                send_status = "Successfully created Issue {0}".format(action)
            elif post_request.status_code == 404:
                error = "Don have access to Write to Repo: {0}".format(api_repo_name)
            else:
                error = "Could not create Issue {0}: {1}".format(action, post_request.content)

            return render_to_response('Issues/add_issue.html',
                                      {'form': form,
                                       'error': error,
                                       'send_status':send_status,
                                       'form_name': form_name,
                                       'GITHUB_ORG_REPO_NAME':api_repo_name },
                                      context_instance=RequestContext(request))
        else:
            error = "You didn't fill in all the required Field 'Action'"
    else:
        form = AddIssueForm()
    return render_to_response('Issues/add_issue.html',
                              {'form': form,
                               'error': error,
                               'send_status':send_status,
                               'form_name': form_name,
                               'GITHUB_ORG_REPO_NAME':api_repo_name },
                              context_instance=RequestContext(request))

