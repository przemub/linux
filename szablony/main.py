import os
import re
import argparse
import sys

def main():
    print("Wersja przed-alfa. Ostrożnie.", file=sys.stderr)

    parser = argparse.ArgumentParser(description='Przetwarza źródła na szablony do tłumaczenia.')
    grupa = parser.add_mutually_exclusive_group(required=True)
    grupa.add_argument('-z', '--zrodla', help="Katalog, który chcesz przetworzyć")
    grupa.add_argument('-w', help="Przetwórz wszystko. Zastępuje -rz źródła.", action="store_true")
    parser.add_argument('-s', '--wyjście', help="Katalog na szablony wyjściowe", default="wyjście")
    parser.add_argument('-k', '--korzeń', help="Katalog korzenia źródeł", default="źródła")
    parser.add_argument('-r', help="Przetwarzaj rekurencyjnie", action="store_true")

    arg = parser.parse_args()

    try:
        os.mkdir(arg.wyjście)
    except FileExistsError:
        pass

    for korzeń, katalogi, pliki in os.walk('źródła'):
        # Usuwanie '/źrodła'
        korzeń = korzeń[7:]
        nazwa = korzeń.replace("/", "_")

        if nazwa.startswith('Documentation'):
            continue

        źródła = list(filter(lambda x: x.endswith(".c"), pliki))
        if not źródła:
            continue

        print("Generowanie", nazwa + ".pot")

        szablon = ""

        dodatkowe = set()
        try:
            p = open(os.path.join('dodatkowe', nazwa), "r")
            for linia in p.readlines():
                dodatkowe.add(linia.strip())
        except OSError:
            pass

        powtórki = set()
        for plik in źródła:
            p = open(os.path.join('źródła', korzeń, plik), "r")
            try:
                źródło = p.read()
            except UnicodeDecodeError:
                print("Błędny ciąg w pliku %s. Pomijam" % plik)
                p.close()
                continue
            p.close()


            ciągi = re.findall('"([^"]*)"', źródło)
            ciągi = []
            for l, linia in enumerate(źródło.split('\n')):
                for ciąg in re.findall('"([^"]*)"', linia):
                    if not ciąg.strip():
                        continue
                    if ciąg in ('\\n',):
                        continue
                    if linia.find("printk") == -1 and linia.find("pr_") == -1 \
                        and linia.find("panic") == -1 \
                        and ciąg.strip() not in dodatkowe:
                        continue
                    if ciąg in powtórki:
                        continue

                    powtórki.add(ciąg)
                    ciągi.append((ciąg, l))

            for ciąg in ciągi:
                szablon += "#: %s/%s:%d\n#, cformat\nmsgid \"%s\"\nmsgstr \"\"\n\n" % \
                           (korzeń, plik, ciąg[1], ciąg[0])

        if not szablon.strip(' \n\t'):
            continue
        
        p = open(os.path.join(arg.wyjście, nazwa + ".pot"), "w")
        p.write(szablon)
        p.close()


if __name__ == "__main__":
    main()

