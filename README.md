# The World in One Day — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/crisdion3006/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/crisdion3006/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page newspaper front page summing up the world's news of Sunday
22 November 2026, built for the [make.fun](https://make.fun) bounty
"Sum up 22 November's world news in one image".

## What is on the page

- **Hero — Ukraine:** Russia's biggest attack of the year so far, 110
  missiles and 400+ drones. Zelenskyy calls Putin a "killer" while Trump
  calls him a friend; Poland reports a Russian missile in its airspace.
- **Mexico:** FBI most-wanted drug lord "El Chapo Isidro" captured in a
  shoot-out; 11 killed in the operation.
- **Climate — COP31:** fossil-fuel fight stalls the deal; talks run into
  overtime in Antalya as the draft drops coal, oil and gas.
- **United States:** the FBI investigates an apparent breach of its
  National Crime Information Center database.
- **Middle East:** Iran strikes Bahrain and the Strait of Hormuz; the IRGC
  claims attacks on US radars.
- **Also today:** ICE arrests on a Seattle jet bridge, Jensen Huang quits
  Nvidia, a helicopter crash on Everest, and a boat sinking in Nigeria.

Every story was verified from reports published on 22 November 2026.

## How it is built

`build_image.py` draws the whole front page with Pillow (PIL): masthead,
night-sky hero with skyline and missile bursts, four story cards and the
also-today strip. It writes `entry.png` (1024×1024, under 1 MiB).

```sh
python3 build_image.py   # writes entry.png
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. Running it twice produces byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
