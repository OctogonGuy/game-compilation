"""
Program: random_sentence_generator.py
Author: Alex Gill
Generates and displays sentences using simple grammar
and randomly selected vocabulary.
"""
from util import readfile
import random

# Grammatical categories
patterns = (1, 2, 3, 4, 5)
numbers = ('singular', 'plural')
tenses = ('past', 'present', 'future')
aspects = ('simple', 'perfect', 'continuous', 'perfect continuous')

# Probability tables
probability = {'adjective': 0.25,
               'adverb': 0.3,
               'pronoun': 0.2,
               'interjection': 0.1,
               'prepositional_phrase': 0.2,
               'compound_sentence': 0.1,
               'complex_sentence': 0.1,
               'be_verb': 0.5}

# Vocabulary
nouns = readfile('WORDS\\nouns.txt', ('singular', 'plural'))
pronouns = {'subject': ('I', 'we', 'he', 'she', 'it', 'they', 'you'),
            'object': ('me', 'us', 'him', 'her', 'it', 'them', 'you'),
            'possessive': ('my', 'our', 'his', 'her', 'its', 'their', 'your')}
verbs = {'intransitive': readfile('WORDS\\verbs-intransitive.txt'),
         'transitive': readfile('WORDS\\verbs-transitive.txt'),
         'ditransitive': readfile('WORDS\\verbs-ditransitive.txt'),
         'linking': readfile('WORDS\\verbs-linking.txt'),
         'copulative': readfile('WORDS\\verbs-copulative.txt'),
         'be': (('am', 'is', 'are', 'was', 'were', 'be', 'being', 'been'),)}
adjectives = readfile('WORDS\\adjectives.txt')
adverbs = readfile('WORDS\\adverbs.txt')
prepositions = ('aboard', 'about', 'above', 'across', 'after', 'against',
                'along', 'among', 'around', 'as', 'at', 'before', 'behind',
                'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by',
                'despite', 'down', 'during', 'except', 'for', 'from', 'in',
                'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'out',
                'outside', 'over', 'past', 'since', 'through', 'throughout',
                'to', 'toward', 'under', 'underneath', 'until', 'up', 'upon',
                'with', 'without', 'without')
conjunctions = {'coordinating': ('and', 'or', 'but'),
                'subordinating': readfile(
                    'WORDS\\conjunctions-subordinating.txt')}
interjections = readfile('WORDS\\interjections.txt')


def sentence():
    """Builds and returns a sentence."""

    # Construct a clause
    constituent = clause()

    compound_or_complex = random.random()
    # Add a compound clause to make a compound sentence
    if compound_or_complex < probability['compound_sentence']:
        constituent = constituent + ', ' + \
            random.choice(conjunctions['coordinating']) + ' ' + clause()
    # Add a dependend clause to make a complex sentence
    elif compound_or_complex < probability['complex_sentence'] + \
        probability['complex_sentence']:
        # Add it before the independent clause
        if random.choice((True, False)):
            constituent = random.choice(conjunctions['subordinating']) + \
                ' ' + clause() + ', ' + constituent
        # Add it after the independent clause
        else:
            constituent = constituent + ' ' + \
                random.choice(conjunctions['subordinating']) + ' ' + clause()

    # Add an interjection
    if random.random() < probability['interjection']:
        interjection = random.choice(interjections)
        # Capitalize the next word if interjection does not end in comma
        if interjection[-1] != ',':
            constituent = constituent[0].upper() + constituent[1:]
        constituent = interjection + ' ' + constituent

    # Capitalize the sentence
    constituent = constituent[0].upper() + constituent[1:] + '.'

    return constituent


def clause():
    """Builds and returns a clause."""

    # Randomly choose the grammatical categories
    pattern = random.choice(patterns)
    number = random.choice(numbers)

    # Construct a clause of a certain pattern with a noun phrase
    constituent = noun_phrase('subject', number)

    # Determin the person of the constituent noun phrase
    if constituent == 'I' or constituent == 'we':
        person = 'first'
    elif constituent == 'you':
        person = 'second'
    else:
        person = 'third'
    
    # Add a verb phrase to the constituent noun phrase
    constituent = constituent + ' ' + verb_phrase(pattern, number, person)

    # Add a prepositional phrase
    if random.random() < probability['prepositional_phrase']:
        before = random.choice((True, False))
        if before:  # Insert before
            constituent = prepositional_phrase() + ', ' + constituent
        else:       # Insert after
            constituent = constituent + ' ' + prepositional_phrase()

    return constituent


