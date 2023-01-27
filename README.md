# FIM (File Integrity Monitoring)

Currently developing a File Integrity Monitoring (FIM) tool using Python, to monitor unauthorized modifications to sensitive files in Linux systems

### Capabilities:
- Tracks and alerts admins of unathorized changes to sensitive files. Changes include file deletion, new file addition and file updation
  - Utilized the SHA-256 algorithm and the compare-by-hash technique to detect variations from a predefined baseline, and provided the option for the administrator to create or reset the baseline as needed.
- Automation by scheduling daily runs of the tool using cron jobs
- Immediate email notifications through a push-notification API service to notify administrator of any unauthorized changes to files **(development in-progress)**

