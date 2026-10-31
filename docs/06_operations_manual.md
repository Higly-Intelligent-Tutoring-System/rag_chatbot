# 🧭 Operator’s Manual

This operator’s manual provides an overview of how to run and maintain the application. It describes the Docker and Compose setup, how to add services, how TLS certificates are handled, and the project’s deployment considerations. Production deployment may require additional configuration for your environment; Ansible support for provisioning a generic VPS is still in progress.

## 🐳 Containerization

Docker-related specifications are located in the `docker/` directory. Docker Compose files in the repository root orchestrate the services and define how they run together.

### Adding a service

1. Add the service definition to the appropriate Compose file in the repository root.
2. If the service needs custom dependencies, runtime settings, or other configuration, create a dedicated Dockerfile for it.
3. Update the Compose service to build from that Dockerfile, then test that the service starts and works with the rest of the stack.

## 🧪 Why the staging environment has five chatbot versions

The five chatbot versions in the staging environment were created for experiments managed by UNICAM to validate the performance of the tools. The user interface was updated to route requests to each version, allowing them to be accessed separately during testing.

## 🔒 Obtaining TLS certificates

A **fully qualified domain name (FQDN)** is required for the deployment’s public domain. Caddy is used to obtain and manage TLS certificates for the configured FQDN, including renewing managed certificates. For public domains, make sure the domain is configured correctly and that Caddy can complete the required validation. <citation src="6"></citation>

See the [Caddy automatic HTTPS documentation](https://caddyserver.com/docs/automatic-https) for details.

## 🚀 Production deployment

Production deployment is not covered here because the required setup depends on the specific use case and infrastructure.

If you fork the repository, create an appropriate deployment workflow in the `.github/` directory. Configure the workflow to use the required secrets and environment variables, then create and push a version tag. For example:

```bash
git tag v1.0.0 && git push origin v1.0.0
```

Make sure the tag format matches the release conventions and triggers expected by your workflow.

## ⚙️ Ansible configuration

An Ansible configuration for setting up a generic VPS is still a work in progress. It will be documented here when it is ready.

## ☁️ rclone configuration

To replicate the automated remote-backup solution, install and configure **rclone** for the remote storage provider you plan to use. The required setup depends on that provider; follow the [official rclone documentation](https://rclone.org/docs/) for installation, remote configuration, and usage.

## 🧪 Production schema for validation

The `docker-compose.prod.yml` file was build to replicate the structure of the actual system used to validate the chatbot's performance.
Here you can see how it was organised.

![VPS diagram](./assets/HITS-VPS.png)