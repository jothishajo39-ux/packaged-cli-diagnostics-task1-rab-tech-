import json


def build_report(system_info, event_analysis):
    return {
        "diagnostic_tool": "Packaged CLI Diagnostics Tool",
        "system": system_info,
        "events": event_analysis,
        "overall_status": (
            "FAIL"
            if event_analysis["status"] == "FAIL"
            else event_analysis["status"]
        ),
    }


def human_report(report):
    system = report["system"]
    disk = system["disk_space"]
    events = report["events"]

    lines = [
        "=== Machine Diagnostic Report ===",
        f"Python Version : {system['python_version']}",
        f"Platform       : {system['platform']}",
        f"Disk Total     : {disk['total_gb']} GB",
        f"Disk Used      : {disk['used_gb']} GB",
        f"Disk Free      : {disk['free_gb']} GB",
        f"PATH Configured: {system['environment']['PATH_configured']}",
        "",
        "Developer Tools:",
    ]

    for name, info in system["developer_tools"].items():
        status = "Installed" if info["installed"] else "Missing"
        lines.append(f"  - {name}: {status}")

    lines += [
        "",
        "Diagnostic Events:",
        f"  - Total events : {events['event_count']}",
        f"  - Errors       : {events['error_count']}",
        f"  - Warnings     : {events['warning_count']}",
        f"  - Services     : {', '.join(events['services']) or 'None'}",
        "",
        f"Overall Status  : {report['overall_status']}",
    ]
    return "\n".join(lines)


def save_json(report, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)
