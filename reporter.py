import csv
import os
import html

class Reporter:
    def __init__(self, outputs):
        self.outputs = outputs

    def outputs_to_csv(self):

        columns_order = [
            "url",
            "title",
            "score",
            "direct_answer",
            "definiton",
            "headings",
            "facts",
            "sources",
            "faq",
            "lists",
            "tables",
            "length_ok",
            "meta_ok",
            "recomandations"
        ]

        # vytvor priečinok ak neexistuje
        os.makedirs("output", exist_ok=True)

        path = "output/report.csv"
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as csvfile:

                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=columns_order,
                    delimiter=";"
                )

                # zapíše hlavičku
                writer.writeheader()

                # zapíše riadky
                for row in self.outputs:

                    # zabezpečí, že všetky stĺpce existujú
                    clean_row = {col: row.get(col, "") for col in columns_order}

                    writer.writerow(clean_row)
        except PermissionError:
            print(f"Nemôžem zapísať {path} (pravdepodobne je otvorený v Exceli). Zavri súbor a skús znova.")
        
        print(f"Data uložené: {path}")

    def outputs_to_html(self):
        columns_order = [
            "url", "title", "score", "direct_answer", "definiton", "headings",
            "facts", "sources", "faq", "lists", "tables", "length_ok",
            "meta_ok", "recomandations"
        ]

        os.makedirs("output", exist_ok=True)
        path = "output/report.html"

        def cell(value):
            """Return HTML for a table cell with basic formatting."""
            if isinstance(value, bool):
                cls = "ok" if value else "no"
                return f'<td class="{cls}">{str(value)}</td>'
            return f"<td>{html.escape(str(value))}</td>"
        
        def score_cell(score):

            if score >= 8:
                cls = "score-high"
            elif score >= 5:
                cls = "score-medium"
            else:
                cls = "score-low"

            return f'<td class="{cls}">{score}</td>'
        
        rows = list(self.outputs)

        # Build HTML
        parts = []
        parts.append("""<!doctype html>
                        <html lang="sk">
                        <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1">
                            <title>GEO Audit Report</title>
                            <style>
                                body {
                                    font-family: Arial, sans-serif;
                                    background: #ffffff;
                                    margin: 24px;
                                    }
                                    .page {
                                    margin: 40px auto;
                                    padding: 20px 40px 60px;
                                    background: #fff;
                                    }
                                    .logo {
                                    height: 100px;
                                    width: auto;
                                    display: flex;
                                    margin-bottom: 40px;
                                    }
                                    .text {
                                    font-size: 14px;
                                    line-height: 1.6;
                                    white-space: pre-line;
                                    }
                                    h1 { margin: 0 0 12px; }
                                    table { border-collapse: collapse; width: 100%; }
                                    th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
                                    th { background: #f5f5f5; position: sticky; top: 0; z-index: 1; }
                                    tr:nth-child(even) { background: #fafafa; }
                                    .ok { background: #e9f7ef; color: #1e7e34; font-weight: 600; text-align: center; }
                                    .no { background: #fdecea; color: #b02a37; font-weight: 600; text-align: center; }
                                    .score { font-weight: 700; text-align: center; }
                                    a { color: #0b66c3; text-decoration: none; }
                                    a:hover { text-decoration: underline; }
                                    .wrap { word-break: break-word; }
                                    .score-high {
                                    background-color: #e6f4ea;
                                    color: #1e7e34;
                                    font-weight: bold;
                                    text-align: center;
                                    }
                                    .score-medium {
                                    background-color: #fff4e5;
                                    color: #b26a00;
                                    font-weight: bold;
                                    text-align: center;
                                    }
                                    .score-low {
                                    background-color: #fdecea;
                                    color: #b02a37;
                                    font-weight: bold;
                                    text-align: center;
                                    }
                            </style>
                        </head>
                        <body>
                            <div class="page">
                                <img class="logo" src="../pictures/gymbeam-logo.png" alt="GymBeam" />

                            <div class="text">
                            <h1>GEO Audit Report</h1>
                            <div style="overflow:auto;">
                            <table>
                            <thead>
                            <tr>""")

        # header row
        for col in columns_order:
            parts.append(f"<th>{html.escape(col)}</th>")
        parts.append("</tr></thead><tbody>")

        # data rows
        for row in rows:
            parts.append("<tr>")
            for col in columns_order:
                val = row.get(col, "")

                # custom formatting for url, title, score
                if col == "url":
                    url = str(val)
                    safe_url = html.escape(url)
                    parts.append(
                        f'<td class="wrap"><a href="{safe_url}" target="_blank" rel="noopener noreferrer">{safe_url}</a></td>'
                    )
                elif col == "title":
                    parts.append(f'<td class="wrap">{html.escape(str(val))}</td>')
                elif col == "score":
                    parts.append(score_cell(val))
                else:
                    parts.append(cell(val))
            parts.append("</tr>")

        parts.append("""</tbody>
                        </table>
                        </div>
                        <div>
                     """)
        
        sum = 0
        counts = 0 

        for output in self.outputs:
            sum += output["score"]
            counts +=1
        
        average_score = sum / counts

        parts.append("""<h2>Priemerné skóre článkov z tabuľky je <b>""")

        parts.append(str(round(average_score,2)))

        parts.append("""</b> bodov </h2>
                        </div>
                        </div>
                        </body>
                        </html>""")

        with open(path, "w", encoding="utf-8") as f:
            f.write("".join(parts))

        print(f"HTML report uložený: {path}")

