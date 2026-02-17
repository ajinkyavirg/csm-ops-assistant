# Server Management Operations Guide

## Common Alerts and Resolutions

### Alert: Filesystem Getting Full

**Example:** "Filesystem getting full: / on host ccd13vXXX.s4.sap.corp used for IBP RXX"

**Severity:** Depends on usage level
- 85-90%: P3 (warning)
- 90-95%: P2 (urgent)
- >95%: P1 (critical - risk of system crash)

**Immediate Actions:**
1. Identify large files/directories:
```bash
   df -h /
   du -sh /* | sort -hr | head -20
   find / -type f -size +1G 2>/dev/null
```

2. Quick cleanup targets:
   - `/tmp` - Temporary files older than 7 days
   - `/var/log` - Old log files (compress or delete)
   - `/var/crash` - Core dump files
   - `/home/*/.cache` - User cache directories
   - Package manager cache: `yum clean all` or `apt clean`

3. SAP-specific cleanup:
   - HANA trace files: `/usr/sap/<SID>/HDB*/*/trace/*.trc.*`
   - SAP work files: `/usr/sap/<SID>/*/work/*.old`
   - ABAP dumps: Clean via `ST22` transaction
   - Transport files: `/usr/sap/trans/` (archive old data)

**Long-term Resolution:**
- Implement log rotation policy
- Schedule automated cleanup jobs
- Monitor disk growth trends (alert at 75%)
- Expand filesystem if legitimate growth

**SLA:** Based on severity (P1/P2/P3)

---

### Alert: Load Balancer Degraded

**Symptoms:**
- Load balancer health check failing
- Backend servers not receiving traffic
- Users experiencing intermittent connectivity

**Troubleshooting Steps:**
1. Check load balancer status in cloud portal (Azure/AWS)
2. Verify backend server health:
```bash
   curl -I http://backend-server:port/health
   systemctl status <service>
```
3. Review load balancer logs for errors
4. Check backend server resources (CPU, memory, disk)
5. Validate firewall rules (NSG/Security Groups)

**Common Root Causes:**
- Backend server(s) down or unhealthy
- Health check endpoint misconfigured
- SSL certificate expired on backend
- Network path issues between LB and backend
- Backend overwhelmed (all servers at capacity)

**Resolution:**
- Restart failed backend servers
- Fix health check endpoint (return 200 OK)
- Renew SSL certificates
- Remove unhealthy backends from rotation
- Scale out additional backend servers

**SLA:** P1 - 15 minutes (affects all users)

---

### Alert: Host Unreachable

**Example:** "host unreachable: ccd01XXXX.s4.sap.corp"

**Troubleshooting Steps:**
1. Ping test from monitoring server:
```bash
   ping -c 4 ccd01XXXX.s4.sap.corp
   traceroute ccd01XXXX.s4.sap.corp
```

2. Check if host is powered on (cloud console or datacenter)

3. Verify network configuration on host (if accessible via console):
```bash
   ip addr show
   ip route show
   systemctl status NetworkManager
```

4. Check firewall/security groups blocking ICMP

5. Review recent changes (deployment, network maintenance)

**Common Root Causes:**
- Server powered off or crashed
- Network interface down
- IP address conflict or misconfiguration
- Firewall blocking all traffic
- Cable/switch port failure (physical)

**Resolution:**
- Power on server if shutdown
- Restart network service: `systemctl restart network`
- Fix IP configuration: `/etc/sysconfig/network-scripts/ifcfg-eth0`
- Disable firewall temporarily to test: `systemctl stop firewalld`
- Engage network team if switching issue

**SLA:** P1 - 15 minutes

---

### Alert: No Metric from Host

**Example:** "No metric from host: ccd01XXXX.s4.sap.corp"

