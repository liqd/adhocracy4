#!/bin/sh

set -e -v

if [ -n ${TRAVIS_SSH_SECRET} ]; then
    SSH_ID_ARG="-i ${HOME}/id_rsa"
    cat <<EOF | openssl enc -d -aes-256-cbc -pbkdf2 -pass env:TRAVIS_SSH_SECRET -a -out ~/id_rsa
U2FsdGVkX18u2lLhir31yxnC61lZhVioi12A6W9gjJhjiyETLVQ84/haZhspgDzt
HFk9V+9JiJGWakrpbH5GexMQDvgzUm4tntw2xU/2LoDBb0iP3HOOYu44Y0VGsTU6
Wf+vBBE5fOuTpAE0XRla9gEeK9pImhxDDybpgLoPI2x8EqsCaizM/7BtuwfsF5It
juZB/z3wokkhe0AsQpOk3FPOmzMcW3ILhYHquvzeU4G79muGYNobhan+pv6uvtER
n7NrFa/oKopa4nJC9Q3fP+itJmTVBaEFuH5vJQWZtSsNvMOPCNq6eXevBInc8aca
a+6wmHVAp3YI5eWPqmO34c3eo5JSfwJDiJ9tRP6q9w/uR3lkvPq4FVef2ccDfWHe
jEzDMGdjZJIX0X3WZVQYSnjY3dB4vd8ptHJkdDP2Oj8JTF39CRkYWmNWB68Xa6sf
7vZ1Q3o3njRGe6R5LrMOQHLR4eMv9f8SjXl8Hifmbk/vqXd9aZD3n75f6ggQR+if
ywfoxlB+aACB3xQM40xY6LHXeE8YbO1hbpAqF23T72yoLTrPjQ0xi9SvP8oNmsNh
u9yspubt1Jha/GR03caafw==
EOF
    chmod 600 ~/id_rsa
fi

ssh ${SSH_ID_ARG} -oStrictHostKeyChecking=no build@build.liqd.net deploy meinberlin main
