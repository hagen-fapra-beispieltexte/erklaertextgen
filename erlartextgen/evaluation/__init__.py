import pipeline
import linguistic.indicators 
import cefr.word_rank
import safety

def evaluate(text):
    doc = pipeline.process(text)


    indicators_structural_complexity = (
        linguistic.indicators.compute_structural_complexity_indicators(doc)
    )
    indicators_ambiguity = linguistic.indicators.compute_ambiguity_indicators(doc)

    out = {
        'indicators_structural_complexty': indicators_structural_complexity,
        'indicators_ambiguity': indicators_ambiguity,
        'cefr_efflex_values': cefr.word_rank.analyze_first_observation(doc),
        'safety': safety.analyze(text)
    }

    print(out)


evaluate(
    "This is a very long test sentence, written behind a wall, in which we describe that Anna gives an apple to Tom - it's complex."
)
