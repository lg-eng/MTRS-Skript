# AGENTS.md — MTRS-Skript

Quarto-Book (Projekt `book`, Format html, `lang: de`) für den Unterricht MTRS
(Messtechnik, Regelungs- und Steuerungstechnik) an der HTL Anichstraße Innsbruck.
Autoren: Leopold Götsch, CC BY. Repo: github.com/lg-eng/MTRS-Skript, Website:
https://lg-eng.github.io/MTRS-Skript/

## Organisation

- Wochenplan/Lehrstoffverteilung: `Lehrstoffverteilung MTRS monatsweise_NEU.csv`
  (im Parent-Ordner `02_Scripts/MTRS/`) plus
  `Lehrstoffverteilung_wochenweise_Vorschlag.md` — daraus ergibt sich, welche
  Kapitel fehlen und in welcher Unterrichtsreihenfolge sie angelegt werden.
  Die aktuelle Fehl-Kapitel-Liste steht in Abschnitt 4 des Vorschlags und im
  Buch-Kapitel `Anhang/xx_Jahresplanung.qmd`.
- Neue Kapitel pro Jahrgang numerieren wie `01.01_…`, `01.02_…` (Part-Nummer.
  Kapitel-Nummer), im Part-Ordner (`Messtechnik/`, `SteuerRegel/`, …).
- Jedes neue Kapitel in `_quarto.yml` im Part einsortieren — in
  Unterrichtsreihenfolge, konsistent mit dem Jahresplan.

## Stil

- Sprache Deutsch. Kurz und gliederungsartig: wenige Absätze, Stichpunkt-Listen,
  kompakte Tabellen. Keine Füllwörter, keine langen Einleitungen.
- Formatierung an bestehenden Seiten orientieren: `# Titel {#sec-…}` als Kapitel,
  `##`/`###` mit `{#sec-…}`-Ankern, `$$…$$` nur für Ausnahmen (alles Rechnende
  gehört in Chunks, siehe unten), Pipe-Tabellen.
- Messunsicherheit immer nach GUM (JCGM 100:2008; deutsche Einführung: JCGM 104
  der PTB) behandeln — Schätzwert + Messunsicherheit, Typ-A/Typ-B-Bewertung,
  kombinierte/erweiterte Unsicherheit. Keine veraltete „wahrer Wert + Messfehler"-
  Sprechweise; systematische Effekte heißen Messabweichung. Die Bib-Einträge
  `jcgm100_2008` und `jcgm104_2011de` existieren in `references.bib`.

## Python-Chunks (wichtigste Regel)

Alle Formeln und Diagramme sind **ausführbare Chunks** — nichts statisch
hinzeichnen, was SymPy/Matplotlib berechnen kann:

- Zeile 2 jeder neuen Kapitel-Datei: den Helper einbinden:

  `{{< include ../../../../Common/QuartoBookHelpers/QuartoBookHelpers.qmd >}}`

  **Der Helper ist read-only.** Er liegt außerhalb des Repos und wird von
  mehreren Quarto-Büchern geteilt — niemals ohne ausdrückliche Autorisierung
  des Owners ändern.

- Formeln: SymPy über die Helper-API — `MySymbol('x', description='…',
  unit=u.volt, value=…)`, `QBookHelpers.print_description([...])`,
  `QBookHelpers.print_equation(eq, label='eq-eindeutig-unique')`,
  `QBookHelpers.print_values([...])`, `QBookHelpers.calculate_num_value(eq)`
  (siehe `Messtechnik/01.01_Einfuehrung.qmd` bis `01.04_Kennwerte.qmd` als
  Referenzmuster).
- Gleichungs-Labels projektweit eindeutig vergeben; `print_equation` immer mit
  `label` aufrufen.
- Diagramme: matplotlib im Chunk erzeugen (keine vor-generierten PNGs, keine
  Build-Skripte für Abbildungen). Figur-Optionen:
  `#| label: fig-…` und `#| fig-cap: '…'` — **fig-cap immer in einfachen
  Anführungszeichen**, weil LaTeX-Backslash-Ausdrücke (`\sqrt`, `\gg`) in
  doppelt-quotierten YAML-Strings zu "unknown escape sequence"-Fehlern führen.
- Jeder Chunk erhält `#| echo: true` und `#| code-fold: true`, damit der Code
  an Ort und Stelle ausklappbar ist (Projekt-Default ist `execute: echo:
  false`).
- Fences sauber schließen: `​```{python}` mit Klammer — ein fehlendes `}` lässt
  Quarto den Chunk **stillschweigend** als Zelle übergehen.

## Bilder

- Freie Bilder von Wikimedia Commons; Lizenzangabe **in der Bildunterschrift**:
  "(Autor, [Lizenz-Link], via [Wikimedia Commons](Datei-URL))". Große Dateien
  vor dem Commit auf ~1400 px skalieren.
- Kein Bild gefunden → **Platzhalter** als Blockquote `> **Platzhalter — …:**`
  mit kurzer Beschreibung der Bildabsicht. Keine Bilder „erfinden"/KI-generieren;
  Kennlinien/Schaltungs-Illustrationen als Matplotlib-Chunk sind erlaubt.

## Testen und Rendern

- Nach Chunk-Änderungen zuerst offline prüfen:
  `uv run --frozen python Messtechnik/test_chunks.py` (Testharness, der alle
  Python-Chunks der Messtechnik-Kapitel ohne Quarto ausführt). Für neue Ordner
  die Dateiliste im Skript erweitern.
- Rendern: `quarto preview` mit `QUARTO_PYTHON` auf den venv-Python setzen:
  `QUARTO_PYTHON=.venv/Scripts/python.exe quarto preview`. Der venv wird per
  `uv run --frozen` verwaltet. Preview rendert inkrementell und serviert die
  Site auf localhost.
- Die MQTT-Sektion in `Datenanalyse/Datenanalyse_Datenquellen.qmd` bleibt
  auskommentiert (`<!-- … -->` **und** `eval: false` im Chunk — nur der
  HTML-Kommentar verhindert die Ausführung nicht!): der verlinkte
  Test-Broker ist tot, sonst hängt der Render ewig.

## Git / Umgebung (OneDrive!)

- Das Repo liegt in einem OneDrive-Ordner. `git status`/`checkout` können mit
  `mmap failed` oder `index.lock exists` fehlschlagen → in Schleife wiederholen.
- Beim Staged-adden OneDrive-Konfliktkopien ausschließen:
  `git add -A -- . ':(exclude)*(1)*'`.
- Standalone-Renders (`quarto render EinzelDatei.qmd`) erzeugen Müll neben den
  Quellen (Root-`site_libs/`, `*.html` und `*_files/` neben den Kapiteln) —
  nicht committen, nach dem Rendern löschen. Book-Output liegt ausschließlich
  in `_book/`.
- Push nur nach ausdrücklicher Freigabe des Owners. Commit-Nachrichten enden
  mit dem Mistral-Vibe-Co-Author-Block.
