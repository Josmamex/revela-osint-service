import subprocess, json, logging

async def run_holehe(email: str):
    try:
        result = subprocess.run(
            ["holehe", email, "--json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return {"email": email, "totalFound": 0, "platforms": [], "error": result.stderr}
        data = json.loads(result.stdout)
        platforms = [{"name": p["platform"], "registered": p["found"]} for p in data if p.get("found")]
        return {
            "email": email,
            "totalFound": len(platforms),
            "platforms": platforms,
            "error": ""
        }
    except subprocess.TimeoutExpired:
        logging.error(f"Holehe timeout for {email}")
        return {"email": email, "totalFound": 0, "platforms": [], "error": "Timeout"}
    except Exception as e:
        logging.error(f"Holehe error: {e}")
        return {"email": email, "totalFound": 0, "platforms": [], "error": str(e)}
