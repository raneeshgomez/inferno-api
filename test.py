from preprocessor.pipeline import NluPipeline

pipeline = NluPipeline()
print(pipeline.extract_named_ents("An apple is a type of fruit."))