#!/bin/sh

target_dir=$(cd $(dirname $0); pwd)
{
echo "[Unit]"
echo "Description = Running Eevee"
echo ""
echo "[Service]"
echo "ExecStart = ${target_dir}/running_eevee.py"
echo "Restart = always"
echo "Type = simple"
echo ""
echo "[Install]"
echo "WantedBy = multi-user.target"
} | tee /etc/systemd/system/eevee.service

systemctl enable eevee
systemctl restart eevee
