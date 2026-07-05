from backend.services.dashboard_export_service import DashboardExportService


def main():
    exporter = DashboardExportService(
        candidates_path="datasets/candidates.jsonl",
        submission_path="exports/submission.csv",
        output_path="exports/dashboard_data.csv"
    )

    exporter.export_dashboard_data()


if __name__ == "__main__":
    main()