# Issue #3 Investigation: "Transparent When Holding"

## Reproduction setup
1. Downloaded the texture pack linked in issue #3 comments (`furfsky.net` 1.21.x full pack):
   `https://cdn.modrinth.com/data/khMbd0K1/versions/OITsstM2/%C2%A7aFurf%C2%A7bSky%20%C2%A76Reborn%20%C2%A7f%C2%A7lFULL%C2%A7r%20%C2%A771.21.5%C2%A78.zip`.
2. Ran the repository code against the pack and analyzed output alpha channels.

## Findings

### 1) CUDA default path causes all images to fail on CPU-only machines
The script defaults to `use_cuda=True`. On systems without CUDA-enabled OpenCV runtime, this caused every image upscale call to fail.

### 2) Non-square RGBA textures were skipped due to swapped width/height in alpha resize
The previous code resized alpha using `(alpha.shape[0], alpha.shape[1])` as `(width, height)`.
OpenCV expects `(width, height)`, but `shape[0]` is height and `shape[1]` is width.
For non-square images, this produced merge-size mismatch errors and skipped files.

### 3) Binary alpha edges became semi-transparent after upscaling
For binary-alpha textures (common for held item/icon silhouettes), the previous code always used `INTER_CUBIC` on alpha.
This introduced semi-transparent edge pixels (`0 < alpha < 255`), which can manifest as transparent/fringed sides when held in-game.

Observed on a representative texture (`assets/minecraft/textures/gui/sprites/hud/crosshair.png`):
- Original alpha unique values: `{0, 255}` (no semi-transparent pixels).
- After old alpha upscaling path: 28 unique alpha levels, 212 semi-transparent pixels.
- With fixed binary-alpha handling: still `{0, 255}`, 0 semi-transparent pixels.

## Proposed solution
- Detect CUDA availability before selecting CUDA backend; otherwise use CPU.
- Fix alpha resize argument order to `(width, height)`.
- Preserve hard alpha edges for binary-alpha textures with `INTER_NEAREST`.
- Keep `INTER_CUBIC` for textures that already contain soft/semi-transparent alpha.

## Validation after patch
Using a mini-pack extracted from the downloaded Furfsky zip:
- Non-square RGBA texture upscaled successfully to the expected size.
- Binary-alpha texture remained binary after upscaling (no semi-transparent alpha pixels).
