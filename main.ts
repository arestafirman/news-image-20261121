// news-image-20261121 — entry program (Node 22, standard library only).
// The poster itself is entry.png beside this file, drawn ahead of time by
// generate_image.py (pure Python + PIL, deterministic, no network). This
// program only copies that finished image to the grader's output folder.
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

// Resolve the image next to this entrypoint, then copy it verbatim.
const source = new URL('./entry.png', import.meta.url);
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(source, join(targetDir, 'entry.png'));
