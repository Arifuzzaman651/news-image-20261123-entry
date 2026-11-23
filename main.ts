// News-image entry (Node 22, standard library only): the poster is the
// entry.png beside this file, drawn by render_poster.py from stories.json,
// and the program copies it to /output/entry.png. It refuses to run when
// the poster is missing, so a broken build fails loudly instead of
// submitting an empty output.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const poster = new URL('./entry.png', import.meta.url);
if (!existsSync(poster)) {
  throw new Error('entry.png is missing: run python3 render_poster.py first');
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(poster, join(outDir, 'entry.png'));
