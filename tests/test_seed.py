import csv
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import seed  # noqa: E402

JKP = (57.78, 14.16)   # Jönköping
MUL = (57.92, 13.88)   # Mullsjö, Jönköpings län
GBG = (57.70, 11.97)   # Göteborg, Västra Götalands län
HAV = (56.50, 18.80)   # Östersjön, inget län


def rep(pos, *regions):
    return {"lat": pos[0], "lon": pos[1], "regions": list(regions)}


EXPORT = {"repeaters": [
    rep(JKP, "se06", "se", "*"),
    rep(JKP, "SE06", "se"),
    rep(MUL, "se06", "se", "se-vgr"),
    rep(MUL, "se-jkp", "se"),
    rep(GBG, "se14", "se"),
    rep(GBG, "se14", "se", "eu"),
    rep(GBG, "se-vgr"),
    rep(HAV, "se06"),
    {"lat": None, "lon": 1, "regions": ["se06"]},
]}


def rows():
    with seed.REGIONER.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Seed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lan = seed.load_lan()

    def measured(self, export=EXPORT):
        per_lan, totalt, var = seed.measure(seed.repeaters_from_export(export), self.lan)
        return seed.lansnamn(per_lan, var), totalt

    def test_points_land_in_the_right_lan(self):
        self.assertEqual(seed.lan_for(*JKP, self.lan), "Jönköpings län")
        self.assertEqual(seed.lan_for(*MUL, self.lan), "Jönköpings län")
        self.assertEqual(seed.lan_for(*GBG, self.lan), "Västra Götalands län")
        self.assertIsNone(seed.lan_for(*HAV, self.lan))

    def test_counts_names_per_lan_and_skips_shared_ones(self):
        egna, totalt = self.measured()
        self.assertEqual(totalt["Jönköpings län"], 4)
        # SE06 and se06 are different scopes to a repeater, so they are counted apart
        self.assertEqual(egna["Jönköpings län"], [("se06", 2), ("SE06", 1), ("se-jkp", 1)])
        # se-vgr: one carrier in each län, a tie, so it belongs to neither
        self.assertEqual(egna["Västra Götalands län"], [("se14", 2)])

    def test_a_name_mostly_carried_elsewhere_is_not_the_lans(self):
        export = {"repeaters": EXPORT["repeaters"] + [rep(GBG, "se-vgr")]}
        egna, _ = self.measured(export)
        self.assertNotIn("se-vgr", dict(egna["Jönköpings län"]))
        self.assertEqual(dict(egna["Västra Götalands län"])["se-vgr"], 2)

    def test_apply_seeds_only_lan_that_have_not_decided(self):
        egna, _ = self.measured()
        r = rows()
        vgr = next(x for x in r if x["scb_lan"] == "14")
        vgr["region"], vgr["beslut"] = "se-vg", "lokalt"
        changes = seed.apply(r, egna, min_repeatrar=2)
        self.assertEqual(changes, [("Jönköpings län", "se-jkp", "se06", 2)])
        jkp = next(x for x in r if x["scb_lan"] == "06")
        self.assertEqual((jkp["region"], jkp["beslut"]), ("se06", "uppmatt"))
        self.assertEqual((vgr["region"], vgr["beslut"]), ("se-vg", "lokalt"))

    def test_apply_never_seeds_a_name_outside_the_format(self):
        export = {"repeaters": [rep(JKP, "SE06"), rep(JKP, "SE06"), rep(JKP, "SE06"), rep(MUL, "se06")]}
        egna, _ = self.measured(export)
        self.assertEqual(egna["Jönköpings län"], [("SE06", 3), ("se06", 1)])
        self.assertEqual(seed.apply(rows(), egna, min_repeatrar=2), [])
        self.assertEqual(seed.apply(rows(), egna, min_repeatrar=1)[0][2], "se06")

    def test_apply_needs_enough_repeaters(self):
        egna, _ = self.measured()
        self.assertEqual(seed.apply(rows(), egna, min_repeatrar=4), [])

    def test_apply_never_takes_a_name_another_lan_has_chosen(self):
        egna, _ = self.measured()
        r = rows()
        kro = next(x for x in r if x["scb_lan"] == "07")
        kro["region"], kro["beslut"] = "se06", "lokalt"
        self.assertNotIn("Jönköpings län", [c[0] for c in seed.apply(r, egna, 2)])


if __name__ == "__main__":
    unittest.main()
