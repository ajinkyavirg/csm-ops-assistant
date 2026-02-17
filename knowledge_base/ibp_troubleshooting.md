# IBP (Integrated Business Planning) Troubleshooting Guide

## Common Alerts and Resolutions

### Alert: SID System Not Accessible

**Symptoms:**
- Users cannot access IBP system
- Connection timeout errors
- System ID not responding to health checks

**Troubleshooting Steps:**
1. Check system status: `sapcontrol -nr <instance> -function GetSystemInstanceList`
2. Verify all IBP processes running (check dispatcher, server, gateway)
3. Review system logs: `/usr/sap/<SID>/*/work/dev_*`
4. Check network connectivity to SID hostname
5. Validate database connection (HANA must be running)

**Common Root Causes:**
- HANA database not started (check HDB daemon)
- Network firewall blocking ports (33XX, 44XX, 80XX)
- SAP processes crashed (check for core dumps)
- Insufficient memory causing process termination

**Resolution:**
- Start HANA: `HDB start` as <sid>adm
- Restart SAP: `sapcontrol -nr <instance> -function StartSystem`
- Clear memory: Stop non-critical processes, restart system
- Verify ports open: `netstat -tuln | grep 33XX`

**SLA:** P1 - 15 minutes (production outage)

---

### Alert: URL Not Available / URL Check Failed

**Symptoms:**
- IBP web interface returns 502/503/504 errors
- URL health check monitoring alert triggered
- Users see "Service Unavailable" message

**Troubleshooting Steps:**
1. Check web dispatcher status: `sapcontrol -nr <WD instance> -function GetProcessList`
2. Verify backend server connectivity from web dispatcher
3. Review ICM logs: `/usr/sap/<SID>/*/work/dev_icm`
4. Check SSL certificate validity (if HTTPS)
5. Validate DNS resolution for URL

**Common Root Causes:**
- Web dispatcher stopped or hung
- Backend IBP server not registered with web dispatcher
- SSL certificate expired
- Network routing issue between dispatcher and backend

**Resolution:**
- Restart web dispatcher: `sapcontrol -nr <WD instance> -function RestartService`
- Re-register backend: Check ICM connection table
- Renew SSL certificate if expired
- Verify network routes: `traceroute <backend-host>`

**SLA:** P1 - 15 minutes

---

### Alert: HDB_HOST_STATUS_ALERT_INST

**Symptoms:**
- HANA database host health alert
- Database performance degradation
- Potential database unavailability

**Troubleshooting Steps:**
1. Check HANA system status: `HDB info` as <sid>adm
2. Review HANA host agent logs: `/usr/sap/<SID>/HDB*/*/trace/`
3. Check disk space on HANA volumes (data, log, backup)
4. Verify HANA services running: `sapcontrol -nr <instance> -function GetProcessList`
5. Review HANA alerts in SAP HANA Studio/Cockpit

**Common Root Causes:**
- Disk space full on /hana/data or /hana/log
- Memory pressure (OOM - Out of Memory)
- Network connectivity issues between HANA nodes (scale-out)
- Savepoint operation delayed/failed

**Resolution:**
- Free up disk space: Clean old backups, archive logs
- Restart HANA if memory leak: `HDB stop && HDB start`
- Check HANA indexserver memory: Review global allocation limit
- Fix savepoint: `ALTER SYSTEM SAVEPOINT`

**SLA:** P1 - 15 minutes

---

## IBP-Specific Monitoring

### Key Metrics to Monitor
- **URL Availability:** Target 99.9% uptime
- **Response Time:** <3 seconds for web UI
- **HANA Database:** CPU <70%, Memory <85%
- **Concurrent Users:** Monitor against licensed capacity
- **Background Jobs:** Check for stuck planning runs

### Preventive Maintenance
- Weekly HANA backup validation
- Monthly SSL certificate expiry check
- Quarterly HANA statistics update
- Monitor disk growth trends (alert at 75%)