import subprocess, json, logging

async def run_sherlock(username: str):
    try:
        result = subprocess.run(
            ["python3", "sherlock", username, "--json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return {"username": username, "totalFound": 0, "platforms": [], "error": result.stderr}
        data = json.loads(result.stdout)
        platforms = [{"name": k, "url": v.get("url"), "found": True} for k, v in data.items() if v.get("url")]
        return {
            "username": username,
            "totalFound": len(platforms),
            "platforms": platforms,
            "error": ""
        }
    except subprocess.TimeoutExpired:
        logging.error(f"Sherlock timeout for {username}")
        return {"username": username, "totalFound": 0, "platforms": [], "error": "Timeout"}
    except Exception as e:
        logging.error(f"Sherlock error: {e}")
        return {"username": username, "totalFound": 0, "platforms": [], "error": str(e)}
