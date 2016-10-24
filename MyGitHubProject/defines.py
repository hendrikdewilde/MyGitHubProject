# Session Defines
SESSION_VALIDATED = 'session_validated'
SESSION_USER_DETAIL = 'session_user_detail'
SESSION_APP_GITHUB_OAUTH_TOKEN = 'session_app_github_oauth_token'

# My Setup
GITHUB_USERNAME = 'swordfishtest'
GITHUB_PASSWORD = 'warr10r'
# My App OAuth
GITHUB_APP_USERNAME = '5261c16c4362adef0b22'
GITHUB_APP_PASSWORD = '5f5c00a765ab1ef75f262a8c23a1978617b8ff94'
GITHUB_APP_NAME_NOTE = "MyGitHubProject"

GITHUB_APP_SCOPE = ['user', 'repo', 'notifications', 'gist']

# My Working Repo Owner
GITHUB_REPO_OWNER_WASF = 'WorkAtSwordfish'
GITHUB_REPO_OWNER_SFT = 'swordfishtest'

# My Working Repo Name
GITHUB_ORG_REPO_NAME_WASF = 'GitIntegration'
GITHUB_ORG_REPO_NAME_SFT = 'MyGitHubProject'

# GITHub Setup
# GITHub OAUTH URL
GITHUB_OAUTH_LOGIN_AUTH = 'https://github.com/login/oauth/authorize'
GITHUB_OAUTH_LOGIN_TOKEN = 'https://github.com/login/oauth/access_token'

# GITHub API URL
GITHUB_API = 'https://api.github.com/'

# My GITHub API URL to my Repo Issues
GITHUB_ORG_API_REPO_ISSUES_WASF = '{0}repos/{1}/{2}/issues'.format(GITHUB_API, GITHUB_REPO_OWNER_WASF, GITHUB_ORG_REPO_NAME_WASF)
GITHUB_ORG_API_REPO_ISSUES_SFT = '{0}repos/{1}/{2}/issues'.format(GITHUB_API, GITHUB_REPO_OWNER_SFT, GITHUB_ORG_REPO_NAME_SFT)

# My GITHub API URL to my Repo labels
GITHUB_ORG_API_REPO_LABELS_WASF = '{0}repos/{1}/{2}/labels'.format(GITHUB_API, GITHUB_REPO_OWNER_WASF, GITHUB_ORG_REPO_NAME_WASF)
GITHUB_ORG_API_REPO_LABELS_SFT = '{0}repos/{1}/{2}/labels'.format(GITHUB_API, GITHUB_REPO_OWNER_SFT, GITHUB_ORG_REPO_NAME_SFT)