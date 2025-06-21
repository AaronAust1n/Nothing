# AGENTS.MD - Notes for Caretakers of the Whimsical Creature Generator

Greetings, esteemed Agent of Code! You have stumbled into the whimsical workshop where digital beasties are born. This document contains vital (and not-so-vital) information for tending to this peculiar codebase.

## The Lore of the Creatures

These creatures are not mere data; they are sparks of joyful nonsense. They emerge from the `random` module's deepest dreams, fueled by lists of peculiar adjectives and improbable scenarios. Treat them with the respect due to any being that might, for instance, sweat lemonade or believe it's a renowned detective.

Their ASCII forms are but crude representations of their magnificent, multi-dimensional selves. Do not judge a Zibber-Zob by its pixelated cover.

## Code Philosophy: Embrace the Quirk

*   **Randomness is Sacred:** The core of this generator is `random.choice()`. Protect it. Venerate it. Maybe leave it small offerings of perfectly shuffled data.
*   **Consistency is Overrated (Mostly):** While we strive for the ASCII art not to look like a catastrophic printer jam, perfect realism is not the goal. If a wing occasionally looks like a pretzel, or a tail seems to defy physics, consider it a feature, a testament to the creature's unique essence.
*   **Adding New Parts (A Sacred Rite):**
    *   **Textual Bits:** Feel free to add new prefixes, suffixes, abilities, or backstory elements to the lists in `creature_parts/`. The more, the merrier (and weirder).
    *   **ASCII Snippets:** The `ascii_art/parts_library.py` is your canvas for new visual forms. When adding new heads, bodies, etc., try to keep them roughly within the existing size paradigms, but don't be afraid to experiment. A creature with an absurdly tiny head on a giant body? Hilarious!
*   **The ASCII Art Engine (`ascii_art/engine.py`):** This is the magical loom that weaves parts together. Its logic is a delicate dance of padding, centering, and occasionally hopeful concatenation. If you modify it, do so with a playful heart and a backup of your work. The current tail and wing attachment logic is "good enough" - improvements are welcome but not at the cost of your sanity.

## Debugging Rituals

1.  Generate at least five (5) creatures.
2.  Observe their forms and read their tales aloud, preferably with a dramatic voice.
3.  If something is amiss, consult the `random` module. Is it feeling mischievous today?
4.  If a creature part is consistently missing or looks odd, check the corresponding list in `creature_parts/` or `ascii_art/parts_library.py`. Typos are the gremlins of this system.
5.  The `AsciiArtEngine`'s assembly logic can be a bit like herding cats. Use print statements liberally if a creature looks particularly discombobulated.

## Forbidden Actions

*   Making the creatures *too* sensible.
*   Removing all sources of glitter.
*   Trying to implement a blockchain for creature ownership (unless it's a *really* funny blockchain).

Thank you for your service to the cause of delightful nonsense! May your code compile and your creatures frolic.
