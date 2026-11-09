import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import seed  # noqa: E402

OMRADEN = {"06": "JKG", "12": "MMX", "10": "RNB", "14": "GOT", "22": "SDL"}


def rad(scb_lan, region, beslut="forslag"):
    return {"scb_lan": scb_lan, "lan": f"Län {scb_lan}", "region": region, "beslut": beslut}


def rows():
    return [rad("06", "se-jkp"), rad("12", "se-ska"), rad("10", "se-blk"),
            rad("14", "se-vgr"), rad("22", "se-vnl")]


def paket(omrade, scope, antal, typ="group_text", start=0):
    return [{"omrade": omrade, "packetHash": f"{omrade}:{scope}:{typ}:{start + i}", "firstHeardAt":
             1793059200000 + i, "payloadTypeName": typ, "scope": scope and f"#{scope}"}
            for i in range(antal)]


TRAFIK = (
    paket("JKG", "se-jkp", 90) + paket("JKG", "se06", 5) + paket("JKG", "se", 5)
    + paket("MMX", "se12", 60) + paket("MMX", "dk", 70)        # Skåne: 46 %, mest Danmark
    + paket("RNB", "se10", 55) + paket("RNB", "se12", 10)      # Blekinge hör Skåne också
    + paket("GOT", "se", 200) + paket("GOT", "se14", 3)
    + paket("SDL", "SDL", 80)                                  # versaler
    + paket("JKG", "se-jkp", 40, typ="advert")                 # bara kanalmeddelanden räknas
    + paket("JKG", None, 4)                                    # okänt scope
)


class Seed(unittest.TestCase):
    def measured(self, trafik=TRAFIK, r=None):
        per_omrade, period = seed.count(trafik)
        r = r or rows()
        return seed.lansnamn(r, OMRADEN, per_omrade), r, period

    def test_counts_channel_messages_once_per_area(self):
        dubbel = TRAFIK + paket("JKG", "se-jkp", 90)  # samma paket hört igen
        egna, _, _ = self.measured(dubbel)
        self.assertEqual(egna["06"], ([("se-jkp", 90), ("se06", 5)], 104))

    def test_shared_foreign_and_neighbour_codes_are_never_the_lans(self):
        egna, _, _ = self.measured()
        self.assertEqual(egna["12"][0], [("se12", 60)])        # dk is foreign
        self.assertEqual(egna["10"][0], [("se10", 55)])        # se12 is Skåne's code
        self.assertEqual(egna["14"][0], [("se14", 3)])         # se is shared

    def test_a_local_name_belongs_where_most_of_its_messages_are(self):
        egna, _, _ = self.measured(TRAFIK + paket("JKG", "jkp-syd", 20) + paket("GOT", "jkp-syd", 5))
        self.assertIn(("jkp-syd", 20), egna["06"][0])
        self.assertNotIn(("jkp-syd", 5), egna["14"][0])

    def test_registers_only_with_enough_messages_and_share(self):
        egna, r, _ = self.measured()
        andrat = {lan for lan, *_ in seed.apply(r, egna, 50, 50)}
        regions = {x["scb_lan"]: (x["region"], x["beslut"]) for x in r}
        self.assertEqual(regions["06"], ("se-jkp", "uppmatt"))
        self.assertEqual(regions["10"], ("se10", "uppmatt"))   # 55 of 65, 85 %
        self.assertEqual(regions["12"], ("se-ska", "forslag"))  # 60 of 130, 46 %
        self.assertEqual(regions["14"], ("se-vgr", "forslag"))  # 3 messages
        self.assertNotIn("Län 12", andrat)

    def test_uppercase_names_are_measured_but_never_registered(self):
        egna, r, _ = self.measured()
        self.assertEqual(egna["22"][0], [("SDL", 80)])
        seed.apply(r, egna, 50, 50)
        self.assertEqual(next(x for x in r if x["scb_lan"] == "22")["region"], "se-vnl")

    def test_a_local_decision_is_never_changed(self):
        r = rows()
        r[1] = rad("12", "se-ska", "lokalt")
        egna, r, _ = self.measured(TRAFIK + paket("MMX", "se12", 500, start=100), r)
        seed.apply(r, egna, 50, 50)
        self.assertEqual(r[1]["region"], "se-ska")

    def test_thresholds_are_options(self):
        egna, r, _ = self.measured()
        seed.apply(r, egna, 50, 40)
        self.assertEqual(next(x for x in r if x["scb_lan"] == "12")["region"], "se12")

    def test_rarely_used_names_are_not_listed(self):
        import tempfile
        egna, r, period = self.measured()
        with tempfile.TemporaryDirectory() as d:
            ut = Path(d) / "uppmatt.csv"
            seed.write_uppmatt(r, egna, period, 5, path=ut)
            listade = {rad.split(",")[2] for rad in ut.read_text().splitlines()[1:]}
        self.assertIn("se06", listade)       # 5 messages
        self.assertNotIn("se14", listade)    # 3 messages

    def test_period_is_taken_from_the_data(self):
        _, _, period = self.measured()
        self.assertEqual(period, ("2026-10-27", "2026-10-27"))


if __name__ == "__main__":
    unittest.main()
