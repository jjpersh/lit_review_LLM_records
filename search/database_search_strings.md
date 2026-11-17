# Manual database searches (run with BYU library access)

Run these yourself in **Scopus, Web of Science Core Collection and IEEE Xplore**. These databases were not
reachable from the Claude session (subscription only). Same window as the rest of the review:
**2022-11-01 to the day you run it**. Write the run date and the hit count for each query in the table at the bottom.

Each search has two blocks:
- **Block L (LLM terms):** the same LLM synonyms as the 14 Oct and 28 Oct searches.
- **Block P (process-control terms):** the union of the control/process terms used across the 25 topic queries
  in `logs/search_log_20261014.csv`.

Q1 is the main search (sensitive). Q2–Q4 are narrower checks that should come back almost entirely as
duplicates of Q1. If they turn up much that Q1 missed, tell me.

---

## Scopus (Advanced search)

**Q1 — main**
```
TITLE-ABS-KEY ( "large language model*" OR llm OR llms OR chatgpt OR "gpt-4*" OR "gpt-3*" OR "vision-language model*"
  OR "multimodal large language model*" OR "llm agent*" OR "language model agent*" OR "foundation model*"
  OR "generative AI" OR "small language model*" )
AND TITLE-ABS-KEY ( "process control" OR "control loop*" OR "closed-loop control" OR "model predictive control"
  OR mpc OR pid OR "controller tuning" OR "controller design" OR setpoint OR "set-point" OR "supervisory control"
  OR "real-time optimization" OR plc OR "IEC 61131" OR "structured text" OR "ladder logic" OR "control logic"
  OR scada OR "distributed control system" OR dcs OR "OPC UA" OR "industrial automation" OR "industrial control"
  OR "fault detection" OR "fault diagnosis" OR "root cause" OR "process monitoring" OR "alarm management"
  OR "abnormal situation" OR "operator support" OR "control room" OR "Tennessee Eastman" OR tclab
  OR "temperature control lab" OR "quadruple tank" OR "four-tank" OR cstr OR "continuous stirred tank"
  OR "soft sensor" OR "system identification" OR "digital twin" OR "chemical process*" OR "chemical plant*"
  OR "process industr*" OR bioprocess OR bioreactor OR fermentation OR crystalli* OR "pharmaceutical manufacturing"
  OR "continuous manufacturing" OR "wastewater treatment" OR "water treatment" OR distillation OR refiner*
  OR boiler OR "batch process*" OR "batch control" OR "ISA-88" OR "P&ID" OR "piping and instrumentation" )
AND PUBYEAR > 2021 AND ( LIMIT-TO ( LANGUAGE , "English" ) )
```
After running, set the date filter to start at Nov 2022: drop the 2022 records dated before November when you
screen. Scopus's PUBYEAR can't filter by month.

**Q2 — closed-loop / supervisory check**
```
TITLE-ABS-KEY ( "large language model*" OR llm OR llms OR "llm agent*" OR agentic )
AND TITLE-ABS-KEY ( "process control" OR "closed-loop" OR "supervisory control" OR "model predictive control"
  OR "fault-tolerant control" OR "setpoint" ) AND PUBYEAR > 2021
```

**Q3 — PLC / automation engineering check**
```
TITLE-ABS-KEY ( "large language model*" OR llm OR llms OR chatgpt OR "gpt-4*" )
AND TITLE-ABS-KEY ( plc OR "IEC 61131" OR "structured text" OR "ladder logic" OR "control logic" )
AND PUBYEAR > 2021
```

**Q4 — process-domain check**
```
TITLE-ABS-KEY ( "large language model*" OR llm OR llms )
AND TITLE-ABS-KEY ( "chemical process*" OR "Tennessee Eastman" OR bioreactor OR crystalli* OR distillation
  OR "wastewater treatment" ) AND TITLE-ABS-KEY ( control OR monitoring OR "fault diagnosis" )
AND PUBYEAR > 2021
```

**Export:** Select all → Export → **CSV**, with *Citation information* plus *Abstract & keywords* ticked.
Save the file as `logs/manual_exports/scopus_Q1_YYYY-MM-DD.csv` (one file per query).

---

## Web of Science Core Collection (Advanced Search)

