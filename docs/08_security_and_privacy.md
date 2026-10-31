# 🔐 Security and Privacy

This document summarizes the security measures and privacy design of the HITS chatbot deployment. It also distinguishes between controls that are in place and planned automation.

## 🛡️ Security

The deployment uses several layers of protection:

- **API authentication:** API authentication can be enabled to restrict access to protected endpoints. Configure the relevant credentials and secrets for the deployment, and keep them out of version control.
- **Containerization:** The application services run in containers, with their configuration managed through Docker and Docker Compose.
- **Reverse proxy and TLS:** A reverse proxy handles HTTPS connections using a TLS certificate issued by Let’s Encrypt.
- **Database backups:** Database backups are created periodically, compressed with `gzip`, encrypted with `age`, and transferred or stored using `rclone`. Keep encryption keys secure and separate from the backup files.
- **Reproducible setup with Ansible:** Ansible automation for setting up a generic VPS was expored but is not ready yet. It will be documented when available to help make deployment steps more repeatable for future adoptions, even if it's not mandatory.

## 🕵️ Privacy

The telemetry server collects chatbot conversations for project purposes. In line with the project’s privacy requirements, the telemetry system is **NOT** able to correlate a user’s browser with the ID of a conversation.

Here, “anonymous telemetry” describes this lack of correlation; it does not mean that conversation content is not collected.