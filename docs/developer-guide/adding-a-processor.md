
# Developer Guide: Adding a Processor

Processors in ChemWorkBench are modular, technique‑specific components that plug into the universal pipeline.  
They do not implement math, plotting, IO, or pipeline logic.  
They orchestrate technique‑specific behavior using shared utilities.

Processors live under:


chemworkbench/processors/<technique>/

Each processor folder contains:


init.py config.py processor.py

---

## Step 1 — Create the Folder

Inside:


chemworkbench/processors/

create:


<technique>/ init.py config.py processor.py

Example:


chemworkbench/processors/uvvis/

---

## Step 2 — Create the Config Model

Each processor defines a Pydantic config model inheriting from:


from chemworkbench.core.models import BaseProcessorConfig

Example:

python
class UVVisConfig(BaseProcessorConfig):
    baseline_method: str = "polynomial"
    smoothing_method: str = "moving_average"
    normalization_method: str = "max"
    detect_peaks: bool = True
    integration_regions: List[Tuple[float, float]] = []


The config:
- validates user input
- controls math operations
- is included in metadata
- is JSON‑serializable

Step 3 — Implement the Processor Class
A processor implements the universal pipeline hooks:
class UVVisProcessor:
    technique = Technique.UV_VIS

    def load(self, data, config): ...
    def validate(self, data, config): ...
    def preprocess(self, data, config): ...
    def process(self, data, config): ...
    def postprocess(self, data, config): ...
    def make_plots(self, data, config): ...
    def export(self, data, config): ...
    def build_metadata(self, data, config): ...
    def compute_qc(self, data, config): ...


Only process() is strictly required.
All others are optional but recommended.
Processors must:
- call math utilities from chemworkbench/utils/
- return JSON‑serializable processed data
- generate PlotConfig objects (not figures)
- provide metadata + QC metrics

Step 4 — Add Plot Definitions
Processors do not render plots.
They return PlotConfig objects:
PlotConfig(
    id="uvvis_main",
    title="UV-Vis Spectrum",
    layers=[
        PlotLayerConfig(
            label="processed",
            plot_type=PlotType.LINE,
            x=x.tolist(),
            y=y.tolist(),
            color="blue",
        )
    ]
)


The plotting engine later renders these into real figures.

Step 5 — Add Tests
Create:
tests/test_<technique>_processor.py


Test:
- preprocessing
- processing
- metadata
- QC metrics
- plot generation
- error handling
The UV‑Vis processor is the reference implementation.

Step 6 — (Optional) Register the Processor
When the registry system is implemented, processors will be registered via:
from chemworkbench.core.registry import register
register("uvvis", UVVisProcessor)


For now, processors are instantiated directly.

Step 7 — Add Example Script
Add:
chemworkbench/examples/test_<technique>_pipeline.py


Example:
processor = UVVisProcessor()
config = UVVisConfig()
result = run_pipeline(processor, config, data)



Summary
A processor must:
- define a config model
- implement pipeline hooks
- call shared math utilities
- return processed data
- generate PlotConfig objects
- provide metadata + QC metrics
Processors must not:
- implement math
- implement plotting
- implement IO
- store state
- bypass the pipeline
The UV‑Vis processor is the canonical example.

---




