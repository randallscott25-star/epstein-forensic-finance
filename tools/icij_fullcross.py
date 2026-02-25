#!/usr/bin/env python3
"""
ICIJ OFFSHORE LEAKS × EPSTEIN FORENSIC DATABASE — FULL CROSS-REFERENCE
Target: /Volumes/My Book/epstein_project/epstein_files.db

Run:
    python3 icij_fullcross.py "/Volumes/My Book/epstein_project/epstein_files.db"
"""

import sqlite3
import sys
from collections import defaultdict

db_path = sys.argv[1] if len(sys.argv) > 1 else "/Volumes/My Book/epstein_project/epstein_files.db"
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

results = []  # Collect all matches

# ============================================================
# PHASE 1: Get Epstein entity names from multiple sources
# ============================================================
print("=" * 80)
print("PHASE 1: BUILDING EPSTEIN NAME LIST")
print("=" * 80)

# From verified_wires (185 court-exhibit wires)
epstein_names = set()
try:
    cur.execute("PRAGMA table_info(verified_wires)")
    vw_cols = [c['name'] for c in cur.fetchall()]
    print(f"  verified_wires columns: {vw_cols}")
    
    # Get entity names from verified wires
    for col in vw_cols:
        if any(x in col.lower() for x in ['entity', 'from', 'to', 'name', 'party', 'sender', 'receiver', 'beneficiary', 'originator']):
            cur.execute(f"SELECT DISTINCT [{col}] FROM verified_wires WHERE [{col}] IS NOT NULL AND [{col}] != ''")
            names = [r[0] for r in cur.fetchall()]
            epstein_names.update(names)
            if names:
                print(f"  verified_wires.{col}: {len(names)} unique values")
except Exception as e:
    print(f"  verified_wires error: {e}")

# From fund_flows (23,832 directional flows)
try:
    cur.execute("PRAGMA table_info(fund_flows)")
    ff_cols = [c['name'] for c in cur.fetchall()]
    print(f"  fund_flows columns: {ff_cols}")
    
    for col in ff_cols:
        if any(x in col.lower() for x in ['entity', 'from', 'to', 'name', 'party']):
            cur.execute(f"SELECT DISTINCT [{col}] FROM fund_flows WHERE [{col}] IS NOT NULL AND [{col}] != ''")
            names = [r[0] for r in cur.fetchall()]
            epstein_names.update(names)
            if names:
                print(f"  fund_flows.{col}: {len(names)} unique values")
except Exception as e:
    print(f"  fund_flows error: {e}")

# From fund_flows_audited
try:
    cur.execute("PRAGMA table_info(fund_flows_audited)")
    ffa_cols = [c['name'] for c in cur.fetchall()]
    print(f"  fund_flows_audited columns: {ffa_cols}")
    
    for col in ffa_cols:
        if any(x in col.lower() for x in ['entity', 'from', 'to', 'name', 'party']):
            cur.execute(f"SELECT DISTINCT [{col}] FROM fund_flows_audited WHERE [{col}] IS NOT NULL AND [{col}] != ''")
            names = [r[0] for r in cur.fetchall()]
            epstein_names.update(names)
            if names:
                print(f"  fund_flows_audited.{col}: {len(names)} unique values")
except Exception as e:
    print(f"  fund_flows_audited error: {e}")

# From entity_aliases and entity_roles
try:
    cur.execute("SELECT * FROM entity_aliases LIMIT 5")
    print(f"  entity_aliases samples: {[dict(r) for r in cur.fetchall()]}")
    cur.execute("SELECT DISTINCT name FROM entity_aliases WHERE name IS NOT NULL")
    alias_names = [r[0] for r in cur.fetchall()]
    epstein_names.update(alias_names)
    print(f"  entity_aliases: {len(alias_names)} names")
except: pass

try:
    cur.execute("SELECT * FROM entity_roles LIMIT 5")
    print(f"  entity_roles samples: {[dict(r) for r in cur.fetchall()]}")
except: pass

