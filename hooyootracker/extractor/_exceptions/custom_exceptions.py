class SourceScrapingError(Exception):
    """Custom exception for issues encountered while scraping data from the source"""

    def __init__(self, source_name) -> None:
        self.message = f"Error extracting data from {source_name}. The source may have changed. Skipping source"
        super().__init__(self.message)


class DataExtractionError(Exception):
    """Custom exception for issues encountered when extracting either code or reward description"""

    def __init__(self, source_name, data_extraction_type) -> None:
        self.message = f"Error extracting {data_extraction_type} from {source_name}. The data may have changed. Skipping entry."
        super().__init__(self.message)