**Troubleshooting Steps:**
1. Verify host is reachable: `ping ccd01XXXX`
2. Check monitoring agent status:
```bash
   systemctl status telegraf  # or monitoring agent name
   ps aux | grep -i monitor
```
3. Review agent logs: `/var/log/telegraf/` or `/var/log/monitoring/`
4. Test agent connectivity to monitoring server
5. Verify agent configuration file

**Common Root Causes:**
- Monitoring agent stopped or crashed
- Network connectivity issue to metrics collector
- Agent configuration error (wrong endpoint)
- Disk full preventing agent from writing metrics
- High load causing agent timeout

**Resolution:**
- Restart monitoring agent: `systemctl restart telegraf`
- Fix configuration: `/etc/telegraf/telegraf.conf`
- Clear disk space if full (see filesystem alert above)
- Verify network path to monitoring server
- Increase agent timeout if system is slow

**SLA:** P3 - 4 hours (monitoring gap, not service impact)

---

### Alert: Server Rebooted (Unexpected)

**Symptoms:**
- Server uptime counter reset
- Alert "Host rebooted at [timestamp]"
- Services down after reboot

**Investigation Steps:**
1. Check reboot reason:
```bash
   last reboot
   journalctl -b -1  # logs from previous boot
   dmesg | grep -i panic
```

2. Review system logs for crash indicators:
```bash
   grep -i "kernel panic" /var/log/messages
   grep -i "out of memory" /var/log/messages
```

3. Check for scheduled maintenance (was it planned?)

4. Review monitoring for pre-reboot indicators:
   - Memory exhaustion (OOM killer)
   - Kernel panic
   - Hardware failure
   - Manual reboot command

**Common Root Causes:**
- Out of Memory (OOM killer rebooted system)
- Kernel panic (driver or hardware issue)
- Power failure (UPS not configured)
- Scheduled patching (forgotten window)
- Manual reboot without communication

**Post-Reboot Actions:**
1. Verify all critical services started:
```bash
   systemctl list-units --state=failed
```
2. Check SAP/HANA status (if SAP server)
3. Validate application functionality
4. Review logs for startup errors

**Resolution:**
- If OOM: Increase memory or tune applications
- If kernel panic: Update kernel/drivers, check hardware
- If power: Configure UPS and auto-start services
- If manual: Improve change management process

**SLA:** P1 - 15 minutes (immediate recovery verification)

---

### Alert: Multiple Hosts in Maintenance Longer Than 7 Hours

**Symptoms:**
- Hosts showing "maintenance mode" status for extended period
- Capacity reduced (fewer servers handling load)
- Risk of overload on remaining servers

**Troubleshooting Steps:**
1. Check maintenance work order status
2. Verify if maintenance completed but status not updated
3. Contact team responsible for maintenance
4. Review change ticket for planned duration

**Common Root Causes:**
- Maintenance completed but forgot to exit maintenance mode
- Maintenance extended due to complications (change freeze)
- Automation failure (exit script didn't run)
- Patching took longer than planned

**Resolution:**
- Exit maintenance mode manually if work completed:
```bash
  # Command depends on monitoring tool
  # E.g., Nagios: acknowledge alert and disable
```
- Update change ticket with actual completion time
- Communicate status to stakeholders
- Investigate why maintenance exceeded window

**SLA:** P2 - 1 hour (capacity risk)

---

## Server Management Best Practices

### Change Management
- All reboots/maintenance require approved change ticket
- Communicate maintenance windows 48 hours in advance
- Use maintenance mode feature to suppress alerts
- Document actual vs. planned duration

### Monitoring Standards
- Filesystem alert thresholds: 75% warning, 85% critical
- CPU alert: >80% for 10 minutes
- Memory alert: Swap usage >50%
- Network: Packet loss >1%
- Uptime: Any unexpected reboot triggers P1 alert

### Escalation Path
1. **L1 Ops** → Initial triage (15 min)
2. **L2 Infrastructure** → Server/network troubleshooting (30 min)
3. **L3 Vendor** → Hardware replacement, advanced diagnostics (1 hour)
4. **Management** → If SLA breach imminent