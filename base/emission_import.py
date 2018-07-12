import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
hostname = '139.191.148.169'

try:
    ssh.connect('.'.join([self.name, self.domain]),
                username=self.username, password=self.password)
    stdin, stdout, stderr = ssh.exec_command("ps aux | grep Xvnc | wc -l")
except:
    pass

# try:
#     host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
# except IOError:
#     try:
#         # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
#         host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
#     except IOError:
#         print '*** Unable to open host keys file'
#         host_keys = {}
#
# if host_keys.has_key(hostname):
#     hostkeytype = host_keys[hostname].keys()[0]
#     hostkey = host_keys[hostname][hostkeytype]
#     print 'Using host key of type %s' % hostkeytype
#
#
# # now, connect and use paramiko Transport to negotiate SSH2 across the connection
# try:
#     t = paramiko.Transport((hostname, port))
#     t.connect(username='lanalfa', password='Albertone_2017_4', hostkey=hostkey)
#     sftp = paramiko.SFTPClient.from_transport(t)
#
#     # dirlist on remote host
#     dirlist = sftp.listdir('.')
#     print "Dirlist:", dirlist
# except:
#     pass
