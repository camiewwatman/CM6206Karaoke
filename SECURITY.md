# Security Policy

Security is taken seriously in the CM6206 Audio Controller project.

The project interacts with system-level components including systemd, sudo, ALSA, USB/HID devices and GPIO. If you discover a security issue, please report it responsibly rather than publishing details before a fix can be made available.

## Supported Versions

The project is currently under active development.

Security fixes will generally be applied to the latest available release rather than backported to older versions.

| Version | Supported |
| ------- | --------- |
| Latest release | :white_check_mark: |
| Development branch | :white_check_mark: |
| Older releases | :x: |

Users are encouraged to update to the latest version before reporting an issue that may already have been resolved.

## Reporting a Vulnerability

Please do not report security vulnerabilities through a public GitHub Issue.

Instead, use **GitHub Private Vulnerability Reporting** through the repository's **Security** tab:

1. Open the GitHub repository.
2. Select **Security**.
3. Select **Advisories**.
4. Select **Report a vulnerability**.
5. Provide as much information as possible about the issue.

If Private Vulnerability Reporting is not available for the repository, please contact the repository maintainer privately rather than publicly disclosing the vulnerability.

## What to Include

A useful vulnerability report should include:

- A clear description of the vulnerability.
- The affected project version or Git commit.
- Raspberry Pi or other hardware being used.
- Operating system and version.
- Steps required to reproduce the issue.
- Relevant commands, configuration or logs.
- The security impact you believe the issue could have.
- Whether physical or network access is required.
- Any suggested mitigation or fix, if known.

Please remove passwords, credentials, private keys, API tokens and other sensitive information from logs before submitting them.

## Particularly Relevant Security Issues

Reports are especially welcome for issues involving:

- Privilege escalation.
- The `cm6206-web` service account.
- `sudoers` configuration.
- Command injection.
- Flask API input handling.
- Unauthenticated network access.
- systemd service permissions.
- udev rules.
- USB/HID handling.
- `cm6206ctl` execution.
- GPIO integrations.
- Unsafe file permissions.
- Dependency vulnerabilities.
- Installation scripts executing unexpected commands.

## Expected Response

For responsibly disclosed vulnerabilities, the goal is to:

- Acknowledge the report within **7 days**.
- Confirm whether the issue can be reproduced.
- Assess the affected versions and likely impact.
- Develop or coordinate an appropriate fix.
- Provide updates when there is a meaningful change in status.
- Publish a security advisory when appropriate.

Complex vulnerabilities, particularly those involving upstream dependencies or operating-system components, may take longer to resolve.

## Accepted Vulnerabilities

If a report is accepted, the issue may be addressed through one or more of the following:

- A patched release.
- Changes to installation or configuration defaults.
- Updated systemd, sudoers or udev configuration.
- Documentation of a secure configuration or mitigation.
- A GitHub Security Advisory.

Details should remain private until a fix or reasonable mitigation is available.

## Declined Reports

A report may be declined if:

- The issue cannot be reproduced.
- The behaviour is working as documented and does not create a security boundary violation.
- The issue exists entirely within an upstream dependency and is not caused by this project.
- Exploitation requires a user who already has equivalent root-level access.
- The reported version is no longer supported.
- The report concerns expected physical access to the hardware rather than a software security vulnerability.

Upstream vulnerabilities may still result in dependency or documentation changes where appropriate.

## Security Considerations

This project is intended primarily for small, local CM6206 audio-controller deployments.

The web interface should be treated as an administrative interface.

It is strongly recommended that users:

- Run the web service only on a trusted network.
- Do not expose the Flask/Gunicorn service directly to the public Internet.
- Keep Raspberry Pi OS or the chosen Linux distribution updated.
- Keep the project's `sudoers` permissions restricted to the commands required by the controller.
- Do not run the Flask/Gunicorn application itself as root.
- Review GPIO integrations before granting them privileged access.
- Review the optional startup optimiser before using it on a multipurpose system.

The supplied configuration intentionally runs the web application using a dedicated service account and limits privileged mode-switching operations through specific `sudoers` rules.

## Third-Party Dependencies

This project relies on third-party software and operating-system components.

Security issues relating specifically to an upstream component should also be reported to the relevant upstream project where appropriate.

See `THIRD_PARTY_NOTICES.md` for information about the project's major third-party dependencies.

## Responsible Disclosure

Please allow reasonable time for a vulnerability to be investigated and addressed before publishing exploit details.

Responsible disclosure helps protect users who may not yet have had an opportunity to update their systems.

Thank you for helping keep the CM6206 Audio Controller project secure.
