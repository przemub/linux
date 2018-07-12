# polinux
polinux to projekt edukacyjno-rozwojowy, mający na celu oswojenie przeze mnie (i ewentualnych innych uczestników?)
drzewa kodu źródłowego Linuksa poprzez tłumaczenie na język polski komunikatów jądra, które są wpisane w źródła "na sztywno"
po angielsku.

Zaczęło się od tego oto posta na grupie „Linuksowa Alternatywa”:
<img src="http://przemub.pl/pub/poploch.png" alt="Zrzut ekranu" />

24 godziny później powstała ta oto pierwsza działająca próbka polinuksa:
<img src="http://przemub.pl/pub/poploch2.png" alt="Zdjęcie ekranu" />

Co dalej? Czas pokaże.

## Po co?

* <a href="http://nonsensopedia.wikia.com/wiki/Bo_tak">Bo tak</a>.
* Jest to fajna motywacja, by pogrzebać w drzewie Linuksa i zrozumieć, co za co odpowiada.
* Tłumacząc słówka (nie uciekając się przy tym do makaronizmów) trzeba zrozumieć, co dany termin oznacza
i wprowadzić go przez to do swojego słownika.

## Fajne, jak to odpalić?

Użyj instrukcji z neta dla swojej ulubionej dystrybucji, jak skompilować jądro, oczywiście pobierając źródła z tej strony - na przykład tą komendą:
```sh
git clone --depth=1 https://przemub.pl/polinux
```

*Swoją drogą, używam Archa*, polecam więc tę instrukcję: https://wiki.archlinux.org/index.php/Kernels/Traditional_compilation

Powyższy komunikat błędu można wywołać usuwając z opcji uruchamiania systemu parametr root. Robi się to tak - klikasz "e"
w GRUBie na wpisie z polinuksem, z linijki zaczynającej się od "linux" usuwasz "root=cośtam" i klikasz Ctrl-X.
Następnie wpisujesz dwukrotnie "exit", by opuścić konsolę ratunkową i zobaczyć upragniony błąd.

## Jak pomóc?

W tym momencie trzeba przede wszystkim rozwiązać te problemy:
* wprowadzić jakiś system lokalizacji
* obsługa polskich znaków
* stworzyć słownik terminów, których używamy

Gdy zostaną one rozwiązane, można będzie się naprawdę zająć tłumaczeniem.

Zapraszam do dyskusji w zakładce "Issues".

Pomysły na terminy można na razie dawać tu: https://github.com/przemub/polinux/wiki/Pomys%C5%82y

