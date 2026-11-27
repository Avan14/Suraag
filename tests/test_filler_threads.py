"""The filler's source label is per thread, so concurrent visitors cannot mislabel each other's case."""
import threading

from suraag import filler


def test_last_source_is_kept_per_thread():
    seen = {}

    def run(name: str, value: str, ready: threading.Barrier) -> None:
        filler._local.source = value
        ready.wait()  # both threads have written before either reads
        seen[name] = filler.last_source

    ready = threading.Barrier(2)
    threads = [threading.Thread(target=run, args=(n, v, ready)) for n, v in (("a", "llm"), ("b", "stub"))]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    assert seen == {"a": "llm", "b": "stub"}
