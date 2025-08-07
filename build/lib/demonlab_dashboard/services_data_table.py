#!/usr/bin/env python3
"""Service Status Widget for Textual Dashboard"""
import datetime
import subprocess
from typing import List

from textual.widget import Widget
from textual.widgets import DataTable


class ServiceStatusChecker:
    def __init__(self, username: str, hostname: str, service_name: str):
        self.username = username
        self.hostname = hostname
        self.service_name = service_name

    def is_service_active(self) -> bool:
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


class ServiceStatusWidget(Widget):
    """A widget that displays service statuses in a DataTable."""

    def __init__(
        self,
        services: List[str],
        username: str,
        hostname: str,
        name: str = None,
        id: str = None,
        classes: str = None,
    ):
        super().__init__(name=name, id=id, classes=classes)
        self.services = services
        self.username = username
        self.hostname = hostname
        self.checkers = [
            ServiceStatusChecker(username, hostname, service) for service in services
        ]
        self.table = DataTable()
        self.table.cursor_type = "row"
        self.table.add_columns(
            "Service",
            "Status",
            "Host",
            "Last ✔",
            "Next ✔",
            "Type",
            "Additional Info",
        )
        self.table.zebra_styles = True

    def on_mount(self) -> None:
        """Refresh statuses when widget is mounted."""
        self.refresh_statuses()

    def refresh_statuses(self) -> None:
        """Refresh all service statuses and update the table."""
        self.table.clear()
        for checker in self.checkers:
            status = "active" if checker.is_service_active() else "inactive"
            color = "#00ff00" if status == "active" else "#ff0000"
            self.table.add_row(
                checker.service_name,
                f"[{color}]{status}[/]",
                checker.hostname,
            )

    def compose(self):
        """Compose the widget with its table."""
        yield self.table
