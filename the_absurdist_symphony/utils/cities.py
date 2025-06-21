CITIES = [
    "London", "Paris", "New York", "Tokyo", "Berlin", "Moscow", "Cairo",
    "Rio de Janeiro", "Sydney", "Beijing", "Rome", "Madrid", "Toronto",
    "Buenos Aires", "Mexico City", "Lagos", "Mumbai", "Jakarta", "Seoul",
    "Bangkok", "Istanbul", "Lima", "Bogota", "Santiago", "Hanoi", "Tehran",
    "Riyadh", "Baghdad", "Nairobi", "Cape Town", "Singapore", "Hong Kong",
    "Kyiv", "Amsterdam", "Brussels", "Vienna", "Warsaw", "Budapest", "Prague",
    "Lisbon", "Dublin", "Oslo", "Stockholm", "Copenhagen", "Helsinki",
    "Athens", "Wellington", "Canberra", "Ottawa", "Brasilia", "New Delhi",
    "Islamabad", "Dhaka", "Manila", "Kuala Lumpur", "Zurich", "Geneva",
    "Vancouver", "Montreal", "Chicago", "Los Angeles", "San Francisco",
    "Miami", "Dallas", "Houston", "Boston", "Philadelphia", "Washington D.C.",
    "Seattle", "Denver", "Phoenix", "Atlanta", "Detroit", "Minneapolis",
    "St. Petersburg", "Novosibirsk", "Yekaterinburg", "Samara", "Omsk",
    "Kazan", "Ufa", "Rostov-on-Don", "Volgograd", "Perm", "Krasnoyarsk",
    "Saratov", "Voronezh", "Tolyatti", "Izhevsk", "Ulyanovsk", "Barnaul",
    "Vladivostok", "Yaroslavl", "Irkutsk", "Tyumen", "Makhachkala", "Orenburg",
    "Kemerovo", "Ryazan", "Tomsk", "Astrakhan", "Penza", "Lipetsk", "Kirov"
]

# A few more whimsical or unusual locations
WHIMSICAL_CITIES = [
    "Timbuktu", "Ushuaia", "Longyearbyen", "Reykjavik", "Kathmandu",
    "Lhasa", "Vladivostok", "Anchorage", "Honolulu", "Fiji", "Male",
    "Monaco", "Nuuk", "Antananarivo", "Ouagadougou", "Djibouti",
    "Ashgabat", "Pyongyang", "Zanzibar City", "El Alto", "La Paz",
    "Stanley", "Adamstown", "Kingston" # Kingston, Norfolk Island
]

ALL_CITIES = list(set(CITIES + WHIMSICAL_CITIES))

if __name__ == '__main__':
    import random
    print(f"Total unique cities: {len(ALL_CITIES)}")
    print(f"Random city: {random.choice(ALL_CITIES)}")