def noun_phrase(case, number=random.choice(numbers)):
    """Builds and returns a noun phrase."""

    # Choose a noun or pronoun
    if random.random() < probability['pronoun']:
        return random.choice(pronouns[case])
    constituent = random.choice(nouns)[number]

    # Add an adjective
    if random.random() < probability['adjective']:
        if random.random() < probability['pronoun']:
            return random.choice(pronouns['possessive']) + ' ' + constituent
        constituent = random.choice(adjectives) + ' ' + constituent
    
    # Add an article
    if number == 'singular':    # Noun is singular
        if constituent[0].lower() in ('a', 'e', 'i', 'o', 'u'):
            valid_articles = ('an', 'the')
        else:
            valid_articles = ('a', 'the')
        constituent = random.choice(valid_articles) + ' ' + constituent
    else:                       # Noun is plural
        add_article = random.choice((True, False))
        if add_article: # Add an article
            constituent = 'the ' + constituent
    
    return constituent


def verb_phrase(pattern, number, person):
    """Builds and returns a verb phrase."""

    # Randomly choose the tense and aspect
    tense = random.choice(tenses)
    aspect = random.choice(aspects)

    # Determine verb type
    if pattern == 1:
        type = 'intransitive'
    elif pattern == 2:
        type = 'transitive'
    elif pattern == 3:
        type = 'ditransitive'
    elif pattern == 4:
        if random.random() < probability['be_verb']:
            type = 'be'
        else:
            type = 'linking'
    elif pattern == 5:
        if random.random() < probability['be_verb']:
            type = 'be'
        else:
            type = 'copulative'
    
    # Determine the inflection
    if not type == 'be':    # Non-be verbs
        if aspect == 'simple' and tense == 'present' and person == 'first':
            inflectionIndex = 1 # Standard
        elif aspect == 'simple' and tense == 'present' and number =='singular':
            inflectionIndex = 0 # -s
        elif aspect == 'simple' and (tense == 'present' or tense == 'future'):
            inflectionIndex = 1 # Standard
        elif aspect == 'simple' and tense == 'past':
            inflectionIndex = 2 # -ed
        elif aspect == 'perfect':
            inflectionIndex = 3 # -ed or exception
        else:
            inflectionIndex = 4
    else:                   # Be verbs
        if aspect == 'simple' and tense == 'present' and number == 'singular' \
                and person == 'first': 
            inflectionIndex = 0 # am
        elif aspect == 'simple' and tense == 'present' and number =='singular':    
            inflectionIndex = 1 # is
        elif aspect == 'simple' and tense == 'present':
            inflectionIndex = 2 # are
        elif aspect == 'simple' and tense == 'past' and number == 'singular':
            inflectionIndex = 3 # was
        elif aspect == 'simple' and tense == 'past':
            inflectionIndex = 4 # were
        elif aspect == 'simple' and tense == 'future':
            inflectionIndex = 5 # be
        elif aspect == 'perfect':
            inflectionIndex = 7 # been
        else:
            inflectionIndex = 6 # being
    
    # Get the random verb
    constituent = random.choice(verbs[type])[inflectionIndex]

    # Conjugate the verb
    if aspect == 'simple' and tense == 'future':
        constituent = 'will ' + constituent
    elif aspect == 'perfect':
        if tense == 'present':
            if number == 'singular' and person != 'first':
                constituent = 'has ' + constituent
            else:
                constituent = 'have ' + constituent
        elif tense == 'past':
            constituent = 'had ' + constituent
        else:
            constituent = 'will have ' + constituent
    elif aspect == 'continuous':
        if tense == 'present':
            if number == 'singular' and person == 'first':
                constituent = 'am ' + constituent
            elif number == 'singular':
                constituent = 'is ' + constituent
            else:
                constituent = 'are ' + constituent
        elif tense == 'past':
            if number == 'singular':
                constituent = 'was ' + constituent
            else:
                constituent = 'were ' + constituent
        else:
            constituent = 'will be ' + constituent
    elif aspect == 'perfect continuous':
        if tense == 'present':
            if number == 'singular' and person != 'first':
                constituent = 'has been ' + constituent
            else:
                constituent = 'have been ' + constituent
        elif tense == 'past':
            constituent = 'had been ' + constituent
        else:
            constituent = 'will have been ' + constituent

    # Construct the verb phrase according to the pattern
    if pattern == 1:
        constituent = constituent
    elif pattern == 2:
        constituent = constituent + ' ' + noun_phrase('object')
    elif pattern == 3:
        constituent = constituent + ' ' + noun_phrase('object') + ' ' + \
            noun_phrase('object')
    elif pattern == 4:
        constituent = constituent + ' ' + noun_phrase('object')
    else:
        constituent = constituent + ' ' + random.choice(adjectives)

    # Add an adverb
    if random.random() < probability['adverb']:
        before = random.choice((True, False))
        if before:  # Insert before
            constituent = random.choice(adverbs) + ' ' + constituent
        else:       # Insert after
            constituent = constituent + ' ' + random.choice(adverbs)

    return constituent


def prepositional_phrase():
    """Builds and returns a prepositional phrase."""
    return random.choice(prepositions) + ' ' + noun_phrase('object')


# The entry point for program execution
if __name__ == '__main__':
    num_sentences = int(input('Enter the number of sentences: '))
    for i in range(num_sentences):
        print(sentence())
