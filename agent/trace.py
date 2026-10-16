"""Observability. In mock mode, collects spans and prints a trace table that
mirrors what you'll see in Arize/Phoenix. In live mode, set up Phoenix OTEL and
these spans export there instead.

Usage:
    from trace import tracer
    with tracer.span("browse", supplier="BoroughBev") as s:
        ...
        s.set("rows", 10)
"""
import time
import config

_otel_span = None
_provider = None
if config.PHOENIX_LIVE:
    try:
        # Real mode: wire Phoenix. Exact helper may differ by version — see README.
        from phoenix.otel import register  # type: ignore
        _provider = register(
            project_name="parwatch",
            endpoint=config.get("PHOENIX_COLLECTOR_ENDPOINT") or None,
        )
        from opentelemetry import trace as _ot  # type: ignore
        _otel_span = _ot.get_tracer("parwatch").start_as_current_span
        print("[trace] Phoenix OTEL registered — spans will export to Arize/Phoenix.")
    except Exception as e:  # noqa: BLE001
        print(f"[trace] Phoenix setup failed ({e}); falling back to console trace.")
        _otel_span = None


def flush():
    """Force any buffered spans to export before the process exits."""
    if _provider is not None:
        try:
            _provider.force_flush()
        except Exception:  # noqa: BLE001
            pass


class _Span:
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = dict(attrs)
        self.t0 = time.time()
        self.status = "ok"

    def set(self, key, value):
        self.attrs[key] = value

    def hold(self, reason):
        self.status = "held"
        self.attrs["hold_reason"] = reason


class Tracer:
    def __init__(self):
        self.spans = []

    class _Ctx:
        def __init__(self, tracer, span, otel_cm):
            self.tracer = tracer
            self.span = span
            self.otel_cm = otel_cm

        def __enter__(self):
            if self.otel_cm:
                self._o = self.otel_cm.__enter__()
            return self.span

        def __exit__(self, *exc):
            self.span.attrs["ms"] = int((time.time() - self.span.t0) * 1000)
            self.tracer.spans.append(self.span)
            if self.otel_cm:
                for k, v in self.span.attrs.items():
                    try:
                        self._o.set_attribute(f"parwatch.{k}", v)
                    except Exception:  # noqa: BLE001
                        pass
                self.otel_cm.__exit__(*exc)
            return False

    def span(self, name, **attrs):
        otel_cm = _otel_span(name) if _otel_span else None
        return self._Ctx(self, _Span(name, attrs), otel_cm)

    def print_table(self):
        print("\n── Arize trace (agent run) " + "─" * 30)
        for s in self.spans:
            flag = "HELD" if s.status == "held" else "ok"
            extra = s.attrs.get("hold_reason") or s.attrs.get("summary") or ""
            print(f"  {s.name:<10} {s.attrs.get('ms', 0):>5}ms  {flag:<5} {extra}")
        print("─" * 56)


tracer = Tracer()
