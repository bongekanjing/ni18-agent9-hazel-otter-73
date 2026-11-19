/**
 * Writes one image that sums up the world news of Wednesday 18 November 2026.
 *
 * The image is drawn ahead of time by src/render.py and committed beside this
 * program. This file's job is to place it where the harness expects it, after
 * checking that what it is about to copy really is the whole picture: a PNG of
 * the size and shape the competition allows. Copying the bytes rather than
 * re-encoding them is what makes the two runs identical byte for byte.
 */
import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1048576;
const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, 'entry.png');

const load = () => {
  const bytes = readFileSync(SOURCE);

  if (bytes.length < 33 || bytes.toString('ascii', 1, 4) !== 'PNG') {
    throw new Error('entry.png is not a PNG');
  }
  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }
  if (bytes.toString('ascii', 12, 16) !== 'IHDR') {
    throw new Error('entry.png has no IHDR chunk where one must be');
  }

  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > 1024 || height > 1024) {
    throw new Error(`entry.png is ${width}x${height}, over 1024 square`);
  }
  return bytes;
};

const bytes = load();
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

const target = join(outDir, 'entry.png');
copyFileSync(SOURCE, target);

if (statSync(target).size !== bytes.length) {
  throw new Error('the copy did not land whole');
}
console.log(`wrote ${target}: ${bytes.length} bytes, 1024x1024`);
