#!/bin/sh

DEFAULT_NTP="time.cloudflare.com,162.159.200.123"
CHRONY_CONF_FILE="/etc/chrony/chrony.conf"

if [ -d /run/chrony ]; then
  chown -R chrony:chrony /run/chrony
  chmod o-rx /run/chrony
  
  rm -f /var/run/chrony/chronyd.pid
fi

if [ -d /var/lib/chrony ]; then
  chown -R chrony:chrony /var/lib/chrony
fi

if [ -z "${NTP_SERVERS}" ]; then
  NTP_SERVERS="${DEFAULT_NTP}"
fi

# chrony log levels: 0 (informational), 1 (warning), 2 (non-fatal error) and 3 (fatal error)
if [ -z "${LOG_LEVEL}" ]; then
  LOG_LEVEL=0
else
  if [ "${LOG_LEVEL}" -gt 3 ]; then
    
    LOG_LEVEL=0
  fi
fi

IFS=","
for N in $NTP_SERVERS; do
  
  N_CLEANED=${N//\"}

  if [[ "${N_CLEANED}" == *"127\."* ]]; then
    echo "server "${N_CLEANED} >> ${CHRONY_CONF_FILE}
    echo "local stratum 10"    >> ${CHRONY_CONF_FILE}
  else
    echo "server "${N_CLEANED}" iburst" >> ${CHRONY_CONF_FILE}
  fi
done

{
  echo
  echo "driftfile /var/lib/chrony/chrony.drift"
  echo "makestep 0.1 3"
  echo "rtcsync"
  echo
  echo "allow all"
} >> ${CHRONY_CONF_FILE}

exec /usr/sbin/chronyd -u chrony -d -x -L ${LOG_LEVEL}