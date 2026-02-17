# S/4HANA Troubleshooting Guide

## Common Alerts and Resolutions

### Alert: CPU Utilization Above 90% on Host

**Example:** "CPU Utilization is above 90% on host azr0900xxxx used for S4P"

**Symptoms:**
- System extremely slow or unresponsive
- Dialog response time >2 seconds
- Background jobs queuing up

**Troubleshooting Steps:**
1. Identify top CPU consumers: `top` or `ps aux --sort=-%cpu | head -20`
2. Check SAP work processes: `SM50` (ABAP processes) or `SM66` (system-wide)
3. Review expensive SQL: `ST04` (Database Performance Monitor)
4. Check for runaway batch jobs: `SM37` (Job Overview)
5. Analyze ABAP dumps: `ST22` (Runtime Errors)

**Common Root Causes:**
- Long-running background job (e.g., mass data update)
- Inefficient custom ABAP code
- Database statistics outdated (poor query plans)
- Memory swapping due to undersized RAM
- HANA indexserver high CPU

**Resolution:**
- Kill/postpone non-critical background jobs
- Optimize expensive SQL queries (add indexes)
- Update database statistics: `DB02` → Update Statistics
- Restart SAP to clear memory leaks
- Scale up host resources if sustained legitimate load

**SLA:** P2 - 1 hour

---

### Alert: Swap Space Usage Above 85%

**Symptoms:**
- Severe performance degradation
- System freezing or hanging
- SAP work processes going into PRIV mode

**Troubleshooting Steps:**
1. Check memory usage: `free -h` and `vmstat 1`
2. Identify memory-consuming processes: `ps aux --sort=-%mem | head -20`
3. Review SAP memory configuration: RZ10 parameters
4. Check for memory leaks in SAP processes
5. Verify HANA global allocation limit

**Common Root Causes:**
- Insufficient physical RAM for workload
- Memory leak in SAP application or HANA
- Too many concurrent users beyond capacity
- Large report or data extraction consuming memory

**Resolution:**
- Clear SAP buffers: `/$SYNC` in transaction field (emergency only)
- Restart SAP instance to release memory
- Increase physical RAM if chronic issue
- Tune SAP memory parameters: `em/initial_size_MB`, `ztta/roll_extension`
- Kill memory-intensive user sessions

**SLA:** P1 - 15 minutes (risk of system crash)

---

### Alert: ABAP Daemon Framework - 405

**Symptoms:**
- ABAP daemon processes not running
- Background processing affected
- Scheduled tasks not executing

**Troubleshooting Steps:**
1. Check daemon manager status: Transaction `SMDAEMON`
2. Review daemon application logs: Transaction `SLG1`
3. Check system log: `SM21` for daemon-related errors
4. Verify RFC connections: `SM59` (daemon uses RFC)
5. Check work process availability: `SM50`

**Common Root Causes:**
- All background work processes busy (no slots available)
- RFC connection failure to local system
- Authorization issues for daemon user
- System resources exhausted (memory/CPU)

**Resolution:**
- Free up background work processes (cancel stuck jobs)
- Restart daemon manager: `SMDAEMON` → Restart
- Check RFC destination "NONE" is configured: `SM59`
- Verify daemon user authorizations: S_ADMI_FCD, S_RFC
- Increase number of background work processes if needed

**SLA:** P2 - 1 hour

---

### Alert: Filesystem Usage Above 90%

**Examples:**
- "Filesystem usage for /hana/backup/ASG is above 90% on host azr0900xxxx"
- "Filesystem usage for /hana/log is above 90%"

**Troubleshooting Steps:**
1. Check disk usage: `df -h` and `du -sh /*`
2. Identify large files: `find /path -type f -size +1G`
3. Review HANA backup catalog: `hdbbackupdiag` or SQL query
4. Check SAP spool/logs: `/usr/sap/<SID>/*/work/`, `/usr/sap/<SID>/*/log/`
5. Check for old HANA trace files: `/usr/sap/<SID>/HDB*/*/trace/`

**Common Root Causes:**
- Old HANA backups not deleted (retention policy not enforced)
- HANA log volume growing (long-running transactions)
- SAP spool files accumulating (print jobs)
- Core dumps from crashed processes

**Resolution for /hana/backup:**
- Delete old backups: Use HANA Cockpit or `hdbbackupdiag --delete`
- Implement backup retention policy (e.g., keep 7 days)
- Move backups to cheaper storage tier

**Resolution for /hana/log:**
- Commit/rollback long transactions
- Archive log backups to /hana/backup
- Increase log volume size if sustained growth

**Resolution for /usr/sap:**
- Clean old work files: `find /usr/sap/*/work -mtime +7 -delete`
- Purge spool files: `RSPO1041` report or manually
- Compress/archive old trace files

**SLA:** P2 - 1 hour (before 100% full = outage)

---

### Alert: Metric Provider Errors During Collection - 104

**Symptoms:**
- Monitoring data gaps in dashboards
- Missing performance metrics
- Alert "Metric collection failed" in monitoring tool

**Troubleshooting Steps:**
1. Check SAP Host Agent: `saphostctrl -function GetComputerSystem`
2. Review metric provider logs: `/usr/sap/hostctrl/exe/sapcontrol.log`
3. Verify connectivity to monitored system
4. Check metric provider configuration: `/usr/sap/hostctrl/exe/host_profile`
5. Test manual metric collection: `sapcontrol -nr <instance> -function GetProcessList`

**Common Root Causes:**
- SAP Host Agent not running
- Network connectivity issue to target system
- Authentication failure (missing credentials)
- Timeout due to slow system response

**Resolution:**
- Restart SAP Host Agent: `saphostexec -restart`
- Verify firewall allows monitoring ports (5XX13, 5XX14)
- Update credentials in monitoring configuration
- Increase timeout values if system genuinely slow

**SLA:** P3 - 4 hours (monitoring issue, not production impact)