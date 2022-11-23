import os, git
from virtualenv import cli_run

c = get_config()

"""
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_hosts =  ['ldap://ldap.example.com:389']
c.LDAPAuthenticator.bind_user_dn = 'uid=ldapbind,cn=users,dc=ldap,dc=example,dc=com'
c.LDAPAuthenticator.bind_user_password = 'Password'
c.LDAPAuthenticator.user_search_base = 'cn=users,dc=ldap,dc=example,dc=com'
c.LDAPAuthenticator.user_search_filter = '(&(objectClass=posixAccount)(uid={username}))'
c.LDAPAuthenticator.username_pattern = '[a-zA-Z0-9_.][a-zA-Z0-9_.-]{0,252}[a-zA-Z0-9_.$-]?'
c.LDAPAuthenticator.create_user_home_dir = True
c.LDAPAuthenticator.create_user_home_dir_cmd = ['mkhomedir_helper']

c.Authenticator.admin_users = {'admin'}
"""


async def devenv_setup_hook(spawner) -> None:
    user_home_dir = f'/home/{spawner.user.name}'
    username = spawner.user.name
    if not os.path.exists(os.path.join(user_home_dir, 'httpx')):
        git.Repo.clone_from(
            url = 'https://github.com/projectdiscovery/httpx.git',
            to_path = os.path.join(user_home_dir, 'httpx')
        )
        cli_run([f'/home/{username}/httpx/.venv'])
        os.system(f'chown {username}:{username} /home/{username}/httpx/.venv -R')
        
    print(f'hello {username}')

c.LocalProcessSpawner.pre_spawn_hook = devenv_setup_hook
c.LocalProcessSpawner.notebook_dir = '~/httpx'
print('config loaded')