# Overview
Vanilla is a powerful open source web-based forum. This charm will deploy
the forum software and connect it to a running MySQL database. This charm
will install the Vanilla files in /var/www/vanilla

# Installation
To deploy this charm you will need at a minimum: a cloud provider,
working Juju installation and a successful bootstrap. Once bootstrapped,
deploy the MySQL charm and then this Vanilla charm:
    juju deploy mysql
    juju deploy vanilla
Add a relation between the two of them:
    juju add-relation mysql vanilla
And finally expose the Vanilla application:
    juju expose vanilla

# Disclaimer
This is not the actual Vanilla charm, but a practice charm created following
the Juju documentation.
