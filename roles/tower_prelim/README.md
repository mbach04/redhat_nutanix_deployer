## Required for this role code to function properly
- This role expects that you already have a bundled tarball on the host on which you'll run the code (in /tmp)
- Ensure that you have your tower nodes in an inventory group named 'tower_nodes' and db in 'db_nodes'
- cluster defaults to 'False'.  Set to 'True' to create a Tower Cluster (otherwise, the installer assumes allinone)
- prudent to change the passwords in defaults/main.yml
