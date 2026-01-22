# Developer Guide: Adding a Tool

A tool is a processing step that maps config to math.

## Step 1 — Add Config Fields

In `config/schema.py`:

class DerivativeConfig(BaseModel): enabled: bool = False order: int = 1


Add defaults in:

config/defaults/<tech>.json


## Step 2 — Add to Processor Metadata

available_tools = ["baseline", "smooth", "derivative"]



## Step 3 — Map Config to Math

if config.processing.derivative.enabled: data = data_utils.derivative(data, order=config.processing.derivative.order)


## Step 4 — Add Plot Layers (Optional)

layers.append({"type": "line", "source": "derivative"})

## Step 5 — Add Tests

Add tests in:

tests/test_processors/

