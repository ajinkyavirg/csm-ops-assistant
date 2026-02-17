# Incident Response SOP

## Severity Levels

### P1 - Critical
- **Definition**: Complete service outage affecting all users
- **Response Time**: 15 minutes
- **Examples**: CloudERP down, HCM login failures, production database crash
- **Action**: Immediately engage on-call engineer, notify management

### P2 - High
- **Definition**: Major functionality impaired, affecting multiple users
- **Response Time**: 1 hour
- **Examples**: Report generation failing, slow performance, partial feature outage
- **Action**: Assign to specialist team, update stakeholders every 30 minutes

### P3 - Medium
- **Definition**: Minor functionality issue, workaround available
- **Response Time**: 4 hours
- **Examples**: UI glitches, minor data sync delays
- **Action**: Standard troubleshooting, document in AppOps case

### P4 - Low
- **Definition**: Cosmetic issues, feature requests
- **Response Time**: Next business day
- **Examples**: Documentation updates, enhancement requests
- **Action**: Queue for planned maintenance

## Escalation Matrix

1. **L1 Support** → Initial triage (15 min)
2. **L2 Specialist** → Deep troubleshooting (30 min)
3. **L3 Engineering** → Code-level fixes (1 hour)
4. **Management** → Business impact decisions

## Communication Templates

**P1 Notification:**
"CRITICAL INCIDENT: [System] is experiencing complete outage. ETA for resolution: [Time]. War room active. Updates every 15 minutes."

**Resolution Notification:**
"RESOLVED: [System] incident cleared at [Time]. Root cause: [Brief]. Post-mortem scheduled."