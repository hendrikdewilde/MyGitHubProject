from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from MyGitHubProject import settings

urlpatterns = patterns('',
    #Index Page
    url(r'^$', 'MyGitHubProject.views.index', name='index_page'),

    #Credentials Validate / Exit Page
    url(r'^Auth/$', 'MyGitHubProject.views.auth', name='auth_page'),
    url(r'^CredentialsValidate/$', 'MyGitHubProject.views.credentials_validate', name='credentials_validate_page'),
    url(r'^Exit/$', 'MyGitHubProject.views.exit', name='exit_page'),

    #Main Page
    url(r'^MyGitHubProject/$', 'MyGitHubProject.views.mydashboard', name='dashboard_page'),

    #Issues URLS
    (r'^MyGitHubProject/Issues/', include('MyGitHubProject.Issues.urls')),

) + static(settings.STATIC_URL, document_root=settings.MY_STATIC_ROOT)
