from abc import ABC, abstractmethod

class TTSProvider(ABC):
    @abstractmethod
    def synthesize_and_play(self, text: str) -> None:
        """Synthesize text and block until audio is fully played."""
        pass
