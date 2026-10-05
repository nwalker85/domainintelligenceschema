/** DIS 1.7 demo — Turtle → Oxigraph → SPARQL CONSTRUCT → Cytoscape.  A view is a query. */
import fs from 'node:fs';
import oxigraph from 'oxigraph';

const DIS = 'https://schemas.domainintelligenceschema.org/dis/1.7.0/';
const BASES = { retail: 'https://dossier.ravenhelm.dev/retail/', dadjoke: 'https://dossier.example/dadjoke/' };

const store = new oxigraph.Store();
const load = (f, base) => store.load(fs.readFileSync(f, 'utf8'), { format: 'text/turtle', base_iri: base });
load('vocabulary/dis.ttl', DIS);
load('fixtures/retail.ttl', BASES.retail);
load('../turtle/dadjoke.ttl', BASES.dadjoke);

const views = {};
for (const q of fs.readdirSync('queries').filter(f => f.endsWith('.rq'))) {
  const name = q.replace(/^\d+-|\.rq$/g, '');
  const sparql = fs.readFileSync(`queries/${q}`, 'utf8');
  if (!/CONSTRUCT/i.test(sparql)) continue;
  views[name] = toCytoscape(store.query(sparql));
  console.error(`${name.padEnd(20)} ${views[name].filter(e=>!e.data.source).length} nodes, ${views[name].filter(e=>e.data.source).length} edges`);
}
fs.writeFileSync('demo/views.json', JSON.stringify(views, null, 2));

function toCytoscape(quads) {
  const short = (t) => { let v = t?.value || ''; for (const [,b] of Object.entries(BASES)) v = v.replace(b,''); return v.replace(DIS,'dis:').replace(/^https?:\/\/.*[/#]/,''); };
  const nodes = new Map(), edges = [], labels = new Map(), types = new Map();
  for (const q of quads) {
    const s = short(q.subject), o = short(q.object);
    const pIri = q.predicate.value, p = short(q.predicate);
    if (pIri === DIS + '__label') { labels.set(s, o); continue; }
    if (pIri.endsWith('22-rdf-syntax-ns#type')) { types.set(s, o); nodes.set(s, nodes.get(s) || {}); continue; }
    nodes.set(s, nodes.get(s) || {});
    if (q.object.termType === 'NamedNode') { nodes.set(o, nodes.get(o) || {}); edges.push({ data: { source: s, target: o, label: p } }); }
    else nodes.set(s, { ...nodes.get(s), [p]: o });
  }
  return [
    ...[...nodes.keys()].map(id => ({ data: { id, label: labels.get(id) || id, kind: (types.get(id)||'thing').replace('dis:',''), props: nodes.get(id) } })),
    ...edges,
  ];
}