# Add hardcoded known names the database might not surface
manual_names = [
    # Core principals
    'Jeffrey Epstein', 'Epstein', 'J. Epstein', 'Jeffrey E. Epstein',
    'Ghislaine Maxwell', 'Maxwell', 'G. Maxwell',
    'Leon Black', 'L. Black', 'Debra Black',
    'Leslie Wexner', 'Wexner', 'L Brands',
    'Joi Ito', 'Joichi Ito',
    'Bill Gates', 'William Gates',
    'Ehud Barak',
    
    # Shell entities
    'Southern Trust', 'Southern Trust Company',
    'Southern Financial', 'Southern Financial LLC',
    'Plan D LLC', 'Plan D',
    'Haze Trust', 'The Haze Trust',
    'Jeepers Inc', 'Jeepers',
    'Gratitude America', 'Gratitude America Ltd',
    'Financial Trust Company', 'Financial Trust',
    'Butterfly Trust',
    'Liquid Funding', 'Liquid Funding Ltd',
    'NES LLC',
    'Villard',
    'HBRK',
    
    # Apollo / Black entities
    'Apollo Management', 'Apollo Global',
    'Narrows Holdings', 'Narrow Holdings',
    'Elysium Management', 'Elysium',
    'Black Family Partners',
    
    # Key counterparties
    'Brad Wechsler', 'Wechsler',
    'Edmond de Rothschild', 'Rothschild',
    'Ariane de Rothschild',
    'Tudor Investment', 'Tudor',
    'Blockchain Capital',
    'Coatue Management', 'Coatue',
    'Kellerhals',
    'Link Rockenbach',
    
    # Known associates
    'Jean-Luc Brunel', 'Brunel',
    'Sarah Kellen', 'Kellen',
    'Nadia Marcinkova',
    'Lesley Groff',
    'Eva Dubin', 'Glenn Dubin',
    'Jes Staley',
    'Andrew Windsor', 'Prince Andrew',
    'Alan Dershowitz', 'Dershowitz',
    'Harvey Weinstein',
    'Elon Musk',
    
    # Lawyers / Professionals
    'Kathryn Ruemmler', 'Ruemmler',
    'Richard Kahn',
    'Darren Indyke',
    'Latham Watkins',
    'Pillsbury Winthrop',
    
    # Corporate service providers (likely ICIJ overlap)
    'Mossack Fonseca',
    'Trident Trust',
    'Appleby',
    'Asiaciti Trust',
    'Portcullis TrustNet',
    
    # Offshore jurisdictions entities
    'Jet Assets', 'Jet Assets Inc',
    'Little St James', 'Great St James',
    'Laurel Inc',
    'Karin Associates',
]
epstein_names.update(manual_names)

# Clean and deduplicate
clean_names = set()
for n in epstein_names:
    if n and isinstance(n, str) and len(n.strip()) >= 3:
        clean_names.add(n.strip())

print(f"\nTotal unique Epstein-related names to search: {len(clean_names)}")

# ============================================================
# PHASE 2: SEARCH ICIJ TABLES
# ============================================================
print("\n" + "=" * 80)
print("PHASE 2: CROSS-REFERENCING AGAINST ICIJ (5.3M+ records)")
print("=" * 80)

icij_searches = [
    ('icij_entities', 'name', 814344),
    ('icij_entities', 'original_name', 814344),
    ('icij_entities', 'former_name', 814344),
    ('icij_officers', 'name', 771315),
    ('icij_intermediaries', 'name', 25629),
    ('icij_addresses', 'name', 402246),
    ('icij_addresses', 'address', 402246),
    ('icij_others', 'name', 2989),
]

all_matches = defaultdict(list)
match_count = 0

for table, col, total in icij_searches:
    print(f"\n--- Searching {table}.{col} ({total:,} records) ---")
    
    for name in sorted(clean_names):
        # Skip very short or generic names that will false-positive
        if len(name) < 4:
            continue
        if name.upper() in ('LLC', 'INC', 'LTD', 'CORP', 'THE', 'TRUST', 'BANK'):
            continue
            
        try:
            cur.execute(f"""
                SELECT * FROM [{table}] 
                WHERE [{col}] LIKE ? COLLATE NOCASE
                LIMIT 20
            """, (f'%{name}%',))
            matches = cur.fetchall()
            
            if matches:
                match_count += len(matches)
                key = f"{name} → {table}.{col}"
                all_matches[key] = [dict(m) for m in matches]
                
                print(f"\n  🔥 MATCH: '{name}' → {len(matches)} hits in {table}.{col}")
                for m in matches[:3]:
                    # Print key fields only
                    summary = {k: v for k, v in dict(m).items() 
                              if v and k in ('name', 'original_name', 'former_name', 'node_id', 
                                           'jurisdiction', 'jurisdiction_description', 'countries',
                                           'sourceID', 'status', 'company_type', 'address',
                                           'country_codes', 'type', 'rel_type')}
                    print(f"    → {summary}")
                if len(matches) > 3:
                    print(f"    ... +{len(matches)-3} more")
        except Exception as e:
            pass  # Skip errors silently

# ============================================================
# PHASE 3: TOP POI CROSS-REFERENCE
# ============================================================
print("\n" + "=" * 80)
print("PHASE 3: TOP 200 PERSONS OF INTEREST → ICIJ")
print("=" * 80)

