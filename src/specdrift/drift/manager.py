import time
from typing import List, Optional
from specdrift.core.models import DriftEventDefinition

class DriftManager:
    def __init__(self, events: List[DriftEventDefinition]):
        self.all_events = events
        self.injected_events: List[DriftEventDefinition] = []
        self.step_count = 0

    def step(self) -> Optional[DriftEventDefinition]:
        """Called by the environment/agent loop on each agent action step."""
        self.step_count += 1
        return self._check_triggers()

    def _check_triggers(self) -> Optional[DriftEventDefinition]:
        for event in self.all_events:
            if event in self.injected_events:
                continue
            
            # Simple MVP trigger parsing: "step: N"
            if event.trigger_condition.startswith("step:"):
                try:
                    target_step = int(event.trigger_condition.split(":")[1].strip())
                    if self.step_count >= target_step:
                        self.injected_events.append(event)
                        return event
                except ValueError:
                    pass
        return None

    def get_visible_events(self) -> List[DriftEventDefinition]:
        return list(self.injected_events)
