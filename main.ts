import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for make.fun news-image-20261122: copy the pre-rendered front page
// (drawn by build_image.py) to the output path the competition reads.
const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outDir, "entry.png"));
