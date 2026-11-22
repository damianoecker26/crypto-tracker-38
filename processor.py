import logging
from typing import Dict, Any, Callable

class InputProcessor:
    def __init__(self):
        self.required_fields = {'symbol': str, 'amount': (int, float), 'side': str}
        self.logger = logging.getLogger('crypto-tracker-38')

    def validate(self, payload: Dict[str, Any]) -> bool:
        for field, expected_type in self.required_fields.items():
            if field not in payload or not isinstance(payload[field], expected_type):
                self.logger.warning(f'Invalid packet rejected: {field}')
                return False
        if payload['side'] not in ['buy', 'sell']:
            return False
        return True

    def run_loop(self, stream: Iterable[Dict[str, Any]]):
        for packet in stream:
            try:
                if self.validate(packet):
                    self.process_trade(packet)
                else:
                    self.quarantine(packet)
            except Exception as e:
                self.logger.error(f'Loop disruption: {e}')

    def process_trade(self, trade: Dict[str, Any]):
        print(f'Execution: {trade["symbol"]} @ {trade["amount"]}')

    def quarantine(self, packet: Dict[str, Any]):
        self.logger.info(f'Discarded malicious payload: {packet}')