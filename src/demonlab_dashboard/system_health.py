from textual.widgets import Static

from database import Database  # Ensure Database module is imported


class SystemHealthPanel(Static):
    async def on_mount(self):
        label, next_datapoint = await self.fetch_health_data()
        self.update(
            f"[b]General System Health[/b]\n{label}:[green bold]{next_datapoint}[/green bold]"
        )

    async def fetch_health_data(self):
        query = """
            SELECT
                TRIM('Next Datapoint') AS "Label",
                MAX(local_timestamp) + INTERVAL '3 hours' AS "NEXT"
            FROM synapx.reports
        """
        result = await Database.execute_query(query)
        if result:
            return result[0]["Label"], result[0]["NEXT"].strftime("%Y-%m-%d %H:%M:%S")
        return "Next Datapoint", "No Data Available"
