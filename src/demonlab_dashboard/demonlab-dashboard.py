import asyncio
import json
import logging
from datetime import datetime, timezone

import psycopg2
from about import AboutScreen
from clock import ClockWidget
from psycopg2 import extensions
from startup import SplashScreen
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, HorizontalScroll, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import (
    Button,
    Digits,
    Footer,
    Header,
    Label,
    LoadingIndicator,
    Placeholder,
    Rule,
    Static,
)
from textual_serve.server import Server

# Configure logging
logging.basicConfig(
    filename="demonlab_dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    filemode="a",
)


server = Server("python -m textual")


class Anomoly(Screen):
    pass


class Alerts(Screen):
    pass


class Misc(Screen):
    pass


class GridLayoutTest(App):
    CSS_PATH = "demonlab-dashboard.tcss"
    TITLE = "Demonlab Dashboard"
    SUB_TITLE = "Synapse and Sysadmin"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
        Binding(key="b", action="null", description="Beep"),
        Binding(key="p", action="null2", description="Plop"),
        Binding(key="a", action="about", description="About"),
        Binding(key="s", action="splashscreen", description="Splash"),
    ]

    # Traffic light icons for user state
    state_icons = {
        "online": "🟢",
        "busy": "🟡",
        "unavailable": "🔴",
        "unknown": "⚪",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize user tracking data
        self.tracked_users: list[str] = []
        self.user_data: dict[str, dict] = {}
        self.user_widgets: dict[str, Label] = {}
        self.displayed_users: list[str] = []
        # Load initial data from database
        logging.info("Initializing dashboard data...")
        try:
            self.refresh_materialized_view()
        except Exception as e:
            logging.error(f"Error refreshing view: {e}")
        try:
            self.load_user_data_from_view()
        except Exception as e:
            logging.error(f"Error loading user data: {e}")
        logging.info(f"Loaded {len(self.tracked_users)} tracked users.")
        # Determine which users to display (two rows worth)
        users_sorted = sorted(
            self.tracked_users,
            key=lambda uid: self.user_data.get(uid, {}).get("last_active_ts", 0),
            reverse=True,
        )
        self.displayed_users = users_sorted[:12]

    def fetch_tracked_users(self) -> list[str]:
        """Fetch tracked users from the database."""
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM synapx.scorecard_member_list;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def refresh_materialized_view(self):
        """Refresh the materialized view for user last active data."""
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("REFRESH MATERIALIZED VIEW synapx.user_last_active;")
        conn.commit()
        cursor.close()
        conn.close()

    def load_user_data_from_view(self):
        """Load user activity data from the refreshed view."""
        self.tracked_users = self.fetch_tracked_users()
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, last_active_ts, display_name, clickable_avatar, usrtz "
            "FROM synapx.user_last_active ORDER BY last_active_ts DESC;"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for user_id, last_active_ts, display_name, avatar_url, usrtz in rows:
            if last_active_ts and last_active_ts > 0:
                last_active_str = datetime.fromtimestamp(
                    last_active_ts / 1000, timezone.utc
                ).strftime("%Y-%m-%dT%H:%M")
            else:
                last_active_str = "N/A"
            self.user_data[user_id] = {
                "state": "unavailable",
                "last_active": last_active_str,
                "last_active_ts": last_active_ts or 0,
                "clickable_avatar": avatar_url,
                "timezone": usrtz or "TZ",
                "display_name": display_name or user_id,
                "currently_active": False,
                "glyph_status": "🔴",
                "status_msg": "N/A",
                "instance": "Unknown",
            }
        # Add default entries for any tracked users missing from the view
        for user_id in self.tracked_users:
            if user_id not in self.user_data:
                self.user_data[user_id] = {
                    "state": "unavailable",
                    "last_active": "N/A",
                    "last_active_ts": 0,
                    "clickable_avatar": None,
                    "timezone": "TZ",
                    "display_name": user_id,
                    "currently_active": False,
                    "glyph_status": "🔴",
                    "status_msg": "N/A",
                    "instance": "Unknown",
                }

    def process_notification(self, payload: str):
        """Process a notification payload (JSON) to update user data."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e} – Payload: {payload}")
            return
        user_id = data.get("user_id")
        if not user_id:
            logging.warning("Skipping notification with no user_id.")
            return
        state = data.get("state", "unknown")
        last_ts = data.get("last_active_ts", 0)
        currently_active = data.get("currently_active", False)
        instance = data.get("instance_name", "Unknown")
        status_msg = data.get("status_msg", "N/A")
        last_active = (
            datetime.fromtimestamp(last_ts / 1000, timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            if last_ts and last_ts > 0
            else "N/A"
        )
        if user_id in self.tracked_users:
            self.user_data[user_id].update(
                {
                    "state": state,
                    "last_active": last_active,
                    "last_active_ts": last_ts or 0,
                    "currently_active": currently_active,
                    "instance": instance,
                    "status_msg": status_msg,
                    "glyph_status": "🟢" if currently_active else "🔴",
                }
            )
            logging.info(f"Updated: {user_id} -> {self.user_data[user_id]}")
        else:
            logging.info(f"Skipping untracked user: {user_id}")

    async def listen_notifications(self):
        """Listen for database notifications and update the dashboard."""
        channel = "dln_test_notifications"
        conn = None
        try:
            while True:
                try:
                    conn = psycopg2.connect(
                        dbname="synapse",
                        user="synapse_user",
                        password="synapse",
                        host="10.99.10.128",
                        port=5432,
                    )
                    conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                    cursor = conn.cursor()
                    cursor.execute(f"LISTEN {channel};")
                    logging.info(f"Listening on channel: {channel}")
                except psycopg2.OperationalError as e:
                    logging.error(f"Database connection error: {e}. Retrying in 5s...")
                    await asyncio.sleep(5)
                    continue
                try:
                    while True:
                        await asyncio.sleep(1.0)
                        conn.poll()
                        while conn.notifies:
                            notify = conn.notifies.pop(0)
                            self.process_notification(notify.payload)
                        # Refresh the dashboard panels with new data
                        self.refresh_user_panels()
                except psycopg2.OperationalError as e:
                    logging.error(
                        f"Database error in listen loop: {e}. Reconnecting..."
                    )
                    # Loop will retry connection
                except Exception as e:
                    logging.error(f"Unexpected error in listener: {e}", exc_info=True)
                    # Break out to reconnect on any other exception
                finally:
                    if conn:
                        try:
                            conn.close()
                        except Exception:
                            pass
                # Continue outer loop to reconnect if needed
        except asyncio.CancelledError:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
            logging.info("Notification listener task cancelled.")

    def refresh_user_panels(self):
        """Update the displayed user panels with the latest user_data."""
        for user_id in self.displayed_users:
            if user_id not in self.user_widgets:
                continue
            widget = self.user_widgets[user_id]
            info = self.user_data.get(user_id, {})
            # Update icons and colors based on current state
            state_icon = self.state_icons.get(info.get("state", "unknown"), "⚪")
            active_icon = (
                " " if not info.get("currently_active") else "[#d7af00] [/#d7af00]"
            )
            fade_color = "#444444"
            lgap_str = "N/A"
            if info.get("last_active") not in (None, "N/A"):
                try:
                    last_active_time = datetime.fromisoformat(info["last_active"])
                    if last_active_time.tzinfo is None:
                        last_active_time = last_active_time.replace(tzinfo=timezone.utc)
                    gap = datetime.now(timezone.utc) - last_active_time
                    minutes_idle = gap.total_seconds() / 60
                    if minutes_idle < 5:
                        fade_color = "lime"
                    elif minutes_idle < 30:
                        fade_color = "#ffd700"
                    elif minutes_idle < 120:
                        fade_color = "#888888"
                    else:
                        fade_color = "#444444"
                    lgap_str = f"[firebrick]{gap.days}d[/] [royalblue]{gap.seconds//3600}h[/] [orangered]{gap.seconds//60%60}m[/]"
                except Exception as e:
                    logging.error(f"Error computing gap for {user_id}: {e}")
                    fade_color = "#444444"
                    lgap_str = "Calc Error"
            status_msg = info.get("status_msg", "N/A")
            tz_label = info.get("timezone", "TZ")
            last_active_label = info.get("last_active", "N/A")
            new_content = (
                f"[#0A9396] : {last_active_label}[/#0A9396]\n"
                f"[#3772FF bold] :[/] {lgap_str}\n"
                f"[#800D80 bold] : {status_msg}[/#800D80 bold]\n"
                "\n"
                f"   [#FFC300] [/#FFC300] {state_icon} "
                f"[#4c3e93]  [/#4c3e93][#279af1]  [/#279af1]"
                f"[#0ebd8c]  [/#0ebd8c][#ff006e]  [/#ff006e]  "
                f"[#8BC34A]  [/#8BC34A]\n"
                #    f"[link='{avatar_url}'][/link]"
            )
            widget.border_title = f"[bold {fade_color}]{user_id}[/bold {fade_color}]"
            widget.border_subtitle = (
                f"{tz_label} {active_icon}[grey35]{info['display_name']}[/grey35]"
            )
            widget.update(new_content)
            widget.border = ("heavy", fade_color)

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Header()
        # Yield user panels (two rows of 6)
        actual_count = len(self.displayed_users)
        for index in range(12):
            if index < actual_count:
                user_id = self.displayed_users[index]
                info = self.user_data[user_id]
                state_icon = self.state_icons.get(info["state"], "⚪")
                active_icon = (
                    " " if not info["currently_active"] else "[#d7af00] [/#d7af00]"
                )
                fade_color = "#444444"
                lgap_str = "N/A"
                if info["last_active"] != "N/A":
                    try:
                        last_dt = datetime.fromisoformat(info["last_active"])
                        if last_dt.tzinfo is None:
                            last_dt = last_dt.replace(tzinfo=timezone.utc)
                        gap = datetime.now(timezone.utc) - last_dt
                        minutes_idle = gap.total_seconds() / 60
                        if minutes_idle < 5:
                            fade_color = "lime"
                        elif minutes_idle < 30:
                            fade_color = "#ffd700"
                        elif minutes_idle < 120:
                            fade_color = "#888888"
                        else:
                            fade_color = "#444444"
                        lgap_str = (
                            f"{gap.days}d {gap.seconds//3600}h {gap.seconds//60%60}m"
                        )
                    except Exception as e:
                        logging.error(f"Error calculating gap for {user_id}: {e}")
                        lgap_str = "Calc Error"
                        fade_color = "#444444"
                status_msg = info.get("status_msg", "N/A")
                tz_label = info.get("timezone", "TZ")
                last_active_label = info["last_active"]
                content = (
                    f"[#0A9396] : {last_active_label}[/#0A9396]\n"
                    f"[#0A9396]    {tz_label} [/#0A9396]\n"
                    f"[#3772FF bold] : {lgap_str}[/#3772FF bold]\n"
                    f"[#800D80 bold] : {status_msg}[/#800D80 bold]\n"
                    "\n"
                    f"   [#FFC300] [/#FFC300] {state_icon} "
                    f"[#4c3e93]  [/#4c3e93][#279af1]  [/#279af1]"
                    f"[#0ebd8c]  [/#0ebd8c][#ff006e]  [/#ff006e]  "
                    f"[#8BC34A]  [/#8BC34A][red][i] Avatar[/i][/red]"
                    f"[#8BC34A]  [/#8BC34A][red][i] Avatar[/i][/red]",
                    Digits(f"{index}", id=f"gap{index+1}"),
                )
                user_label = Label(content, id=f"User{index+1}", classes="box")
                user_label.border_title = (
                    f"[bold {fade_color}]{user_id}[/bold {fade_color}]"
                )

                user_label.border_subtitle = f"{last_active_label} {active_icon}[grey35]{info['display_name']}[/grey35]"

                user_label.border = ("heavy", fade_color)
                self.user_widgets[user_id] = user_label
                yield user_label
            else:
                # Empty panel placeholder
                yield Label("", id=f"User{index+1}", classes="box empty_box")
        # Other panels and controls
        yield Static("[b]Options Misc2[/b]", classes="box", id="opts")
        yield Static("[b]General System Health[/b]", classes="box", id="gsh")
        yield Static("[b]System Alerts[/b]", classes="box", id="alrt")
        yield Static("[b]System Misc.[/b]", classes="box", id="msc")
        yield Horizontal(
            Button("DF Report", id="but01"),
            Button("Scrub Stat", id="but02"),
            Button("ssh FF1", id="but03"),
            Button("ssh FN2", id="but04"),
            Button("ssh rpi05", id="but05"),
            Button("All Stop", id="but06"),
            Button("Primary", id="but07"),
            Button("Blowjob", id="but08"),
        )
        yield Horizontal(ClockWidget(), id="clockface")

    async def on_mount(self):
        # Show splash screen initially, fade-in effect clearly working
        await self.push_screen(SplashScreen())

        # Start the background notification listener
        self.notifications_task = asyncio.create_task(self.listen_notifications())

        # Start system health updater task
        asyncio.create_task(self.update_health())

        # Short delay clearly visible, then remove splash screen automatically

        await asyncio.sleep(3)

        await self.pop_screen()

    async def update_health(self):
        """Periodically update General System Health panel with query results explicitly."""
        while True:
            label, next_datapoint = await asyncio.to_thread(
                self.query_db_next_datapoint
            )

            gsh_widget = self.query_one("#gsh", Static)
            gsh_widget.update(
                f"[b]General System Health[/b]\n\n[green]{label}: {next_datapoint}[/green]"
            )

            await asyncio.sleep(60)

    def query_db_next_datapoint(self):
        """Correct synchronous DB query, safely executed explicitly."""
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
            SELECT
            trim('Next Datapoint') as "Label",
            max(local_timestamp) + interval '3 hours' as "NEXT"
            FROM synapx.reports
            """
            )
            result = cursor.fetchone()

            if result and result[1]:
                label, next_datapoint = result
                next_dp_str = next_datapoint.strftime("%Y-%m-%d %H:%M:%S")
                return label, next_dp_str
            else:
                return "Next Datapoint", "N/A"
        finally:
            cursor.close()
            conn.close()

    def action_null(self) -> None:
        """No-op action for 'b' key (beep)."""
        return

    def action_null2(self) -> None:
        """No-op action for 'p' key (plop)."""
        return

    def action_about(self) -> None:
        """No-op action for 'a' key (about)."""
        self.push_screen(AboutScreen())
        return

    def action_splashscreen(self) -> None:
        """No-op action for 's' key (splash)."""
        self.push_screen(SplashScreen())
        return


if __name__ == "__main__":
    app = GridLayoutTest()
    app.run()
