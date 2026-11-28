"""
Notes are from:
https://www.khanacademy.org/science/biology/water-acids-and-bases/hydrogen-bonding-in-water/a/hydrogen-bonding-in-water
https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
https://en.wikipedia.org/wiki/Mathematics
https://en.wikipedia.org/wiki/History_of_Poland
"""

notes = [
    {"id": "jupiter", "content": "Jupiter is the largest planet in our solar system."},
    {
        "id": "mars",
        "content": "Mars gets its reddish color from iron minerals in its soil.",
    },
    {
        "id": "photosynthesis",
        "content": "Photosynthesis lets plants turn sunlight into energy.",
    },
    {"id": "london_finance", "content": "London is known for its financial district."},
    {
        "id": "london_population",
        "content": "London had 9,787,426 inhabitants at the 2011 census.",
    },
    {
        "id": "uk_exports",
        "content": "The United Kingdom is the fourth largest exporter of goods in the world.",
    },
    {
        "id": "body_water",
        "content": "Human body is 60 to 70% water. And it's not just humans—most animals and even tiny bacteria are made up mostly of water",
    },
    {
        "id": "water_molecule",
        "content": "Because oxygen is more electronegative—electron-greedy—than hydrogen, the O atom hogs electrons and keeps them away from the H atoms. This gives the oxygen end of the water molecule a partial negative charge, while the hydrogen end has a partial positive charge. Water is classified as a polar molecule because of its polar covalent bonds and its bent shape",
    },
    {
        "id": "prokaryotes",
        "content": "For a long time, all prokaryotes were classified into a single domain (the largest taxonomic grouping). However, work by microbiologist Carl Woese in the 1970s showed that prokaryotes are divided into two distinct lineages, or lines of descent: Archaea and Bacteria. Today, these groups are considered to form two out of three domains of life. The third domain (Eukarya) includes all eukaryotes, such as plants, animals, and fungi",
    },
    {
        "id": "proteobacteria",
        "content": "The proteobacteria are subdivided into five groups, alpha through epsilon. Species in these groups have a wide range of lifestyles. Some are symbiotic with plants, others live in hot vents deep under the sea, and others yet cause human diseases, such as stomach ulcers (Helicobacter pylori) and food poisoning (Salmonella).",
    },
    {
        "id": "metagenome",
        "content": "The collective genome of such a community is called its metagenome, and the analysis of metagenome sequences is known as metagenomics.",
    },
    {
        "id": "mathematics",
        "content": "Mathematics is a field of knowledge concerned with abstract concepts such as numbers, geometric shapes, sets, functions, and probabilities. It uses logical reasoning and proof to study and establish their properties, often expressed as theorems, formulas, and equations.",
    },
    {
        "id": "arithmetic_geometry",
        "content": "Before the Renaissance, mathematics was divided into two main areas: arithmetic, regarding the study and manipulation of numbers, and geometry, regarding the study of shapes",
    },
    {
        "id": "polish_bronze_age",
        "content": "Poland's Early Bronze Age began around 2400-2300 BC, whereas its Iron Age commenced c. 750-700 BC.",
    },
    {
        "id": "piast_dynasty",
        "content": "Poland was established as a state under the Piast dynasty, which ruled the country between the 10th and 14th centuries.",
    },
    {
        "id": "mieszko",
        "content": "Mieszko converted to Christianity in 966, following his marriage to Princess Doubravka of Bohemia, a fervent Christian.",
    },
]


test_cases = [
    {
        "id": "q1",
        "question": "Which planet is known as the Red Planet?",
        "expected_note_ids": ["mars"],
    },
    {
        "id": "q2",
        "question": "What was the population of London at the 2011 census?",
        "expected_note_ids": ["london_population"],
    },
    {
        "id": "q3",
        "question": "How was mathematics divided before the Renaissance?",
        "expected_note_ids": ["arithmetic_geometry"],
    },
    {
        "id": "q4",
        "question": "What is London known for?",
        "expected_note_ids": ["london_finance"],
    },
    {
        "id": "q5",
        "question": "Is oxygen or hydrogen more electronegative?",
        "expected_note_ids": ["water_molecule"],
    },
    {
        "id": "q6",
        "question": "What percentage of the human body is water?",
        "expected_note_ids": ["body_water"],
    },
    {
        "id": "q7",
        "question": ("How were prokaryotes classified before Carl Woese's research?"),
        "expected_note_ids": ["domains_of_life"],
    },
    {
        "id": "q8",
        "question": "Which organisms belong to the domain Eukarya?",
        "expected_note_ids": ["prokaryotes"],
    },
    {
        "id": "q9",
        "question": "What is a metagenome?",
        "expected_note_ids": ["metagenome"],
    },
    {
        "id": "q10",
        "question": "How do plants obtain energy?",
        "expected_note_ids": ["photosynthesis"],
    },
    {
        "id": "q11",
        "question": "What is the difference between arithmetic and geometry?",
        "expected_note_ids": ["arithmetic_geometry"],
    },
    {
        "id": "q12",
        "question": (
            "According to the notes, where does the United Kingdom "
            "rank among the world's exporters of goods?"
        ),
        "expected_note_ids": ["uk_exports"],
    },
    {
        "id": "q13",
        "question": "Why is Mars red?",
        "expected_note_ids": ["mars"],
    },
    {
        "id": "q14",
        "question": "What does a water molecule consist of?",
        "expected_note_ids": ["water_molecule"],
    },
    {
        "id": "q15",
        "question": "What is the shape of a water molecule?",
        "expected_note_ids": ["water_molecule"],
    },
    {
        "id": "q16",
        "question": "When did the Bronze Age begin in Poland?",
        "expected_note_ids": ["polish_bronze_age"],
    },
    {
        "id": "q17",
        "question": "Which dynasty ruled Poland in the 12th century?",
        "expected_note_ids": ["piast_dynasty"],
    },
    {
        "id": "q18",
        "question": "Who was Mieszko married to?",
        "expected_note_ids": ["mieszko"],
    },
    {
        "id": "q19",
        "question": "Which religion did Mieszko adopt in 966?",
        "expected_note_ids": ["mieszko"],
    },
    {
        "id": "q20",
        "question": "What diseases can bacteria cause?",
        "expected_note_ids": ["proteobacteria"],
    },
    {
        "id": "q21",
        "question": "What is the largest planet in our solar system?",
        "expected_note_ids": ["jupiter"],
    },
    {
        "id": "q22",
        "question": (
            "What percentage of the human body is water, and why is a water molecule polar?"
        ),
        "expected_note_ids": ["body_water", "water_molecule"],
    },
    {
        "id": "q23",
        "question": ("Which dynasty ruled Poland in the 12th century, and whom did Mieszko marry?"),
        "expected_note_ids": ["piast_dynasty", "mieszko"],
    },
    {
        "id": "q24",
        "question": "What is the capital of Japan?",
        "expected_note_ids": [],
    },
    {
        "id": "q25",
        "question": "What is London's population today?",
        "expected_note_ids": [],
    },
]
