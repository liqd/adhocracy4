#!/bin/sh

set -e -v

if [ -n ${TRAVIS_SSH_SECRET} ]; then
    SSH_ID_ARG="-i ${HOME}/id_rsa_TRAVIS"
    cat <<EOF | openssl enc -d -pass env:TRAVIS_SSH_SECRET -aes256 -a -out ~/id_rsa
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
XLLfeOmGX6d5KL/v6FVBTg==
EOF
    chmod 600 ~/id_rsa_TRAVIS
fi

ssh -p 22036 ${SSH_ID_ARG} -oStrictHostKeyChecking=no build@benhabib.liqd.net deploy meinberlin master
