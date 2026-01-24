class TechniqueRouter:
    """
    Routes metadata to the correct processor.
    """

    def route(self, metadata: dict):
        technique = metadata.get("technique")

        if technique == "uvvis":
            from chemworkbench.processors.uvvis.processor import UVVisProcessor
            return UVVisProcessor()

        if technique == "ir":
            from chemworkbench.processors.ir.processor import IRProcessor
            return IRProcessor()

        if technique == "raman":
            from chemworkbench.processors.raman.processor import RamanProcessor
            return RamanProcessor()

        if technique == "nmr":
            from chemworkbench.processors.nmr.processor import NMRProcessor
            return NMRProcessor()

        if technique == "ms":
            from chemworkbench.processors.ms.processor import MSProcessor
            return MSProcessor()

        if technique == "chrom":
            from chemworkbench.processors.chrom.processor import ChromProcessor
            return ChromProcessor()

        if technique == "electrochemistry":
            from chemworkbench.processors.echem.processor import EchemProcessor
            return EchemProcessor()

        if technique == "epr":
            from chemworkbench.processors.epr.processor import EPRProcessor
            return EPRProcessor()

        raise ValueError(f"No processor found for technique: {technique}")
