import pipeline
import linguistic.indicators
import cefr.word_rank


def evaluate(text):
    doc = pipeline.process(text)
    indicators_structural_complexity = (
        linguistic.indicators.compute_structural_complexity_indicators(doc)
    )
    indicators_ambiguity = linguistic.indicators.compute_ambiguity_indicators(doc)

    print(indicators_structural_complexity)
    print(indicators_ambiguity)

    level_values = cefr.word_rank.analyze_first_observation(doc)
    print(level_values)


evaluate(
    "This is a very long test sentence, written behind a wall, in which we describe that Anna gives an apple to Tom - it's complex."
)
