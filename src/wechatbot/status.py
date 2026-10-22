"""Read-only, closed metadata. Inspect never constructs a runner or UI adapter."""
import json


def inspect(config):
    from .pyweixin_probe import inspect_candidate
    d = config.data
    return dict(phase='offline_only', configuration='valid', config_digest=config.digest,
                transport=d['bot']['transport'], enabled=d['bot']['enabled'],
                sends_enabled=d['runtime']['sends_enabled'], production_eligible=False,
                identity='unverified', mentions='unverified', delivery='unverified',
                real_channel=False, real_model=False,
                pyweixin_candidate=inspect_candidate())


def make_health_server(config):
    """Explicit manual call only. Bind conflicts raise; no automatic port fallback."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    payload = json.dumps(inspect(config)).encode()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != '/health':
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_):
            pass

    runtime = config.data['runtime']
    return HTTPServer((runtime['host'], runtime['health_port']), Handler)
