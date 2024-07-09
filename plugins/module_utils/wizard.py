
def wizard(connection, wizard_xml, step_id, data: dict):
    connection.post(
        "/wizard.php",
        {
            "xml": f"{wizard_xml}.xml",
            "stepid": step_id,
            "next": "Next"
        } | {k: "on" if v is True else v for k, v in data.items() if v is not None} if data is not None else {}
    )