**Q1 — main** (TS = title, abstract, author keywords, Keywords Plus)
```
TS=("large language model*" OR LLM OR LLMs OR ChatGPT OR "GPT-4*" OR "GPT-3*" OR "vision-language model*"
  OR "multimodal large language model*" OR "LLM agent*" OR "language model agent*" OR "foundation model*"
  OR "generative AI" OR "small language model*")
AND TS=("process control" OR "control loop*" OR "closed-loop control" OR "model predictive control" OR MPC
  OR PID OR "controller tuning" OR "controller design" OR setpoint OR "set-point" OR "supervisory control"
  OR "real-time optimization" OR PLC OR "IEC 61131" OR "structured text" OR "ladder logic" OR "control logic"
  OR SCADA OR "distributed control system" OR DCS OR "OPC UA" OR "industrial automation" OR "industrial control"
  OR "fault detection" OR "fault diagnosis" OR "root cause" OR "process monitoring" OR "alarm management"
  OR "abnormal situation" OR "operator support" OR "control room" OR "Tennessee Eastman" OR TCLab
  OR "temperature control lab" OR "quadruple tank" OR "four-tank" OR CSTR OR "continuous stirred tank"
  OR "soft sensor" OR "system identification" OR "digital twin" OR "chemical process*" OR "chemical plant*"
  OR "process industr*" OR bioprocess OR bioreactor OR fermentation OR crystalli* OR "pharmaceutical manufacturing"
  OR "continuous manufacturing" OR "wastewater treatment" OR "water treatment" OR distillation OR refiner*
  OR boiler OR "batch process*" OR "batch control" OR "ISA-88" OR "P&ID" OR "piping and instrumentation")
```
Set Publication Date = **Custom 2022-11-01 to today**. Language = English.

Q2–Q4: same strings as the Scopus versions, with `TITLE-ABS-KEY` replaced by `TS=` and the `PUBYEAR` clause
removed (use the date setting instead).

**Export:** Export → **Excel** or **Tab delimited file**, Record content = **Full Record**. WoS exports at most
1,000 records per file, so export in 1–1000, 1001–2000 and so on if needed.
Save as `logs/manual_exports/wos_Q1_YYYY-MM-DD.xls` (or `.txt`).

---

## IEEE Xplore (Advanced Search → Command Search)

IEEE allows at most **40 search terms per query** (wildcards count). That's why Q1 is split into Q1a–Q1c here.
```
Q1a: ("All Metadata":"large language model*" OR "All Metadata":LLM OR "All Metadata":ChatGPT OR "All Metadata":"GPT-4" OR "All Metadata":"LLM agent*")
     AND ("All Metadata":"process control" OR "All Metadata":"model predictive control" OR "All Metadata":PID
     OR "All Metadata":"controller tuning" OR "All Metadata":"supervisory control" OR "All Metadata":setpoint
     OR "All Metadata":"closed-loop control" OR "All Metadata":"industrial control" OR "All Metadata":"digital twin")

Q1b: ("All Metadata":"large language model*" OR "All Metadata":LLM OR "All Metadata":ChatGPT OR "All Metadata":"GPT-4")
     AND ("All Metadata":PLC OR "All Metadata":"IEC 61131" OR "All Metadata":"structured text" OR "All Metadata":"ladder logic"
     OR "All Metadata":SCADA OR "All Metadata":DCS OR "All Metadata":"OPC UA" OR "All Metadata":"industrial automation")

Q1c: ("All Metadata":"large language model*" OR "All Metadata":LLM OR "All Metadata":ChatGPT)
     AND ("All Metadata":"fault diagnosis" OR "All Metadata":"fault detection" OR "All Metadata":"Tennessee Eastman"
     OR "All Metadata":"process monitoring" OR "All Metadata":alarm OR "All Metadata":"chemical process"
     OR "All Metadata":"soft sensor" OR "All Metadata":distillation OR "All Metadata":bioreactor OR "All Metadata":wastewater)
```
Filter Year: 2022–2026. Content types: Conferences, Journals, Early Access.

**Export:** Select all (all pages) → Export → **CSV**. Save as `logs/manual_exports/ieee_Q1a_YYYY-MM-DD.csv`
and so on.

---

## Drop-in import format

Put the raw exports in `logs/manual_exports/` **without editing them**. The import script reads the native column
names of each database:

| Database | Title | DOI | Year | Venue | Abstract |
|---|---|---|---|---|---|
| Scopus CSV | `Title` | `DOI` | `Year` | `Source title` | `Abstract` |
| WoS tab-delimited / Excel | `TI` / `Article Title` | `DI` / `DOI` | `PY` / `Publication Year` | `SO` / `Source Title` | `AB` / `Abstract` |
| IEEE CSV | `Document Title` | `DOI` | `Publication Year` | `Publication Title` | `Abstract` |

If you prefer to hand me a single merged file, use this header (UTF-8 CSV, one row per record):
```
database,query_id,run_date,title,doi,year,venue,abstract
Scopus,Q1,2026-10-29,"Title here",10.1016/j.xxx,2026,"Journal name","Abstract text..."
```
The file names give the database, query ID and run date, which is how each search gets logged in PRISMA.

## Run record (fill in)

| Database | Query | Run date | Hits | Exported file |
|---|---|---|---|---|
| Scopus | Q1 | | | |
| Scopus | Q2 | | | |
| Scopus | Q3 | | | |
| Scopus | Q4 | | | |
| WoS | Q1 | | | |
| WoS | Q2–Q4 | | | |
| IEEE Xplore | Q1a | | | |
| IEEE Xplore | Q1b | | | |
| IEEE Xplore | Q1c | | | |
