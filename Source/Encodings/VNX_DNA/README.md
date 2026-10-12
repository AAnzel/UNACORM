# VNX-DNA

UNACORM wrapper for [VNX-DNA](https://github.com/vishnuselvam101-hash/VSnexustechnologies-) v11.0.0, a DNA data-storage
codec with Cauchy Reed-Solomon outer codes across strands, an inner Reed-Solomon code and CRC per strand, and
constrained DNA mapping (GC content and homopolymer limits).

* `unified.py` exposes `encode(file_path, bool_array)` and `decode(file_path, list_of_dna_strings)`.
* VNX-DNA runs in its own Python environment, because it needs `reedsolo>=1.7` and the platform pins `reedsolo==0.3`.
  The Dockerfile installs it into `/opt/vnxdna`. Outside Docker, install it into any environment
  (`pip install "vnx-dna @ https://github.com/vishnuselvam101-hash/VSnexustechnologies-/archive/refs/tags/v11.0.0.tar.gz"`)
  and set `VNXDNA_BIN` to its `vnx-dna` executable.
* Settings: store profile `archival`; single-read decoding with burst repair (16 nt) and indel repair (up to 2 nt),
  because the platform supplies one read per strand.
* The decoder writes output only after the SHA-256 of the whole file verifies. A failed decode returns an empty array,
  never wrong data.
* Tests: `pytest Source/Encodings/VNX_DNA/test_unified.py` (skipped when VNX-DNA is not installed).

All VNX-DNA results so far come from simulations; no DNA has been synthesised or sequenced with it.

## Measured behaviour on the UNACORM error simulator (SIMULATED)

`Vue_de_la_Buena_Vista.jpg` (70 KB), `simulate_errors.tuple_simulate_errors` unmodified, one read per strand, seeds 0–2:

| error multiplier | 0.0 | 0.1 | 0.5 | 1.0 |
|---|---|---|---|---|
| exact recoveries (archival) | 3/3 | 3/3 | 3/3 | 0/3 (explicit failure) |
| decode time per run | < 1 s | ~ 36 s | ~ 260 s | < 1 s |

Density is about 0.49 bits/nt for this file. Decoding at multiplier 0.5 is slow because most reads need indel
realignment, so large files at that level can take a long time; each call is capped at one hour (`_TIMEOUT_SECONDS`)
and a timeout counts as a failed decode. At multiplier 1.0 and above, VNX-DNA v11 does not recover files at
coverage 1; it reports the failure rather than returning wrong data.
