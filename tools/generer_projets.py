#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere les projets de rappel (JSON, meme format que 01.json) a partir des
"مستخرج من مقرر الترقية" (fichiers .txt, encodage Windows-1256), un projet par سلك.
Les dates d'effet et les nouvelles echelons sont LUS dans les extraits : rien n'est saisi a la main.

Usage :
  python3 tools/generer_projets.py [--modele 01.json] [--sortie projets] extrait1.txt extrait2.txt ...
"""
import re, sys, json, os, argparse, collections

def norm(s):
    s = re.sub(r'[ـً-ْ‏‎]', '', s or '')
    s = s.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ى', 'ي').replace('ة', 'ه')
    return re.sub(r'\s+', '', s)

def read_text(fn):
    b = open(fn, 'rb').read()
    for enc in ('utf-8-sig', 'cp1256'):
        try:
            return b.decode(enc).replace('‏', '')
        except UnicodeDecodeError:
            pass
    return b.decode('cp1256', errors='replace').replace('‏', '')

def parse_extract(fn):
    t = read_text(fn)
    parts = [x for x in re.split(r'(?=الجمهورية الجزائرية)', t) if 'سلك' in x and re.search(r'(?:السيد|السيدة|الآنسة|الانسة)\s*:', x)]
    out = []
    for r in parts:
        g = lambda pat, s=r: (re.search(pat, s) or [None, None])[1]
        m0 = re.search(r'(?:[تي])?رقى\s+وفقا', r)
        cur, prom = (r[:m0.start()], r[m0.end():]) if m0 else (r, '')
        name = re.sub(r'\s+', ' ', re.sub(r'ـ', '', g(r'(?:السيدة|السيد|الآنسة|الانسة)\s*:\s*(.+)') or '')).strip()
        out.append(dict(
            fichier=os.path.basename(fn),
            corps=re.sub(r'\s+', ' ', (g(r'سلك\s*:\s*(.+)') or '').strip()),
            grade=re.sub(r'\s+', ' ', (g(r'رتبة\s*:\s*(.+)') or '').strip()),
            nom=name,
            decision=g(r'رقم\s*:\s*(\d+)'),
            ech_cur=g(r'الدرجة\s*:\s*(\d+)', cur),
            ech_new=g(r'الدرجة\s*:\s*(\d+)', prom),
            eff_new=g(r'تاريخ السريان\s*:\s*(\d\d/\d\d/\d{4})', prom),
        ))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--modele', default='01.json')
    ap.add_argument('--sortie', default='projets')
    ap.add_argument('--premier', default=2, type=int, help='numero du premier nouveau projet')
    ap.add_argument('fichiers', nargs='+')
    a = ap.parse_args()
    model = json.load(open(a.modele, encoding='utf-8'))
    recs = []
    for f in a.fichiers:
        recs += parse_extract(f)
    os.makedirs(a.sortie, exist_ok=True)
    problems = []
    for r in recs:
        if not (r['ech_new'] and r['eff_new']):
            problems.append('%s : promotion illisible' % r['nom'])
    recs = [r for r in recs if r['ech_new'] and r['eff_new']]

    # 1) agents deja connus du modele (corps du modele) : meme nom exact, ou meme (echelon, date) que la saisie manuelle
    by = collections.defaultdict(list)
    for ag in model['agents']:
        by[norm(ag['nom'])].append(ag)
    def toks(z):
        return [norm(w) for w in re.split(r'[\s/]+', z) if w]
    def subset(x, y):  # tous les mots du nom le plus court figurent dans l'autre (>= 2 mots)
        A, B = toks(x), toks(y)
        S, L = (A, B) if len(A) <= len(B) else (B, A)
        return len(S) >= 2 and all(w in L for w in S)
    def sim(x, y):
        x, y = norm(x), norm(y)
        if not x or not y: return 0
        m, n = len(x), len(y); p = list(range(n + 1))
        for ii in range(1, m + 1):
            prev = p[0]; p[0] = ii
            for jj in range(1, n + 1):
                t = p[jj]; p[jj] = min(p[jj] + 1, p[jj - 1] + 1, prev + (x[ii - 1] != y[jj - 1])); prev = t
        return 1 - p[n] / max(m, n)
    known = {}
    used = set()
    # A) agents deja traites a la main par l'utilisateur (inclus, avec date) : meme echelon + meme date + nom identique ou proche
    manual = [ag for ag in model['agents'] if ag.get('inclure') and ag.get('dateEffet')]
    for i, r in enumerate(recs):
        cand = [ag for ag in manual if id(ag) not in used and ag['dateEffet'] == r['eff_new'] and int(ag['nouvelEch'] or -1) == int(r['ech_new'])
                and (norm(ag['nom']) == norm(r['nom']) or sim(ag['nom'], r['nom']) >= 0.7 or subset(ag['nom'], r['nom']))]
        if len(cand) == 1:
            known[i] = cand[0]; used.add(id(cand[0]))
    # B) meme nom exact, unique dans le modele
    for i, r in enumerate(recs):
        if i in known:
            continue
        c = [ag for ag in by.get(norm(r['nom']), []) if id(ag) not in used]
        if len(c) == 1:
            known[i] = c[0]; used.add(id(c[0]))

    # 2) projet mis a jour du corps du modele : dates lues dans les extraits
    upd = json.loads(json.dumps(model))
    diffs = []
    index = {ag['mat']: ag for ag in upd['agents']}
    nb_new = 0
    for i, ag in known.items():
        r = recs[i]
        t = index[ag['mat']]
        old = (t['nouvelEch'], t['dateEffet'], t['inclure'])
        t['nouvelEch'] = str(int(r['ech_new']))
        t['dateEffet'] = r['eff_new']
        t['inclure'] = True
        if old[1] and (old[1] != t['dateEffet'] or int(old[0] or -1) != int(t['nouvelEch'])):
            diffs.append('%s %s : saisi %s / %s -> extrait %s / %s' % (t['mat'], t['nom'], old[0], old[1], t['nouvelEch'], t['dateEffet']))
        if not old[1]:
            nb_new += 1
    upd['date'] = '2026-11-23T00:00:00.000Z'
    upd['calcule'] = False
    write_project(os.path.join(a.sortie, '01.json'), upd)

    # 3) un projet par CORPS de la base (et non par intitule de grade du decision) ; les paramedicaux (corps du modele) restent dans le projet 01
    CORPS = collections.OrderedDict([
        ('800', 'Biologistes S.P'), ('1200', 'Psychologues de santé publique'), ('1100', 'Auxiliaires médicaux en anesthesie - réanimation de santé publique'),
        ('1000', 'Sages femmes de sante publique'), ('100', 'Praticiens Médicaux'), ('1400', 'Praticiens médicaux spécialistes s.p')])
    def corps_code(t):
        if 'التخذير' in t or 'التخدير' in t: return '1100'
        if 'البيولوجي' in t: return '800'
        if 'النفساني' in t: return '1200'
        if 'القابلات' in t: return '1000'
        if 'المتخصصين' in t: return '1400'
        if 'الممارسين' in t: return '100'
        return model['filtres'].get('corps') or '200'      # infirmiers, aides-soignants, laborantins... = paramedicaux
    fin = model['agents'][0]['fin'] if model['agents'] else '12/2026'
    def mk(r):
        return dict(mat='', nom=r['nom'], inclure=True, nouvelEch=str(int(r['ech_new'])), dateEffet=r['eff_new'], fin=fin, ech2='', date2='', bulletinRef='')
    extra = collections.defaultdict(list)
    for i, r in enumerate(recs):
        if i not in known:
            extra[corps_code(r['corps'])].append(r)
    base_code = model['filtres'].get('corps') or '200'
    n_extra = len(extra.get(base_code, []))
    if n_extra:
        upd['agents'] += [mk(r) for r in sorted(extra[base_code], key=lambda z: z['nom'])]
        write_project(os.path.join(a.sortie, '01.json'), upd)
    summary = []
    k = a.premier
    for code, label in CORPS.items():
        lst = extra.get(code)
        if not lst:
            continue
        no = '%02d' % k; k += 1
        pr = json.loads(json.dumps(model))
        pr['no'] = no
        pr['titre'] = ''
        pr['date'] = '2026-11-23T00:00:00.000Z'
        pr['calcule'] = False
        pr['filtres'] = dict(pr['filtres'], corps=code, matricules='')
        pr['filtresListe'] = dict(corps=code, matricules='')
        pr['corpsNom'] = label
        pr['source'] = sorted(set(x['fichier'] for x in lst))
        pr['rapprochement'] = 'noms'
        pr['agents'] = [mk(x) for x in sorted(lst, key=lambda z: z['nom'])]
        write_project(os.path.join(a.sortie, no + '.json'), pr)
        summary.append((no, '%s [%s]' % (label, code), len(lst)))
    if n_extra:
        summary.insert(0, ('01', 'Paramedicaux [%s] : %d agents ajoutes par nom' % (base_code, n_extra), len(upd['agents'])))
    matched_ids = set(id(v) for v in known.values())
    for ag in model['agents']:
        if ag.get('inclure') and ag.get('dateEffet') and ag['mat'] in index and id(ag) not in matched_ids:
            poss = [r for r in recs if r['eff_new'] == ag['dateEffet'] and int(r['ech_new']) == int(ag['nouvelEch'] or -1) and r['nom'].split()[:1] == ag['nom'].split()[:1]]
            print('  A VERIFIER : %s %s (saisi %s / %s) non retrouve dans les extraits%s' % (ag['mat'], ag['nom'], ag['nouvelEch'], ag['dateEffet'], (' ; meme premier mot, meme echelon et meme date : ' + ' / '.join(x['nom'] for x in poss)) if poss else ''))
    for p in problems:
        print('PROBLEME :', p)

def write_project(path, pr):
    head = {k: v for k, v in pr.items() if k != 'agents'}
    txt = json.dumps(head, ensure_ascii=False, indent=1)
    lines = [json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in pr['agents']]
    txt = txt[:-2] + ',\n "agents": [\n' + ',\n'.join(lines) + '\n ]\n}\n'
    open(path, 'w', encoding='utf-8', newline='\n').write(txt)

if __name__ == '__main__':
    main()
