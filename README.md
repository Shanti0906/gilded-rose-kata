# Gilded Rose Kata

Refactored the update_quality logic and added support for Conjured items.

Before touching anything, I wrote tests against the original code to make sure
I wasn't going to break Aged Brie, Sulfuras, or Backstage passes while adding
the new item type.

The original `update_quality` had all item types crammed into one long nested
if/else, so I split it into one small updater class per item type so each one
just handles "how does this item changes in a day". Conjured items reuses the
normal item logic with double the degrade rate, so it ended up being a very
small addition once the rest was split out.

Didn't touch `Item` itself, per the instructions.

## Running the tests

1. Clone the repo and cd into it:
   ```
   git clone https://github.com/Shanti0906/gilded-rose-kata.git
   cd gilded-rose-kata
   ```
2. Install the one dependency (pytest):
   ```
   pip3 install -r requirements.txt
   ```
3. Run the tests:
   ```
   python3 -m pytest tests/ -v
   ```
   You should see 19 tests pass.

(Use `python`/`pip` instead of `python3`/`pip3` if that's how Python is set up
on your machine.)
