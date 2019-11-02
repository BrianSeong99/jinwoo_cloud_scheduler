"""Configuration file for dev"""
import os

KUBERNETES_CLUSTER_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNmQ4MnciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjY1NjNjMTc1LWViNDgtMTFlOS1hYzA2LTUyMGMzOGUyZjVlNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.UTS6FqgyHxKFT7nWbxzbi3qXf8Xx6zIYg-TXJItpX_u4lPFQB6DwlgBMA16Xv3uImhDK857vfh_jyulqTlFZQTx47T3CzZ0NMxdTPYV6jPqdgxOXLixFWmfkVzsup7HhcTjXo67crxTu5pXlUqfDHmlub_JRdkLK5eHvEBU7-ArNWS-2iaeF-zifwih7A52qfxt-87PkFO76c3GetJ9b9RPu5mtVyMA7CaQoj2MZybKiTfq1C_mLgXsCHNwRpubJSBLdNMI9E6QDG99zV2asOMxMoNClrCDNfD97a702_2d2P-KU11yvM37rzMvaJptRFHuXtO_2ow6s9byez1XSGw"
KUBERNETES_API_SERVER_URL = "https://152.136.222.117:30000"
KUBERNETES_NAMESPACE = "cloud-scheduler"
DEBUG = True
SECRET_KEY = '(t@s1tb(r%^7q0s6^$%vfzb!)5(=ywp3(%vu0d0gwidsdizkav'
CLOUD_SCHEDULER_API_SERVER_BASE_URL = 'http://127.0.0.1:8000/'  # for handle redirects

USER_TOKEN_EXPIRE_TIME = 900  # in seconds

DOCKER_ADDRESS = "https://registry.dropthu.online:30001"
REGISTRY_ADDRESS = "registry.dropthu.online:30443"
REGISTRY_V2_API_ADDRESS = "https://registry.dropthu.online:30443/v2"

DAEMON_WORKERS = 2
TASK_DISPATCH_WORKERS = 4
IPC_PORT = 50000

CEPH_STORAGE_CLASS_NAME = "csi-cephfs"
GLOBAL_TASK_TIME_LIMIT = 3600  # one hour
USER_SPACE_POD_TIMEOUT = 300  # 5 minutes

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3'),
    }
}

USER_WEBSHELL_DOCKER_IMAGE = "registry.dropthu.online:30443/ubuntu:19.10"
USER_VNC_DOCKER_IMAGE = "registry.dropthu.online:30443/ubuntu:19.10"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.126.com'   # SMTP server
EMAIL_HOST_USER = 'cloud_scheduler@126.com'    # username and domain
EMAIL_HOST_PASSWORD = '1gZIrMq5onyli9HN'    # password
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
