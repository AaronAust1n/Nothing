class CosmicSeedGenerator:
    """
    Generates a unique seed value based on a literary quote.
    This seed will be the genesis of each unique "Ephemeral Echo Garden."
    """

    def __init__(self, quote: str):
        self.quote = quote.strip()
        if not self.quote:
            raise ValueError("Quote cannot be empty.")

    def generate_master_seed(self, large_prime: int = 1_000_000_007) -> int:
        """
        Generates the master seed from the quote.

        The process involves:
        1. Calculating the sum of ASCII values of all characters in the quote.
        2. Multiplying by the number of words in the quote.
        3. Taking the result modulo a large prime number.

        Args:
            large_prime: A large prime number to use for the modulo operation.
                         Default is 1,000,000,007.

        Returns:
            The master_seed (integer).
        """
        if not self.quote:
            return 0 # Or raise an error, depending on desired behavior for empty string post-init

        ascii_sum = sum(ord(char) for char in self.quote)
        words = self.quote.split()
        num_words = len(words)

        if num_words == 0: # Should not happen if initial quote is not empty and stripped
            return ascii_sum % large_prime

        master_seed = (ascii_sum * num_words) % large_prime
        return master_seed

if __name__ == '__main__':
    # Example Usage
    quotes = [
        "In a utilitarian age, of all other times, it is a matter of grave importance that fairy tales should be respected.",
        "To be, or not to be, that is the question.",
        "The only way to get rid of a temptation is to yield to it.",
        "All that we see or seem is but a dream within a dream.",
        "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.",
        "  ", # Test emptyish string
        "Word" # Test single word
    ]

    for q in quotes:
        try:
            seed_generator = CosmicSeedGenerator(q)
            seed = seed_generator.generate_master_seed()
            print(f"Quote: \"{q[:50]}...\"")
            print(f"Master Seed: {seed}\n")
        except ValueError as e:
            print(f"Error for quote \"{q}\": {e}\n")

    # Test with a very specific known quote for reproducibility if needed
    specific_quote = "This is a test quote."
    # Expected sum(ord(c) for c in "This is a test quote.") = 1938
    # Expected len("This is a test quote.".split()) = 5
    # Expected (1938 * 5) % 1000000007 = 9690
    seed_generator_specific = CosmicSeedGenerator(specific_quote)
    specific_seed = seed_generator_specific.generate_master_seed()
    print(f"Specific Quote: \"{specific_quote}\"")
    print(f"Master Seed: {specific_seed} (Expected: 9690)")
    assert specific_seed == 9690
