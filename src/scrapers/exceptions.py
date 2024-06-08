class TimeoutException(Exception):
    def __init__(
        self,
        timeout: int = 0,
        message: str = "Timed out waiting {timout}s for page to load",
    ):
        self.timeout = timeout
        super().__init__(message.format(timout=self.timeout))
