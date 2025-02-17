#!/bin/bash

# Create images directory if it doesn't exist
mkdir -p images

# Extract and render the System Context diagram
sed -n '/```plantuml/,/```/{/```plantuml/d;/```/d;p}' ../ResponseStreamingADR.md | \
  grep -v '^$' | \
  plantuml -pipe > images/streaming_context.png

# Extract and render the Container diagram
sed -n '/```plantuml/,/```/{/```plantuml/d;/```/d;p}' ../ResponseStreamingADR.md | \
  grep -v '^$' | \
  plantuml -pipe > images/streaming_container.png 