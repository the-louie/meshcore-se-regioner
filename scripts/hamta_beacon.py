#!/usr/bin/env python3
"""Hämtar alla paket med scope från Beacon (beacon.meshat.se) för de svenska områdena.

Kör:  python3 scripts/hamta_beacon.py <från> <till> beacon.jsonl
      python3 scripts/hamta_beacon.py 2026-10-27T00:00:00Z 2026-11-09T00:00:00Z beacon.jsonl

Beacon är öppet och kräver ingen nyckel. Skriptet läser via Beacons MCP-server, bara
sökningar, och väntar mellan anropen för att inte belasta den. Två veckor tar ungefär en kvart.
Beacon sparar paket i ungefär två veckor, så längre bakåt än så går inte.

Resultatet är en rad JSON per paket, med området (omrade) det hördes i. Filen checkas inte in.
"""
import csv
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OMRADEN = ROOT / "data" / "beacon-omraden.csv"
URL = "https://mcp.beacon.meshat.se/"
PAUS = 0.4


class Beacon:
    def __init__(self):
        self.session = None
        self.next_id = 1
        self._rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                 "clientInfo": {"name": "meshcore-se-regioner", "version": "1"}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _post(self, body):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream"}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(URL, json.dumps(body).encode(), headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            self.session = resp.headers.get("Mcp-Session-Id") or self.session
            raw = resp.read().decode()
            ctype = resp.headers.get("Content-Type", "")
        if not raw:
            return None
        if "event-stream" in ctype:
            raw = [l[5:].strip() for l in raw.splitlines() if l.startswith("data:")][-1]
        return json.loads(raw)

    def _rpc(self, method, params):
        r = self._post({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params})
        self.next_id += 1
        if "error" in r:
            raise RuntimeError(r["error"])
        return r["result"]

    def sok(self, **args):
        time.sleep(PAUS)
        r = self._rpc("tools/call", {"name": "beacon_search_packets", "arguments": args})
        if r.get("isError"):
            raise RuntimeError(r["content"][0]["text"])
        return r.get("structuredContent") or json.loads(r["content"][0]["text"])


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2
    fran, till, ut = argv[1], argv[2], Path(argv[3])
    with OMRADEN.open(newline="", encoding="utf-8") as f:
        omraden = sorted({r["omrade"] for r in csv.DictReader(f)})
    beacon = Beacon()
    with ut.open("w", encoding="utf-8") as f:
        for omrade in omraden:
            # routeTypes 0 och 3: flood och direkt med scope (transport-kod)
            args = dict(iatas=[omrade], routeTypes=[0, 3], since=fran, until=till, limit=50)
            antal = 0
            while True:
                r = beacon.sok(**args)
                for paket in r["items"]:
                    paket["omrade"] = omrade
                    f.write(json.dumps(paket, ensure_ascii=False) + "\n")
                antal += len(r["items"])
                nasta = r["pagination"].get("nextCursor")
                if not r["pagination"].get("hasMore") or not nasta:
                    break
                args["pageCursor"] = nasta["pageCursor"]
            print(f"{omrade} {antal}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
