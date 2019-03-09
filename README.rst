
.. image:: https://previews.dropbox.com/p/thumb/AAXEDWXMVglSRpgmrfk3w4dMQ8klNpRBYw_l3M3Qn-umMvrvHsyB7qRyKyF0VW_paZjQengfGpPo35JiMet5pBbNu0sYk8o9woIpA_ENQe8LsG_09P0fTb91zfegPVG2fVCfflKNIqBQXGNs_nEClJQNzbGvu4wh5PKP-wEkoODqOSC4Q2CRifYkX0BVlHqwLZV6kOnvYOK-JJ6vO0K6a01_iJdspGhEafKqkFHODrfqdZ6bKY9D3xlowdKT95AOBOb1JZ0WTcHVBeM63YJyx9sN8fu7qP7ilRj-NUehUsP5EA/p.png?size_mode=5

------------

castic is a minimal web-based monitoring and management tool built on top of 
the non-graphical backup-tool 'restic' (https://github.com/restic/restic).

Documentation_

.. _Documentation: https://github.com/zoerbd/castic/tree/dev/docs

|

Requirements and support
------------------------
Castic is mostly built and tested on CentOS 7, thats why I strongly recommend using a RHEL based distro.
Ubuntu and other distros should also work, but you have to setup some parts by yourself (i.e. mainly webserver infrastructure and package installation).

|

How to build castic
----------------------

1. Clone the repository and cd into it.

     ``git clone https://bitbucket.org/zoerbd/castic``

     ``cd castic``

2. Install the package with: 

     ``pip install -e .``

3. Recommended: I strongly recommend using the interactive installer, by running this command: 

        ``src/bin/installme.py``

If you got another distro than CentOS you will have to setup some parts by yourself, so take a look at the docs folder for more details.

---------