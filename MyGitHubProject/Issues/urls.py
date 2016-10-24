from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Display Issues - View Orientated
    url(r'^(?P<repo>[a-z,A-Z,0-9, ,_,&,.,-]+)/issues_1/$', 'MyGitHubProject.Issues.views.view_issues_1', name='view_issues_page_1'),
    # Display Issues - Template Orientated
    url(r'^(?P<repo>[a-z,A-Z,0-9, ,_,&,.,-]+)/issues_2/$', 'MyGitHubProject.Issues.views.view_issues_2', name='view_issues_page_2'),
    # Add Issues
    # Using Username & Password
    url(r'^(?P<repo>[a-z,A-Z,0-9, ,_,&,.,-]+)/add_issues_1/$', 'MyGitHubProject.Issues.views.add_issue_1', name='add_issue_page_1'),
    # Using OAuth
    url(r'^(?P<repo>[a-z,A-Z,0-9, ,_,&,.,-]+)/add_issue_2/$', 'MyGitHubProject.Issues.views.add_issue_2', name='add_issue_page_2'),
)