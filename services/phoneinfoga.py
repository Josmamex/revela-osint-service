import subprocess, json, logging

async def run_phoneinfoga(phone: str):
    try:
        result = subprocess.run(
            ["phoneinfoga", "scan", "-n", phone, "--output", "json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return {"phoneNumber": phone, "valid": False, "country": "", "carrier": "", "lineType": "", "error": result.stderr}
        data = json.loads(result.stdout)
        return {
            "phoneNumber": phone,
            "valid": data.get("valid", False),
            "country": data.get("country", ""),
            "carrier": data.get("carrier", ""),
            "lineType": data.get("line_type", ""),
            "error": ""
        }
    except subprocess.TimeoutExpired:
        logging.error(f"PhoneInfoga timeout for {phone}")
        return {"phoneNumber": phone, "valid": False, "country": "", "carrier": "", "lineType": "", "error": "Timeout"}
    except Exception as e:
        logging.error(f"PhoneInfoga error: {e}")
        return {"phoneNumber": phone, "valid": False, "country": "", "carrier": "", "lineType": "", "error": str(e)}
