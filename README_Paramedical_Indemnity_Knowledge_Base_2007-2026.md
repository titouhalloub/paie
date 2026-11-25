# Algeria Public-Health Paramedical Indemnities — Legal Knowledge Base

**Release:** 1.0.0  
**Legal cutoff:** 25 November 2026  
**Jurisdiction:** Algeria  
**Primary data:** [JSON knowledge base](./Algeria_Paramedical_Indemnity_Knowledge_Base_2007-2026.json)  
**Salary grids:** [Algeria_Public_Service_Grids_Official_Extraction.json](./Algeria_Public_Service_Grids_Official_Extraction.json)

## Scope

This repository document records legal rules for allowances and indemnities relevant to public-health paramedical corps. It deliberately does **not** duplicate salary index grids, classifications, grades, or echelon tables. Use the linked grid extraction only to map a grade to its classification for the relevant period.

This is a research knowledge base, not an official consolidated code or legal opinion. It distinguishes verified historical rates from current rates and marks unresolved continuity, annex, and implementation questions explicitly.

## Critical correction: astreinte is not sujétion spéciale

The two French legal labels refer to distinct indemnities and must never be merged.

| Indemnity | Legal source | Period | Rate | Calculation base |
|---|---|---:|---:|---|
| **Indemnité d'astreinte paramédicale** (تعويض الإلزام شبه الطبي) | Decree 11-200, Art. 4; amended by 24-425 | 2008-01-01 to 2024-12-31 | **25%** | traitement (الراتب الرئيسي) |
| **Indemnité d'astreinte paramédicale** | Decree 24-425, effective 2025-01-01 | From 2025-01-01 | **40%** | traitement (الراتب الرئيسي) |
| **Indemnité de sujétion spéciale** (تعويض التبعة الخاصة) | Decree 91-113, amended by Presidential Decree 02-340 | From 2002-10-01 in the historical text | 45% for paramedical staff in hospitalisation services; 40% for medico-technical and extra-hospital services | salaire de base du grade d'origine (الراتب الأساسي للرتبة الأصلية) |

**Do not report 45%/40% as the astreinte rate.** Those rates belong to the distinct 91-113 special sujétion allowance. Whether that older allowance continued to coexist with the later special paramedical regime after 2008 is not conclusively established here; do not automatically add it to a current payroll calculation.

## Main 2011 regime and 2025 amendments

Decree 11-200 was published in Official Gazette No. 30 on 1 June 2011, but Article 15 gives it effect from **1 January 2008**.

| Item | 2008–2024 | From 2025-01-01 |
|---|---:|---:|
| Performance improvement | 0–30% of traitement, calculated monthly and paid quarterly | 0–35% of traitement, calculated monthly and paid quarterly |
| Paramedical astreinte | **25%** of traitement, monthly | **40%** of traitement, monthly |
| Support for paramedical activities | 30% for categories 10 and below; 25% for categories 11 and above | 55% for categories 10 and below; 50% for categories 12 and above |
| Technicity | 10% for categories 11 and above | 10% for categories 12 and above |

### Category 11 issue

The amended Article 5 in Decree 24-425 names categories **10 and below** and **12 and above**, but does not name category 11. The omission is recorded as unresolved. Do not infer a rate for category 11.

## Earlier / separate indemnities

The JSON file contains structured records for:

- Special sujétion (91-113, amended 02-340)
- Shift work (81-14, amended 88-220)
- Professional experience (85-58)
- Health-sector performance and service improvement (90-415, amended 02-337)
- Guard duty (97-437, amended 03-38; replaced by the 2013 framework in 13-195)
- Contagion risk (03-52)
- Incentives for specified isolated/underserved-area assignments and mobile teams (02-119)
- Pedagogical experience (91-269)
- Pedagogical documentation (02-330)
- Teaching/specialized-education qualification (03-495)

These are not universal entitlements. Some are historical, limited to specific posts or services, dependent on ministerial decisions or nominative lists, or have unresolved post-2011 continuity. The JSON records the exact known scope and uncertainty.

## Rules for AI agents and payroll implementations

1. Distinguish **astreinte paramédicale** from **sujétion spéciale**.
2. Apply astreinte at **25% of traitement from 2008 through 2024**, and **40% from 1 January 2025**.
3. Never substitute **salaire de base** for **traitement**, or vice versa.
4. A ceiling of 15% of payroll mass is not an individual employee's 15% rate.
5. A 25% headcount quota is not a 25% salary rate.
6. Do not generalize guard duty, contagion-risk, rural/mobile-team, pedagogical, or teaching-only indemnities to every paramedical employee.
7. Do not use the 2003 guard-duty table as a current amount after the 2013 Decree 13-195 framework.
8. Do not infer continued legal effect merely because a decree is absent from Decree 11-200 Article 14's repeal list.
9. Do not invent a category 11 support rate under the 2025 amended Article 5.
10. When an annex or implementing decision is not transcribed, return **unknown / requires source**, not a guessed value.

## Important unresolved research items

- Post-2008 continuity and interaction of Decree 91-113 / Presidential Decree 02-340 with the special 11-200 regime.
- Post-2011 continuity of Decree 02-119.
- Exact individual amount in the Decree 03-52 annex and any later changes.
- Full text and application of joint ministerial Decision 21/MS/CAB/MIN dated 25 March 1991 (90-415).
- Complete health-sector annex to Decree 03-495.
- Current guard annex amounts under Decree 13-195 for each paramedical grade.
- Authoritative correction or interpretation of category 11 omission in amended Article 5.
- Exhaustive Official Gazette audit of every issue after 30 December 2024 through 25 November 2026. This release does not claim such an audit was completed.

## Official primary sources

- [Decree 11-200 — Official Gazette No. 30/2011 (PDF)](https://www.joradp.dz/FTP/JO-FRANCAIS/2011/F2011030.pdf)
- [Decree 24-425 — Official Gazette No. 87/2024, Arabic official PDF](https://www.joradp.dz/FTP/jo-arabe/2024/A2024087.pdf)
- [Decree 91-113 — Official Gazette No. 22/1991](https://www.joradp.dz/FTP/Jo-Francais/1991/F1991022.pdf)
- [Presidential Decree 02-340 — Official Gazette No. 69/2002](https://www.joradp.dz/FTP/jo-francais/2002/F2002069.PDF)
- [Decree 81-14 — shift work](https://www.joradp.dz/FTP/Jo-Francais/1981/F1981005.pdf)
- [Decree 85-58 — professional experience](https://www.joradp.dz/FTP/Jo-Francais/1985/F1985013.pdf)
- [Decree 03-52 — contagion risk, Official Gazette No. 8/2003](https://www.joradp.dz/JO2000/2003/008/FP5.pdf)
- [Decree 13-195 — guard indemnity, Official Gazette No. 27/2013](https://www.joradp.dz/FTP/JO-FRANCAIS/2013/F2013027.pdf)

See the JSON `sources` array for the complete source register and the `open_issues` array for research gaps.

## Version history

- **1.0.0 — 2026-11-25:** Consolidated structured release; corrected the astreinte/sujétion confusion; added pre-2008 instruments and post-2011 transition rules; explicitly marked unresolved issues and category 11 gap.
