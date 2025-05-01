#!/usr/bin/env python3
"""Service status checker with Textual DataTable display"""
import subprocess

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header


class ServiceStatusChecker:
    def __init__(self, username, hostname, service_name):
        self.username = username
        self.hostname = hostname
        self.service_name = service_name

    def is_service_active(self):
        try:
            command = f"systemctl -H {self.username}@{self.hostname} is-active {self.service_name}"
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result.stdout.decode().strip() == "active"
        except subprocess.CalledProcessError as e:
            print(f"Error checking service status: {e}")
            return False

class ServiceStatusApp(App):
    """Textual app to display service statuses in a table."""

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, services, username, hostname, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services = services
        self.username = username
        self.hostname = hostname
        self.checkers = [
            ServiceStatusChecker(username, hostname, service)
            for service in services
        ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Service", "Status", "Host")
        table.cursor_type = "none"

        for checker in self.checkers:
            status = "active" if checker.is_service_active() else "inactive"
            color = "green" if status == "active" else "red"
            table.add_row(
                checker.service_name,
                f"[{color}]{status}[/]",
                checker.hostname,
            )

def main():
    services_to_check = [
        "barad-dur",
        "dnsmasq",
        "sshd",
        "nginx",
        "unbound",
        "postgresql",
    ]

    username = "mike"
    hostname = "pi0501"

    app = ServiceStatusApp(services_to_check, username, hostname)
    app.run()

if __name__ == "__main__":
    main()
