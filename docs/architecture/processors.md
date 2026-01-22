# Architecture: Processor Layer

Processors are thin, technique-specific modules that:

- Load raw data
- Map config to math functions
- Apply technique-specific transforms
- Build plot layers
- Provide metadata for UI

## Processor Responsibilities

### 1. Raw Loading
Convert file to raw arrays.

### 2. Processing
Call universal math functions:

data = data_utils.smooth(data, window=7)

### 3. Technique-Specific Transforms
Examples:

- NMR phasing
- MS calibration
- IR band math

### 4. Plot Layer Construction
Processors define how data should be visualized:

layers = [ {"type": "line", "source": "processed"} ]

### 5. Metadata
Used by UI:

available_tools = ["baseline", "smooth", "peaks"]

## What Processors Must Not Do

- Implement math
- Implement plotting
- Implement IO
- Implement pipeline logic
- Store state