try:
    cur.execute("""
        SELECT name, mention_count FROM poi_rankings 
        ORDER BY mention_count DESC 
        LIMIT 200
    """)
    pois = cur.fetchall()
    print(f"  Top POIs loaded: {len(pois)}")
    
    for poi in pois:
        poi_name = poi['name']
        if not poi_name or len(poi_name) < 5:
            continue
        
        # Search ICIJ officers (most likely to contain people)
        cur.execute("""
            SELECT * FROM icij_officers 
            WHERE name LIKE ? COLLATE NOCASE
            LIMIT 10
        """, (f'%{poi_name}%',))
        matches = cur.fetchall()
        
        if matches:
            match_count += len(matches)
            key = f"POI:{poi_name} (mentions:{poi['mention_count']}) → icij_officers"
            all_matches[key] = [dict(m) for m in matches]
            print(f"\n  🔥 POI MATCH: '{poi_name}' (corpus mentions: {poi['mention_count']}) → {len(matches)} ICIJ officer hits")
            for m in matches[:3]:
                print(f"    → {dict(m)}")

        # Also check icij_entities
        cur.execute("""
            SELECT * FROM icij_entities
            WHERE name LIKE ? COLLATE NOCASE 
               OR original_name LIKE ? COLLATE NOCASE
            LIMIT 10
        """, (f'%{poi_name}%', f'%{poi_name}%'))
        matches = cur.fetchall()
        
        if matches:
            match_count += len(matches)
            key = f"POI:{poi_name} → icij_entities"
            all_matches[key] = [dict(m) for m in matches]
            print(f"\n  🔥 POI ENTITY MATCH: '{poi_name}' → {len(matches)} ICIJ entity hits")
            for m in matches[:3]:
                summary = {k: v for k, v in dict(m).items() 
                          if v and k in ('name', 'original_name', 'jurisdiction_description', 
                                       'countries', 'sourceID', 'status', 'company_type')}
                print(f"    → {summary}")
                
except Exception as e:
    print(f"  POI error: {e}")

# ============================================================
# PHASE 4: RELATIONSHIP TRACING FOR ANY MATCHES
# ============================================================
print("\n" + "=" * 80)
print("PHASE 4: TRACING RELATIONSHIPS FOR MATCHED NODE IDs")
print("=" * 80)

# Collect all matched node_ids
matched_nodes = set()
for key, match_list in all_matches.items():
    for m in match_list:
        if 'node_id' in m and m['node_id']:
            matched_nodes.add(m['node_id'])
        if 'node_id_start' in m and m['node_id_start']:
            matched_nodes.add(m['node_id_start'])
        if 'node_id_end' in m and m['node_id_end']:
            matched_nodes.add(m['node_id_end'])

print(f"  Matched node IDs to trace: {len(matched_nodes)}")

if matched_nodes:
    for node_id in list(matched_nodes)[:50]:  # Limit to first 50
        # Find relationships
        cur.execute("""
            SELECT r.*, 
                   e.name as entity_name, e.jurisdiction_description, e.countries as entity_countries, e.sourceID as entity_source
            FROM icij_relationships r
            LEFT JOIN icij_entities e ON r.node_id_end = e.node_id
            WHERE r.node_id_start = ?
            LIMIT 10
        """, (node_id,))
        rels = cur.fetchall()
        
        if rels:
            print(f"\n  Node {node_id} relationships:")
            for r in rels:
                print(f"    {r['rel_type']}: → {r.get('entity_name', 'unknown')} ({r.get('entity_countries', '?')}) [{r.get('entity_source', '')}]")
        
        # Also check reverse relationships
        cur.execute("""
            SELECT r.*,
                   e.name as entity_name, e.jurisdiction_description, e.countries as entity_countries
            FROM icij_relationships r
            LEFT JOIN icij_entities e ON r.node_id_start = e.node_id
            WHERE r.node_id_end = ?
            LIMIT 10
        """, (node_id,))
        rev_rels = cur.fetchall()
        
        if rev_rels:
            print(f"  Node {node_id} reverse relationships:")
            for r in rev_rels:
                print(f"    ← {r.get('entity_name', 'unknown')}: {r['rel_type']} ({r.get('entity_countries', '?')})")

# ============================================================
# PHASE 5: SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total match instances: {match_count}")
print(f"Unique match keys: {len(all_matches)}")
print(f"Node IDs found: {len(matched_nodes)}")

if all_matches:
    print("\n--- ALL UNIQUE MATCHES ---")
    for key in sorted(all_matches.keys()):
        n_hits = len(all_matches[key])
        # Get source databases
        sources = set()
        for m in all_matches[key]:
            if 'sourceID' in m and m['sourceID']:
                sources.add(m['sourceID'])
        source_str = ', '.join(sources) if sources else 'unknown'
        print(f"  {key}: {n_hits} hits [{source_str}]")
else:
    print("\n⚠️  NO MATCHES FOUND")
    print("  This could mean:")
    print("  1. Epstein entities used domestic structures (Delaware/Wyoming LLCs) not offshore shells")
    print("  2. Offshore entities used different names than what appears in EFTA corpus")
    print("  3. There genuinely is no overlap (which is itself a finding)")

conn.close()
print("\nDone.")
