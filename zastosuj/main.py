#!/usr/bin/python3
import os
import re
import argparse
import sys
import glob

import polib

def main():
    print("Wersja przed-alfa. Ostrożnie.", file=sys.stderr)

    parser = argparse.ArgumentParser(description='Stosuje pliki *.po na źródłach.')
    parser.add_argument('-t', '--tłumaczenia', help="Katalog tłumaczeń", default="tłumaczenia")
    parser.add_argument('-z', '--źródła', help="Katalog korzenia źródeł", default="źródła")

    arg = parser.parse_args()

    for ścieżka in glob.glob(os.path.join(arg.tłumaczenia, "*.po")):
        plik = os.path.basename(ścieżka)
        źródło = os.path.join(arg.źródła, plik.replace("_", "/").replace(".po", ""))
        print("Stosowanie %s na %s." % (plik, źródło))

        ostrożnie = dict()
        try:
            p = open(os.path.join("ostrożnie", plik[:-3]), "r")
            print("\tWczytano plik ostrożności %s." % plik[:-3])

            for wpis in p.readlines():
                wpis = wpis.rstrip("\n")
                if not wpis.strip():
                    continue
                ostrożnie[wpis] = None

            p.close()
        except OSError:
            pass

        słownik = dict()
        try:
            po = polib.pofile(ścieżka)
            for wpis in po:
                if not wpis.msgstr:
                    continue
                if wpis.msgid in ostrożnie.keys():
                    ostrożnie[wpis.msgid] = wpis.msgstr
                else:
                    słownik[wpis.msgid] = wpis.msgstr
        except OSError:
            print("\tNie udało się otworzyć pliku %s. Pomijam.", file=sys.stderr)
            continue

        for źródło_plik in glob.glob(os.path.join(źródło, "*.c")):
            p = open(źródło_plik, "r")
            try:
                źródło_tekst = p.read()
            except UnicodeDecodeError:
                print("\tBłędny ciąg w pliku %s. Pomijam" % plik)
                p.close()
                continue
            p.close()

            ciągi = re.findall('"([^"]*)"', źródło_tekst)
            for ciąg in list(re.findall('"([^"]*)"', źródło_tekst)):
                if ciąg in słownik:
                    źródło_tekst = źródło_tekst.replace('"%s"' % ciąg, '"%s"' % słownik[ciąg])

            for wpis in ostrożnie:
                źródło_tekst = re.sub(r"(printk|pr_)(.*)\"" + wpis + r"\"(.*)",
                                      r'\g<1>\g<2>"' + ostrożnie[wpis] + r'"\g<3>',
                                      źródło_tekst)

            p = open(źródło_plik, "w")
            p.write(źródło_tekst)
            p.close()


if __name__ == "__main__":
    main()

